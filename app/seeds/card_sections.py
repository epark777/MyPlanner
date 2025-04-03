from app.models import db, CardSection, environment, SCHEMA
from sqlalchemy.sql import text
from datetime import datetime, timezone

def seed_card_sections():

    demo_sections = [
        # Work Tasks
        CardSection(
            title="To Do",
            board_id=1,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        ),
        CardSection(
            title="In Progress",
            board_id=1,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        ),
        CardSection(
            title="Done",
            board_id=1,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        ),
        
        # Personal Projects board
        CardSection(
            title="Ideas",
            board_id=2,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        ),
        CardSection(
            title="Planning",
            board_id=2,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        ),
        CardSection(
            title="In Progress",
            board_id=2,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        ),
        CardSection(
            title="Completed",
            board_id=2,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        ),
        
        # Study Plan board
        CardSection(
            title="Week 1",
            board_id=3,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        ),
        CardSection(
            title="Week 2",
            board_id=3,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        ),
        CardSection(
            title="Week 3",
            board_id=3,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        ),
        
        # Vacation Planning board
        CardSection(
            title="Destinations",
            board_id=4,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        ),
        CardSection(
            title="Accommodations",
            board_id=4,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        ),
        CardSection(
            title="Activities",
            board_id=4,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        ),
        
        # Home Renovation board
        CardSection(
            title="Planning",
            board_id=5,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        ),
        CardSection(
            title="Shopping",
            board_id=5,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        ),
        CardSection(
            title="In Progress",
            board_id=5,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        ),
        CardSection(
            title="Completed",
            board_id=5,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
    ]

    db.session.add_all(demo_sections)
    db.session.commit()

def undo_card_sections():

    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.card_sections RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM card_sections"))
        
    db.session.commit()