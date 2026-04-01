from sqlmodel import Field, Relationship, SQLModel
from typing import Optional, List, TYPE_CHECKING
from pydantic import EmailStr

if TYPE_CHECKING:
    from app.models.todo import Todo


class UserBase(SQLModel):
    username: str = Field(index=True, unique=True)
    email: EmailStr = Field(index=True, unique=True)
    password: str
    #role: str = ""
    role: str = Field(default="user", index=True)



class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    # Relationship to Todo (string reference avoids circular import)
    todos: List["Todo"] = Relationship(back_populates="user")