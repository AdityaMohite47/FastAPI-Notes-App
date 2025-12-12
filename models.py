from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from datetime import datetime

class NoteModel(BaseModel):
    id: UUID = Field(default_factory=uuid4, alias="_id")
    title: str
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True        # allow using id and _id interchangeably
        arbitrary_types_allowed = True