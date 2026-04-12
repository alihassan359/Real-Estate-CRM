"""
Clients Routes
"""

from fastapi import APIRouter

router = APIRouter(prefix="/clients", tags=["Clients"])


@router.post("/")
async def create_client():
    """Create a new client"""
    # TODO: Implement
    return {"message": "Create client"}


@router.get("/")
async def list_clients(skip: int = 0, limit: int = 100):
    """List all clients"""
    # TODO: Implement
    return {"message": "List clients"}


@router.get("/{client_id}")
async def get_client(client_id: int):
    """Get client by id"""
    # TODO: Implement
    return {"message": f"Get client {client_id}"}


@router.put("/{client_id}")
async def update_client(client_id: int):
    """Update client"""
    # TODO: Implement
    return {"message": f"Update client {client_id}"}


@router.delete("/{client_id}")
async def delete_client(client_id: int):
    """Delete client"""
    # TODO: Implement
    return {"message": f"Delete client {client_id}"}
