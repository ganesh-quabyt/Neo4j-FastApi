from fastapi import APIRouter, Depends
from neo4j import AsyncGraphDatabase
from app.db import get_db
from app.models.page import PageCreate, PageOut
from datetime import datetime
import uuid

router = APIRouter(prefix="/pages", tags=["Pages"])


@router.post("/", response_model=PageOut)
async def create_page(data: PageCreate, session=Depends(get_db)):
    page_id = str(uuid.uuid4())
    now = datetime.utcnow()

    query = """
    MATCH (pdf:PDF {id: $pdf_id})
    CREATE (page:Page {
        id: $id,
        page_number: $page_number,
        pdf_id: $pdf_id,
        image_path: $image_path,
        created_at: $created_at,
        updated_at: $updated_at
    })
    CREATE (pdf)-[:HAS_PAGE]->(page)
    RETURN page
    """

    params = {
        "id": page_id,
        "page_number": data.page_number,
        "pdf_id": data.pdf_id,
        "image_path": data.image_path,
        "created_at": now,
        "updated_at": now
    }

    tx = await session.begin_transaction()
    try:
        result = await tx.run(query, params)
        record = await result.single()
        node = record["page"]
        await tx.commit()
    except Exception as e:
        await tx.rollback()
        raise e

    return {
        "id": node["id"],
        "page_number": node["page_number"],
        "pdf_id": node["pdf_id"],
        "image_path": node.get("image_path"),
        "created_at": node["created_at"].to_native(),
        "updated_at": node["updated_at"].to_native(),
    }
