"""
Projects Routes
"""

from fastapi import APIRouter

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.post("/")
async def create_project():
    """Create a new project"""
    # TODO: Implement
    return {"message": "Create project"}


@router.get("/")
async def list_projects(skip: int = 0, limit: int = 100):
    """List all projects"""
    # TODO: Implement
    return {"message": "List projects"}


@router.get("/{project_id}")
async def get_project(project_id: int):
    """Get project by id"""
    # TODO: Implement
    return {"message": f"Get project {project_id}"}


@router.put("/{project_id}")
async def update_project(project_id: int):
    """Update project"""
    # TODO: Implement
    return {"message": f"Update project {project_id}"}


@router.delete("/{project_id}")
async def delete_project(project_id: int):
    """Delete project"""
    # TODO: Implement
    return {"message": f"Delete project {project_id}"}
