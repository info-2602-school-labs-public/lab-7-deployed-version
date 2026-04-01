from fastapi import Request
from fastapi.responses import HTMLResponse
from sqlmodel import select
from sqlalchemy.orm import selectinload

from app.models import Todo, User
from app.dependencies.session import SessionDep
from app.dependencies.auth import AdminDep
from app.pagination import Pagination
from . import router, templates


@router.get("/admin", response_class=HTMLResponse)
def admin_home_view(
    request: Request,
    user: AdminDep,
    db: SessionDep,
    page: int = 1,
    limit: int = 10,
    q: str = "",
    done: str = "any"
):
    # =====================
    # BASE QUERY
    # =====================
    query = select(Todo).options(selectinload(Todo.user))

    # =====================
    # SEARCH FILTER
    # =====================
    if q:
        query = query.where(Todo.text.contains(q))

    # =====================
    # DONE FILTER
    # =====================
    if done == "true":
        query = query.where(Todo.done == True)
    elif done == "false":
        query = query.where(Todo.done == False)

    # =====================
    # TOTAL COUNT (for pagination UI)
    # =====================
    total = len(db.exec(query).all())

    # =====================
    # REAL DB PAGINATION (IMPORTANT FIX)
    # =====================
    query = query.offset((page - 1) * limit).limit(limit)
    todos = db.exec(query).all()

    # =====================
    # PAGINATION OBJECT
    # =====================
    pagination = Pagination(page, limit, total)

    # =====================
    # RETURN TEMPLATE
    # =====================
    return templates.TemplateResponse(
        request=request,
        name="admin.html",
        context={
            "request": request,
            "user": user,
            "todos": todos,
            "pagination": pagination,
            "q": q,
            "done": done
        }
    )

@router.get("/admin-stats", response_class=HTMLResponse)
def admin_stats(
    request: Request,
    user: AdminDep,
    db: SessionDep
):
    from sqlmodel import select
    from app.models import Todo, User

    users = db.exec(select(User)).all()

    data = {}

    for u in users:
        count = db.exec(
            select(Todo).where(Todo.user_id == u.id)
        ).all()
        data[u.username] = len(count)

    return templates.TemplateResponse(
        request=request,
        name="admin_stats.html",
        context={
            "request": request,
            "user": user,
            "data": data
        }
    )

@router.get("/admin-stats-data")
def admin_stats_data(db: SessionDep, user: AdminDep):
    users = db.exec(select(User)).all()

    data = {}

    for u in users:
        count = db.exec(select(Todo).where(Todo.user_id == u.id)).all()
        data[u.username] = len(count)

    return data
