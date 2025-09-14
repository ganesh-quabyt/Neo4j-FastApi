from fastapi import APIRouter, Depends, HTTPException
from neo4j import AsyncSession
from app.db import get_db
from app.models.project import ProjectCreate, ProjectOut
from datetime import datetime
from typing import List
import uuid

router = APIRouter(prefix="/projects", tags=["Projects"])

@router.post("/", response_model=ProjectOut)
async def create_project(data: ProjectCreate, session: AsyncSession = Depends(get_db)):
    project_id = str(uuid.uuid4())
    now = datetime.utcnow()

    query = """
    CREATE (p:Project {
        id: $id,
        name: $name,
        description: $description,
        created_at: datetime($created_at),
        updated_at: datetime($updated_at)
    })
    RETURN p
    """

    result = await session.run(query, {
        "id": project_id,
        "name": data.name,
        "description": data.description,
        "created_at": now.isoformat(),
        "updated_at": now.isoformat(),
    })

    record = await result.single()
    p = record["p"]

    return {
        "id": str(p["id"]),
        "name": p["name"],
        "description": p["description"],
        "created_at": p["created_at"].to_native(),
        "updated_at": p["updated_at"].to_native(),
    }


@router.get("/", response_model=List[ProjectOut])
async def get_all_projects(session: AsyncSession = Depends(get_db)):
    query = "MATCH (p:Project) RETURN p"
    result = await session.run(query)
    records = await result.data()

    projects = []
    for record in records:
        p = record["p"]
        projects.append({
            "id": str(p["id"]),
            "name": p["name"],
            "description": p.get("description"),
            "created_at": p["created_at"].to_native(),
            "updated_at": p["updated_at"].to_native(),
        })

    return projects


@router.get("/{project_id}", response_model=ProjectOut)
async def get_project(project_id: str, session: AsyncSession = Depends(get_db)):
    query = "MATCH (p:Project {id: $id}) RETURN p"
    result = await session.run(query, {"id": project_id})
    record = await result.single()

    if record is None:
        raise HTTPException(status_code=404, detail="Project not found")

    p = record["p"]
    return {
        "id": str(p["id"]),
        "name": p["name"],
        "description": p.get("description"),
        "created_at": p["created_at"].to_native(),
        "updated_at": p["updated_at"].to_native(),
    }
