from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PDFBase(BaseModel):
    name: str
    path: Optional[str] = None
    page_count: int
    size: str
    project_id: str

class PDFCreate(PDFBase):
    pass

class PDFOut(BaseModel):
    id: str
    filename: str
    page_count: int
    file_path: Optional[str] = None
    project_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 
