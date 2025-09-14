from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TableBase(BaseModel):
    table_id: str
    page_id: str
    header: Optional[str] = None
    description: Optional[str] = None

class TableCreate(TableBase):
    pass

class TableOut(TableBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
