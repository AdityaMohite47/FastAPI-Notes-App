from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse , RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from mongodb.dboperations import *
from uuid import UUID

APP = FastAPI()
APP.mount("/static", StaticFiles(directory="static"), name="static")
TEMPLATES = Jinja2Templates(directory="templates")


@APP.get("/notes", response_class=HTMLResponse)
async def main_page(request: Request):
    notes = get_notes()
    return TEMPLATES.TemplateResponse(
        "index.html",
        {
            "request": request,
            "notes": notes if notes else []
        }
    )


@APP.post("/notes/create", response_class=RedirectResponse)
async def create_note_endpoint(request: Request):
    form = await request.form()
    title = form.get("title")
    content = form.get("content")
    new_note = NoteModel(title=title, content=content)
    notes = get_notes()

    try:
        create_note(new_note)
        return RedirectResponse(url="/notes" , status_code=303)

    except Exception as e:
        print("Error creating note:", e)
        return RedirectResponse(url="/notes" , status_code=303)



@APP.post("/notes/update/{note_id}", response_class=RedirectResponse)
async def update_note_endpoint(request: Request, note_id: str):
    form = await request.form()
    updated_fields = {
        "title": form.get("title"),
        "content": form.get("content")
    }
    try:
        update_note(UUID(note_id), updated_fields)
        return RedirectResponse(url="/notes" , status_code=303)
    except Exception as e:
        print("Error updating note:", e)
        return RedirectResponse(url="/notes" , status_code=303)


@APP.post("/notes/delete/{note_id}", response_class=RedirectResponse)
async def delete_note_endpoint(request: Request, note_id: str):
    notes = get_notes()
    try:
        delete_note(UUID(note_id))
        return RedirectResponse(url="/notes" , status_code=303)

    except Exception as e:
        print("Error deleting note:", e)
        return RedirectResponse(url="/notes" , status_code=303)
