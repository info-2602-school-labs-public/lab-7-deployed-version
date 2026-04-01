from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from sqlmodel import select

from app.dependencies.session import SessionDep
from app.dependencies.auth import AuthDep
from app.models import Todo
from . import router, templates


@router.get("/app", response_class=HTMLResponse)
async def user_home_view(
    request: Request,
    user: AuthDep,
    db: SessionDep
):
    # Fetch todos
    todos = db.exec(
        select(Todo).where(Todo.user_id == user.id)
    ).all()

    return templates.TemplateResponse(
        request=request,
        name="app.html",
        context={
            "request": request,
            "user": user,
            "todos": todos
        }
    )
@router.get("/user-stats", response_class=HTMLResponse)
def user_stats(
    request: Request,
    user: AuthDep,
    db: SessionDep
):

    todos = db.exec(
        select(Todo).where(Todo.user_id == user.id)
    ).all()

    done = sum(1 for t in todos if t.done)
    pending = len(todos) - done

    return templates.TemplateResponse(
        request=request,
        name="user_stats.html",
        context={
            "request": request,
            "user": user,
            "done": done,
            "pending": pending,
            "total": len(todos)
        }
    )

@router.get("/user-stats-data")
def user_stats_data(user: AuthDep, db: SessionDep):

    todos = db.exec(
        select(Todo).where(Todo.user_id == user.id)
    ).all()

    done = sum(1 for t in todos if t.done)
    pending = len(todos) - done

    return {
        "done": done,
        "pending": pending
    }
