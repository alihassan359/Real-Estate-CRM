"""
Notifications Routes
"""

from fastapi import APIRouter

router = APIRouter(prefix="/notifications", tags=["Notifications"])


@router.get("/")
async def list_notifications(skip: int = 0, limit: int = 100):
    """List notifications"""
    # TODO: Implement
    return {"message": "List notifications"}


@router.post("/{notification_id}/read")
async def mark_notification_read(notification_id: int):
    """Mark notification as read"""
    # TODO: Implement
    return {"message": f"Marked notification {notification_id} as read"}


@router.post("/read-all")
async def mark_all_as_read():
    """Mark all notifications as read"""
    # TODO: Implement
    return {"message": "Marked all notifications as read"}


@router.delete("/{notification_id}")
async def delete_notification(notification_id: int):
    """Delete notification"""
    # TODO: Implement
    return {"message": f"Deleted notification {notification_id}"}
