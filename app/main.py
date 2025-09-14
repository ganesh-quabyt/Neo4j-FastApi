from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import projects, pdfs, pages, tables,relationships

app = FastAPI(title="PDF Table Extraction Graph API")

# Allow all CORS for dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Route registration
app.include_router(projects.router, prefix="/projects", tags=["Projects"])
app.include_router(pdfs.router, prefix="/pdfs", tags=["PDFs"])
app.include_router(pages.router, prefix="/pages", tags=["Pages"])
app.include_router(tables.router, prefix="/tables", tags=["Tables"])
app.include_router(relationships.router,prefix="/relationships",tags=["Relations"])

