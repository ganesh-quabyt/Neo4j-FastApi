from fastapi import APIRouter, Depends
from neo4j import AsyncSession
from app.db import get_db
from app.models.pdf import PDFCreate, PDFOut
from datetime import datetime
import uuid

router = APIRouter(prefix="/pdfs", tags=["PDFs"])

# Utility function to map Neo4j node to PDFOut
def map_pdf_props_to_output(props: dict, project_id: str | None = None) -> PDFOut:
    return PDFOut(
        id=props["id"],
        filename=props["name"],
        file_path=props.get("path"),
        project_id=project_id or props.get("project_id"),
        page_count=props["page_count"],
        created_at=props["created_at"].to_native(),
        updated_at=props["updated_at"].to_native(),
    )

@router.post("/", response_model=PDFOut)
async def create_pdf(data: PDFCreate, session: AsyncSession = Depends(get_db)):
    pdf_id = str(uuid.uuid4())
    now = datetime.utcnow().isoformat()

    query = """
    MATCH (p:Project {id: $project_id})
    CREATE (pdf:PDF {
        id: $id,
        name: $name,
        path: $path,
        page_count: $page_count,
        size: $size,
        created_at: datetime($created_at),
        updated_at: datetime($updated_at)
    })
    CREATE (p)-[:HAS_PDF]->(pdf)
    RETURN pdf
    """

    result = await session.run(query, {
        "id": pdf_id,
        "name": data.name,
        "path": data.path,
        "page_count": data.page_count,
        "size": data.size,
        "created_at": now,
        "updated_at": now,
        "project_id": data.project_id
    })

    record = await result.single()
    node = record["pdf"]
    props = node._properties

    return map_pdf_props_to_output(props, project_id=data.project_id)

@router.get("/", response_model=list[PDFOut])
async def get_pdfs(session: AsyncSession = Depends(get_db)):
    query = """
    MATCH (p:Project)-[:HAS_PDF]->(pdf:PDF)
    RETURN pdf, p.id AS project_id
    ORDER BY pdf.created_at DESC
    """
    result = await session.run(query)
    records = [record async for record in result]

    pdfs = []
    for r in records:
        props = r["pdf"]._properties
        project_id = r.get("project_id")
        pdfs.append(map_pdf_props_to_output(props, project_id=project_id))

    return pdfs
