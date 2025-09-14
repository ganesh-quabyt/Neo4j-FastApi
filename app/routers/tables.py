from fastapi import APIRouter, Depends, HTTPException
from neo4j import AsyncSession
from app.db import get_db
from app.models.table import TableCreate, TableOut
from datetime import datetime
import uuid
import logging

router = APIRouter(prefix="/tables", tags=["Tables"])
logger = logging.getLogger(__name__)

@router.post("/", response_model=TableOut)
async def create_table(data: TableCreate, session: AsyncSession = Depends(get_db)):
    table_id = str(uuid.uuid4())
    now = datetime.utcnow().isoformat()

    cypher = """
    MATCH (page:Page {id: $page_id})
    CREATE (table:Table {
        id: $id,
        table_id: $table_id,
        header: $header,
        description: $description,
        created_at: datetime($created_at),
        updated_at: datetime($updated_at)
    })
    CREATE (page)-[:HAS_TABLE]->(table)
    RETURN table
    """

    result = await session.run(cypher, {
        "id": table_id,
        "table_id": data.table_id,
        "header": data.header,
        "description": data.description,
        "page_id": data.page_id,
        "created_at": now,
        "updated_at": now
    })

    record = await result.single()

    if not record or "table" not in record:
        logger.error(f"Page with id '{data.page_id}' not found or table creation failed.")
        raise HTTPException(status_code=404, detail=f"Page with id '{data.page_id}' not found.")

    table_node = record["table"]
    properties = table_node._properties


    if "created_at" in properties:
        properties["created_at"] = properties["created_at"].to_native()
    if "updated_at" in properties:
        properties["updated_at"] = properties["updated_at"].to_native()

    return TableOut(**properties)
