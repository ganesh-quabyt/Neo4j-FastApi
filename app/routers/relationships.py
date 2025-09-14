from fastapi import APIRouter, Depends
from neo4j import AsyncSession
from app.db import get_db

router = APIRouter(prefix="/relationships", tags=["Relationships"])


@router.get("/")
async def get_all_relationships(session: AsyncSession = Depends(get_db)):
    cypher = """
    MATCH (a)-[r]->(b)
    RETURN labels(a)[0] AS from_label,
           a.id AS from_id,
           type(r) AS rel_type,
           r AS rel_props,
           labels(b)[0] AS to_label,
           b.id AS to_id
    """

    result = await session.run(cypher)
    relationships = []

    async for record in result:
        rel_props = record["rel_props"]._properties
        # Convert datetime props if needed
        if "created_at" in rel_props:
            rel_props["created_at"] = rel_props["created_at"].to_native()
        if "updated_at" in rel_props:
            rel_props["updated_at"] = rel_props["updated_at"].to_native()

        relationships.append({
            "from": f"{record['from_label']}({record['from_id']})",
            "to": f"{record['to_label']}({record['to_id']})",
            "type": record["rel_type"],
            "properties": rel_props
        })

    return relationships
