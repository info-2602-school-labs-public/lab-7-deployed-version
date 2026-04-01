from fastapi import Request, Form, status
from fastapi.responses import RedirectResponse, HTMLResponse
from sqlmodel import select
from typing import Annotated

from app.dependencies.session import SessionDep
from app.dependencies.auth import AuthDep
from app.models import Todo
from app.utilities import flash
from . import router, templates


# =========================
# TODOS PAGE (READ)
# =========================
@router.get("/app", response_class=HTMLResponse)
def user_home(
    request: Request,
    db: SessionDep,
    user: AuthDep
):
    todos = db.exec(
        select(Todo).where(Todo.user_id == user.id)
    ).all()

    return templates.TemplateResponse(
        request=request,
        name="app.html",
        context={
            "user": user,
            "todos": todos
        }
    )


# =========================
# CREATE TODO
# =========================
@router.post("/todos")
def create_todo(
    request: Request,
    text: Annotated[str, Form()],
    db: SessionDep,
    user: AuthDep
):
    todo = Todo(text=text, user_id=user.id)

    db.add(todo)
    db.commit()

    return RedirectResponse("/app", status_code=status.HTTP_303_SEE_OTHER)


# =========================
# TOGGLE TODO
# =========================
@router.post("/toggle/{id}")
def toggle_todo(
    request: Request,
    id: int,
    db: SessionDep,
    user: AuthDep
):
    todo = db.exec(
        select(Todo).where(Todo.id == id, Todo.user_id == user.id)
    ).one_or_none()

    if not todo:
        flash(request, "Todo not found or unauthorized")
        return RedirectResponse("/app", status_code=status.HTTP_303_SEE_OTHER)

    todo.done = not todo.done
    db.add(todo)
    db.commit()

    return RedirectResponse("/app", status_code=status.HTTP_303_SEE_OTHER)


# =========================
# EDIT TODO PAGE
# =========================
@router.get("/editTodo/{id}", response_class=HTMLResponse)
def edit_todo_page(request: Request, id: int, db: SessionDep, user: AuthDep):

    todo = db.exec(
        select(Todo).where(Todo.id == id, Todo.user_id == user.id)
    ).one_or_none()

    if not todo:
        return RedirectResponse("/app", status_code=303)

    return templates.TemplateResponse(
        request=request,
        name="edit.html",
        context={
            "request": request,
            "user": user,
            "todo": todo
        }
    )

# =========================
# EDIT TODO SUBMIT
# =========================
@router.post("/editTodo/{id}")
def edit_todo(request: Request, id: int, db: SessionDep, user: AuthDep, text: str = Form()):

    todo = db.exec(
        select(Todo).where(Todo.id == id, Todo.user_id == user.id)
    ).one_or_none()

    if not todo:
        flash(request, "Todo not found")
        return RedirectResponse("/app", status_code=303)

    try:
        todo.text = text
        db.add(todo)
        db.commit()
    except Exception as e:
        db.rollback()
        flash(request, "Edit failed")
        print("EDIT ERROR:", e)

    return RedirectResponse("/app", status_code=303)

# =========================
# DELETE TODO
# =========================
@router.post("/deleteTodo/{id}")
def delete_todo(request: Request, id: int, db: SessionDep, user: AuthDep):

    todo = db.exec(
        select(Todo).where(Todo.id == id, Todo.user_id == user.id)
    ).one_or_none()

    if not todo:
        flash(request, "Todo not found")
        return RedirectResponse("/app", status_code=303)

    try:
        db.delete(todo)
        db.commit()
    except Exception as e:
        db.rollback()
        flash(request, "Delete failed")
        print("DELETE ERROR:", e)

    return RedirectResponse("/app", status_code=303)