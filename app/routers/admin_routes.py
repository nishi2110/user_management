from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_db, require_role
from app.services.admin_service import AdminService
from app.schemas.user_schemas import UserListResponse, UserResponse

router = APIRouter()

@router.get("/users", response_model=UserListResponse, tags=["Admin"])
async def list_all_users(
    db: AsyncSession = Depends(get_db), current_user: dict = Depends(require_role(["ADMIN"]))
):
    """
    List all users in the system (Admin only).
    """
    users = await AdminService.get_all_users(db)
    if users:
        return {"items": [UserResponse.model_validate(user) for user in users], "total": len(users)}
    raise HTTPException(status_code=404, detail="No users found")

@router.delete("/users/{user_id}", status_code=204, tags=["Admin"])
async def delete_user(
    user_id: str, db: AsyncSession = Depends(get_db), current_user: dict = Depends(require_role(["ADMIN"]))
):
    """
    Delete a user by their ID (Admin only).
    """
    success = await AdminService.delete_user_by_id(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
