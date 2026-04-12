"""
Receipts Routes
"""

from fastapi import APIRouter

router = APIRouter(prefix="/receipts", tags=["Receipts"])


@router.post("/")
async def create_receipt():
    """Create a new receipt"""
    # TODO: Implement
    return {"message": "Create receipt"}


@router.get("/")
async def list_receipts(skip: int = 0, limit: int = 100):
    """List all receipts"""
    # TODO: Implement
    return {"message": "List receipts"}


@router.get("/{receipt_id}")
async def get_receipt(receipt_id: int):
    """Get receipt by id"""
    # TODO: Implement
    return {"message": f"Get receipt {receipt_id}"}


@router.get("/{receipt_id}/pdf")
async def download_receipt_pdf(receipt_id: int):
    """Download receipt as PDF"""
    # TODO: Implement
    return {"message": f"Download receipt {receipt_id} as PDF"}
