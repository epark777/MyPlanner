from app.models import db, Board, environment, SCHEMA
from sqlalchemy.sql import text
from datetime import datetime, timezone

def seed_boards():
    demo_boards = [
        Board(
            name="Work Tasks",
            user_id=1,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        ),
        Board(
            name="Personal Projects",
            user_id=1,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        ),
        Board(
            name="Study Plan",
            user_id=2,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        ),
        Board(
            name="Vacation Planning",
            user_id=2,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        ),
        Board(
            name="Home Renovation",
            user_id=3,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
    ]

    db.session.add_all(demo_boards)
    db.session.commit()

def undo_boards():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.boards RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM boards"))
        
    db.session.commit()