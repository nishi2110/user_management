from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import User

class AdminService:
    @staticmethod
    async def get_all_users(db: AsyncSession):
        """
        Retrieve all users from the database.

        Args:
            db (AsyncSession): The database session.

        Returns:
            List[User]: List of all users.
        """
        query = select(User)
        result = await db.execute(query)
        return result.scalars().all()

    @staticmethod
    async def delete_user_by_id(db: AsyncSession, user_id):
        """
        Delete a user by their ID.

        Args:
            db (AsyncSession): The database session.
            user_id (UUID): The ID of the user to delete.

        Returns:
            bool: True if deletion was successful, False otherwise.
        """
        user = await db.get(User, user_id)
        if user:
            await db.delete(user)
            await db.commit()
            return True
        return False
