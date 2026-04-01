# WITH CSV 

import typer
import csv
from tabulate import tabulate
from sqlmodel import select

from app.database import create_db_and_tables, get_cli_session, drop_all
from app.models import User, Todo
from app.utilities.security import encrypt_password

cli = typer.Typer()


# =========================================================
# INITIALIZE DATABASE + SEED DATA
# =========================================================
@cli.command()
def initialize():
    #Drop DB, recreate tables, and seed initial data.

    with get_cli_session() as db:

        print("Dropping old database...")
        drop_all()

        print("Creating tables...")
        create_db_and_tables()

        # =====================================================
        # USERS (SEED DATA)
        # =====================================================
        users = [
            User(
                username="bob",
                email="bob@mail.com",
                password=encrypt_password("bobpass"),
                role="user"
            ),
            User(
                username="rick",
                email="rick@mail.com",
                password=encrypt_password("rickpass"),
                role="user"
            ),
            User(
                username="sally",
                email="sally@mail.com",
                password=encrypt_password("sallypass"),
                role="user"
            ),
            User(
                username="pam",
                email="pam@mail.com",
                password=encrypt_password("pampass"),
                role="admin"
            ),
        ]

        db.add_all(users)
        db.commit()

        print("Users seeded successfully.")

        # =====================================================
        # TODOS (FROM CSV)
        # =====================================================
        print("Loading todos from CSV...")

        with open("todos.csv", newline="") as file:
            reader = csv.DictReader(file)

            for row in reader:
                todo = Todo(
                    text=row["text"],
                    done=True if row["done"].lower() == "true" else False,
                    user_id=int(row["user_id"])
                )
                db.add(todo)

        db.commit()

        print("Todos seeded successfully.")
        print("Database Initialized ✔")


# =========================================================
# LIST TODOS (DEBUG / ADMIN TOOL)
# =========================================================
@cli.command()
def list_todos():
    #Print all todos in a table format.

    with get_cli_session() as db:
        todos = db.exec(select(Todo)).all()

        data = []
        for todo in todos:
            data.append([
                todo.text,
                todo.done,
                todo.user.username if todo.user else "Unknown"
            ])

        print(tabulate(data, headers=["Text", "Done", "User"]))


# =========================================================
# RUN CLI
# =========================================================
if __name__ == "__main__":
    cli() 





# WITHOUT CSV (UNCOMMENT TO USE)

""" import typer
from sqlmodel import select

from app.database import create_db_and_tables, get_cli_session, drop_all
from app.models import User, Todo
from app.utilities.security import encrypt_password

cli = typer.Typer()


# =========================================================
# INITIALIZE DATABASE (FULL RESET + SEED)
# =========================================================
@cli.command()
def initialize():
    # Reset DB and seed users + todos.

    with get_cli_session() as db:

        print("Dropping database...")
        drop_all()

        print("Creating tables...")
        create_db_and_tables()

        # =====================================================
        # USERS SEED
        # =====================================================
        users = [
            User(
                username="bob",
                email="bob@mail.com",
                password=encrypt_password("bobpass"),
                role="user"
            ),
            User(
                username="rick",
                email="rick@mail.com",
                password=encrypt_password("rickpass"),
                role="user"
            ),
            User(
                username="sally",
                email="sally@mail.com",
                password=encrypt_password("sallypass"),
                role="user"
            ),
            User(
                username="pam",
                email="pam@mail.com",
                password=encrypt_password("pampass"),
                role="admin"
            ),
        ]

        db.add_all(users)
        db.commit()

        print("Users seeded ✔")

        # =====================================================
        # TODOS SEED (MANUAL DATA)
        # =====================================================
        todos = [
            Todo(text="Buy groceries", done=False, user_id=1),
            Todo(text="Finish assignment", done=False, user_id=2),
            Todo(text="Clean room", done=True, user_id=3),
            Todo(text="Prepare presentation", done=False, user_id=1),
            Todo(text="Review code", done=True, user_id=2),
        ]

        db.add_all(todos)
        db.commit()

        print("Todos seeded ✔")
        print("Database initialized successfully ✔")


# =========================================================
# LIST TODOS
# =========================================================
@cli.command()
def list_todos():
    with get_cli_session() as db:
        todos = db.exec(select(Todo)).all()

        for t in todos:
            print(f"{t.id} | {t.text} | done={t.done} | user={t.user.username}")


# =========================================================
# RUN CLI
# =========================================================
if __name__ == "__main__":
    cli()
 """