"""
Payments Routes
"""

from fastapi import APIRouter

router = APIRouter(prefix="/payments", tags=["Payments"])


@router.post("/")
async def create_payment():
    """Create a new payment"""
    # TODO: Implement
    return {"message": "Create payment"}


@router.get("/")
async def list_payments(skip: int = 0, limit: int = 100):
    """List all payments"""
    # TODO: Implement
    return {"message": "List payments"}


@router.get("/{payment_id}")
async def get_payment(payment_id: int):
    """Get payment by id"""
    # TODO: Implement
    return {"message": f"Get payment {payment_id}"}


@router.put("/{payment_id}")
async def update_payment(payment_id: int):
    """Update payment"""
    # TODO: Implement
    return {"message": f"Update payment {payment_id}"}


@router.delete("/{payment_id}")
async def delete_payment(payment_id: int):
    """Delete payment"""
    # TODO: Implement
    return {"message": f"Delete payment {payment_id}"}
