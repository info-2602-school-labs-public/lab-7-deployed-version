# WITH CSV 
import os
import typer
import csv
from tabulate import tabulate
from sqlmodel import select

from app.database import create_db_and_tables, get_cli_session, drop_all
from app.models import User, Todo
from app.utilities.security import encrypt_password

cli = typer.Typer()


# =========================================================
# SAFE SEED FUNCTION (USED BY APP STARTUP)
# =========================================================
def seed_data():
    with get_cli_session() as db:

        # Check if already seeded
        existing = db.exec(select(User)).first()
        if existing:
            print("Data already exists. Skipping seed.")
            return

        print("Seeding users...")

        users = [
            User(username="bob", email="bob@mail.com", password=encrypt_password("bobpass"), role="user"),
            User(username="rick", email="rick@mail.com", password=encrypt_password("rickpass"), role="user"),
            User(username="sally", email="sally@mail.com", password=encrypt_password("sallypass"), role="user"),
            User(username="pam", email="pam@mail.com", password=encrypt_password("pampass"), role="admin"),
        ]

        db.add_all(users)
        db.commit()

        print("Users seeded successfully.")

        # ================= CSV TODOS =================
        print("Loading todos from CSV...")

        BASE_DIR = os.path.dirname(os.path.dirname(__file__))
        CSV_PATH = os.path.join(BASE_DIR, "todos.csv")
        print("CSV PATH:", CSV_PATH)
        print("Exists:", os.path.exists(CSV_PATH))

        try:
            with open(CSV_PATH, newline="") as file:
                reader = csv.DictReader(file)

                for row in reader:
                    todo = Todo(
                        text=row["text"],
                        done=row["done"].lower() == "true",
                        user_id=int(row["user_id"])
                    )
                    db.add(todo)

            db.commit()
            print("Todos seeded successfully.")
        except FileNotFoundError:
            print("CSV file not found at:", CSV_PATH)

        print("Seed complete")


# =========================================================
# FULL RESET (MANUAL USE ONLY)
# =========================================================
@cli.command()
def initialize():
    with get_cli_session() as db:

        print("Dropping old database...")
        drop_all()

        print("Creating tables...")
        create_db_and_tables()

    seed_data()

    print("Database Initialized")


# =========================================================
# LIST TODOS
# =========================================================
@cli.command()
def list_todos():
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
# SAFE SEED FUNCTION
# =========================================================
def seed_data():
    with get_cli_session() as db:

        existing = db.exec(select(User)).first()
        if existing:
            print("Data already exists. Skipping seed.")
            return

        print("Seeding users...")

        users = [
            User(username="bob", email="bob@mail.com", password=encrypt_password("bobpass"), role="user"),
            User(username="rick", email="rick@mail.com", password=encrypt_password("rickpass"), role="user"),
            User(username="sally", email="sally@mail.com", password=encrypt_password("sallypass"), role="user"),
            User(username="pam", email="pam@mail.com", password=encrypt_password("pampass"), role="admin"),
        ]

        db.add_all(users)
        db.commit()

        print("Users seeded")

        print("Seeding todos...")

        todos = [
            Todo(text="Buy groceries", done=False, user_id=1),
            Todo(text="Finish assignment", done=False, user_id=2),
            Todo(text="Clean room", done=True, user_id=3),
            Todo(text="Prepare presentation", done=False, user_id=1),
            Todo(text="Review code", done=True, user_id=2),
        ]

        db.add_all(todos)
        db.commit()

        print("Todos seeded")
        print("Seed complete")


# =========================================================
# FULL RESET (MANUAL ONLY)
# =========================================================
@cli.command()
def initialize():
    with get_cli_session() as db:

        print("Dropping database...")
        drop_all()

        print("Creating tables...")
        create_db_and_tables()

    seed_data()

    print("Database initialized successfully")


# =========================================================
# LIST TODOS
# =========================================================
@cli.command()
def list_todos():
    with get_cli_session() as db:
        todos = db.exec(select(Todo)).all()

        for t in todos:
            print(f"{t.id} | {t.text} | done={t.done} | user={t.user.username}")


if __name__ == "__main__":
    cli() """