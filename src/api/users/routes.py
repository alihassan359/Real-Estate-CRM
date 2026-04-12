"""
Users Routes
"""

from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/")
async def create_user():
    """Create a new user"""
    # TODO: Implement
    return {"message": "Create user"}


@router.get("/")
async def list_users(skip: int = 0, limit: int = 100):
    """List all users"""
    # TODO: Implement
    return {"message": "List users"}


@router.get("/{user_id}")
async def get_user(user_id: int):
    """Get user by id"""
    # TODO: Implement
    return {"message": f"Get user {user_id}"}


@router.put("/{user_id}")
async def update_user(user_id: int):
    """Update user"""
    # TODO: Implement
    return {"message": f"Update user {user_id}"}


@router.delete("/{user_id}")
async def delete_user(user_id: int):
    """Delete user"""
    # TODO: Implement
    return {"message": f"Delete user {user_id}"}
