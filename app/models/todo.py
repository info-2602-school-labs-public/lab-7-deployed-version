from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List
from . import User

# -----------------------
# LINK TABLE (MANY-TO-MANY)
# -----------------------
class TodoCategory(SQLModel, table=True):
    category_id: int = Field(foreign_key="category.id", primary_key=True)
    todo_id: int = Field(foreign_key="todo.id", primary_key=True)


# -----------------------
# CATEGORY MODEL
# -----------------------
class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    text: str

    todos: List["Todo"] = Relationship(
        back_populates="categories",
        link_model=TodoCategory
    )


# -----------------------
# TODO CREATE SCHEMA
# -----------------------
class TodoCreate(SQLModel):
    text: str


# -----------------------
# TODO UPDATE SCHEMA
# -----------------------
class TodoUpdate(SQLModel):
    text: Optional[str] = None
    done: Optional[bool] = None


# -----------------------
# TODO RESPONSE SCHEMA
# -----------------------
class TodoResponse(SQLModel):
    id: int
    text: str
    done: bool


# -----------------------
# TODO TABLE
# -----------------------
class Todo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    user_id: int = Field(foreign_key="user.id")

    text: str
    done: bool = False

    # Relationships (string refs prevent circular imports)
    user: "User" = Relationship(back_populates="todos")

    categories: List["Category"] = Relationship(
        back_populates="todos",
        link_model=TodoCategory
    )

    # Helper methods
    def toggle(self):
        self.done = not self.done

    def get_cat_list(self):
        return ", ".join([c.text for c in self.categories])