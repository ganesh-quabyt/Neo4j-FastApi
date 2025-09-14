from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PageCreate(BaseModel):
    page_number: int
    pdf_id: str
    image_path: Optional[str] = None

class PageOut(BaseModel):
    id: str
    page_number: int
    pdf_id: str
    image_path: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  
