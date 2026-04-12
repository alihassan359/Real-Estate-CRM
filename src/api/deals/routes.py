"""
Deals Routes
"""

from fastapi import APIRouter

router = APIRouter(prefix="/deals", tags=["Deals"])


@router.post("/")
async def create_deal():
    """Create a new deal"""
    # TODO: Implement
    return {"message": "Create deal"}


@router.get("/")
async def list_deals(skip: int = 0, limit: int = 100):
    """List all deals"""
    # TODO: Implement
    return {"message": "List deals"}


@router.get("/{deal_id}")
async def get_deal(deal_id: int):
    """Get deal by id"""
    # TODO: Implement
    return {"message": f"Get deal {deal_id}"}


@router.put("/{deal_id}")
async def update_deal(deal_id: int):
    """Update deal"""
    # TODO: Implement
    return {"message": f"Update deal {deal_id}"}


@router.delete("/{deal_id}")
async def delete_deal(deal_id: int):
    """Delete deal"""
    # TODO: Implement
    return {"message": f"Delete deal {deal_id}"}
