from fastapi import HTTPException
from builtins import Exception, bool, classmethod, int, str
from datetime import datetime, timezone
import secrets
from typing import Optional, Dict, List
from pydantic import ValidationError
from sqlalchemy import func, null, update, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_email_service, get_settings
from app.models.user_model import User
from app.schemas.user_schemas import UserCreate, UserUpdate
from app.utils.nickname_gen import generate_nickname
from app.utils.security import generate_verification_token, hash_password, verify_password, validate_password
from uuid import UUID
from app.services.email_service import EmailService
from app.models.user_model import UserRole
from app.utils.validators import validate_url_safe_username
from sqlalchemy.exc import IntegrityError
import logging
from typing import List, Tuple 



settings = get_settings()
logger = logging.getLogger(__name__)

class UserService:
    @classmethod
    async def _execute_query(cls, session: AsyncSession, query, commit: bool = False):
        try:
            result = await session.execute(query)
            if commit:  # Only commit if the `commit` parameter is True
                await session.commit()
            return result
        except SQLAlchemyError as e:
            logger.error(f"Database error: {e}")
            await session.rollback()
            return None


    @classmethod
    async def _fetch_user(cls, session: AsyncSession, **filters) -> Optional[User]:
        query = select(User).filter_by(**filters)
        result = await cls._execute_query(session, query, commit=False)  # Explicitly specify commit=False for clarity
        return result.scalars().first() if result else None

    @classmethod
    async def get_by_id(cls, session: AsyncSession, user_id: UUID) -> Optional[User]:
        return await cls._fetch_user(session, id=user_id)

    @classmethod
    async def get_by_nickname(cls, session: AsyncSession, nickname: str) -> Optional[User]:
        return await cls._fetch_user(session, nickname=nickname)

    @classmethod
    async def get_by_email(cls, session: AsyncSession, email: str) -> Optional[User]:
        return await cls._fetch_user(session, email=email)

    @classmethod
    async def create(cls, session: AsyncSession, user_data: Dict[str, str], email_service: EmailService) -> Optional[User]:
        try:
           # Check if the user is the first user
           is_first_user = await cls.is_first_user(session)
           logger.debug(f"is_first_user: {is_first_user}")  # Debug statement
           if is_first_user:
               user_data["role"] = UserRole.ADMIN.name  # Automatically assign ADMIN role
           else:
               # Set default role if not provided
               user_data.setdefault("role", UserRole.AUTHENTICATED.name)
           logger.debug(f"Assigned role: {user_data['role']}")
           validated_data = UserCreate(**user_data).model_dump()

           # Check for existing email
           existing_user = await cls.get_by_email(session, validated_data['email'])
           if existing_user:
               logger.error("User with given email already exists.")
               return None

           # Validate and hash password
           password = validated_data.pop('password')
           try:
               validate_password(password)  # Ensures password meets security criteria
           except ValueError as e:
               logger.error(f"Password validation failed: {e}")
               return None
           validated_data['hashed_password'] = hash_password(password)

           # Check for existing nickname
           if validated_data.get("nickname"):
               existing_nickname = await cls.get_by_nickname(session, validated_data["nickname"])
               if existing_nickname:
                   logger.error("User with given nickname already exists.")
                   return None
           else:
               # Auto-generate a unique nickname if not provided
               new_nickname = generate_nickname()
               while await cls.get_by_nickname(session, new_nickname):
                   new_nickname = generate_nickname()
               validated_data["nickname"] = new_nickname

           # Prepare new user
           new_user = User(**validated_data)
           
           # Assign role explicitly based on whether it’s the first user
           new_user.role = UserRole.ADMIN if is_first_user else UserRole.AUTHENTICATED

           # Add and commit new user
           new_user.verification_token = generate_verification_token()
           session.add(new_user)
           await session.commit()
           await session.refresh(new_user)  # Ensure in-memory reflects database state

           # Send verification email
           await email_service.send_verification_email(new_user)
           return new_user

        except ValidationError as e:
            logger.error(f"Validation error during user creation: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error during user creation: {e}")
            return None

    @classmethod
    async def is_first_user(cls, session: AsyncSession) -> bool:
       """Check if the current user is the first user in the database."""
       query = select(func.count()).select_from(User)
       result = await session.execute(query)
       count = result.scalar()  # Ensure count is an integer
       logger.debug(f"User count in database: {count}")
       return count == 0

    @classmethod
    async def update(cls, session: AsyncSession, user_id: UUID, update_data: Dict[str, str]) -> Optional[User]:
        try:
            validated_data = UserUpdate(**update_data).dict(exclude_unset=True)

            # Check for nickname uniqueness if nickname is being updated
            if "nickname" in validated_data:
                existing_nickname = await cls.get_by_nickname(session, validated_data["nickname"])
                if existing_nickname and existing_nickname.id != user_id:
                    logger.error("User with given nickname already exists.")
                    return None

            # Hash the password if being updated
            if 'password' in validated_data:
                validated_data['hashed_password'] = hash_password(validated_data.pop('password'))

            # Update the user
            query = update(User).where(User.id == user_id).values(**validated_data).execution_options(synchronize_session="fetch")
            await cls._execute_query(session, query)

            updated_user = await cls.get_by_id(session, user_id)
            if updated_user:
                session.refresh(updated_user)  # Explicitly refresh the updated user object
                logger.info(f"User {user_id} updated successfully.")
                return updated_user

            logger.error(f"User {user_id} not found after update attempt.")
            return None

        except Exception as e:
            logger.error(f"Error during user update: {e}")
            return None

    @classmethod
    async def delete(cls, session: AsyncSession, user_id: UUID) -> bool:
        user = await cls.get_by_id(session, user_id)
        if not user:
            logger.info(f"User with ID {user_id} not found.")
            return False
        await session.delete(user)
        await session.commit()
        return True

    @classmethod
    async def list_users(cls, session: AsyncSession, skip: int = 0, limit: int = 10) -> List[User]:
        query = select(User).offset(skip).limit(limit)
        result = await cls._execute_query(session, query)
        return result.scalars().all() if result else []

    @classmethod
    async def register_user(cls, session: AsyncSession, user_data: Dict[str, str], get_email_service) -> Optional[User]:
        return await cls.create(session, user_data, get_email_service)
    

    @classmethod
    async def login_user(cls, session: AsyncSession, email: str, password: str) -> Optional[User]:
        user = await cls.get_by_email(session, email)
        if user:
            if user.email_verified is False:
                return None
            if user.is_locked:
                return None
            if verify_password(password, user.hashed_password):
                user.failed_login_attempts = 0
                user.last_login_at = datetime.now(timezone.utc)
                session.add(user)
                await session.commit()
                return user
            else:
                user.failed_login_attempts += 1
                if user.failed_login_attempts >= settings.max_login_attempts:
                    user.is_locked = True
                session.add(user)
                await session.commit()
        return None

    @classmethod
    async def is_account_locked(cls, session: AsyncSession, email: str) -> bool:
        user = await cls.get_by_email(session, email)
        return user.is_locked if user else False


    @classmethod
    async def reset_password(cls, session: AsyncSession, user_id: UUID, new_password: str) -> bool:
        hashed_password = hash_password(new_password)
        user = await cls.get_by_id(session, user_id)
        if user:
            user.hashed_password = hashed_password
            user.failed_login_attempts = 0  # Resetting failed login attempts
            user.is_locked = False  # Unlocking the user account, if locked
            session.add(user)
            await session.commit()
            return True
        return False

    @classmethod
    async def verify_email_with_token(cls, session: AsyncSession, user_id: UUID, token: str) -> bool:
        user = await cls.get_by_id(session, user_id)
        if user and user.verification_token == token:
            user.email_verified = True
            user.verification_token = None  # Clear the token once used
            user.role = UserRole.AUTHENTICATED
            session.add(user)
            await session.commit()
            return True
        return False

    @classmethod
    async def count(cls, session: AsyncSession) -> int:
        """
        Count the number of users in the database.

        :param session: The AsyncSession instance for database access.
        :return: The count of users.
        """
        query = select(func.count()).select_from(User)
        result = await session.execute(query)
        count = result.scalar()
        return count
    
    @classmethod
    async def unlock_user_account(cls, session: AsyncSession, user_id: UUID) -> bool:
        user = await cls.get_by_id(session, user_id)
        if user and user.is_locked:
            user.is_locked = False
            user.failed_login_attempts = 0  # Optionally reset failed login attempts
            session.add(user)
            await session.commit()
            return True
        return False
    
    @classmethod
    async def anonymize_user(cls, session: AsyncSession, user_id: UUID):
        user = await cls.get_by_id(session, user_id)
        if user:
            user.anonymize()
            session.add(user)
            await session.commit()
            return user
        return None


    @staticmethod
    async def search_and_filter_users(
        session: AsyncSession, 
        filters: Dict[str, Optional[str]], 
        skip: int, 
        limit: int
    ) -> Tuple[List[User], int]:
        """
        Search and filter users based on the given criteria.

        :param session: AsyncSession for database access.
        :param filters: Dictionary of search and filter criteria.
        :param skip: Pagination offset.
        :param limit: Number of records to return.
        :return: A tuple containing the list of users and total count.
        """
        query = select(User)

        # Apply filters
        if filters.get("username"):
            query = query.filter(User.nickname.ilike(f"%{filters['username']}%"))
        if filters.get("email"):
            query = query.filter(User.email.ilike(f"%{filters['email']}%"))
        if filters.get("role"):
            query = query.filter(User.role == filters["role"])
        if filters.get("account_status") is not None:
            query = query.filter(User.email_verified == filters["account_status"])
        if filters.get("registration_date_start") and filters.get("registration_date_end"):
            query = query.filter(
                User.created_at.between(filters["registration_date_start"], filters["registration_date_end"])
            )

        # Add pagination
        query = query.offset(skip).limit(limit)

        # Execute the query and count total users
        result = await session.execute(query)
        users = result.scalars().all()

        total_query = select(func.count()).select_from(User)
        total_result = await session.execute(total_query)
        total_users = total_result.scalar()

        return users, total_users

def generate_unique_nickname(session) -> str:
    while True:
        nickname = generate_nickname()
        if not session.query(User).filter_by(nickname=nickname).first():
            return nickname
@classmethod
async def is_nickname_unique(cls, session: AsyncSession, nickname: str) -> bool:
    existing_user = await cls.get_by_nickname(session, nickname)
    return existing_user is None
