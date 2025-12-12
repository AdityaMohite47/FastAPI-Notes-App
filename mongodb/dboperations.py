from mongodb.dbconn import get_mongodb_connection
import os
from uuid import UUID
from models import NoteModel
from datetime import datetime


def get_notes():
    conn = get_mongodb_connection()
    notes_collection = conn[os.getenv("NOTES_COLLECTION", "Notes")]
    notes = notes_collection.find()
    cleaned = []

    for note in notes:
        note["_id"] = UUID(note["_id"])
        cleaned.append(NoteModel(**note))

    return cleaned


def create_note(note: NoteModel):
    conn = get_mongodb_connection()
    notes_collection = conn[os.getenv("NOTES_COLLECTION", "Notes")]

    data = note.model_dump(by_alias=True)
    data["_id"] = str(data["_id"])

    notes_collection.insert_one(data)
    return True


def update_note(id: UUID, fields: dict):
    conn = get_mongodb_connection()
    notes_collection = conn[os.getenv("NOTES_COLLECTION", "Notes")]

    updated_fields = {k: v for k, v in fields.items() if v is not None}
    updated_fields["updated_at"] = datetime.utcnow()

    result = notes_collection.update_one(
        {"_id": str(id)},               
        {"$set": updated_fields}   
    )
    return result.modified_count > 0


def delete_note(id: UUID):
    conn = get_mongodb_connection()
    notes_collection = conn[os.getenv("NOTES_COLLECTION", "Notes")]

    result = notes_collection.delete_one({"_id": str(id)})
    return result.deleted_count > 0