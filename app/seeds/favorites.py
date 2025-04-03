from app.models import db, Favorite, environment, SCHEMA
from sqlalchemy.sql import text
from datetime import datetime, timezone

def seed_favorites():

    now = datetime.now(timezone.utc)
    
    demo_favorites = [
        # Demo user's favorites
        Favorite(
            user_id=1,
            board_id=1,
            created_at=now,
            updated_at=now
        ),
        
        Favorite(
            user_id=2,
            board_id=3,
            created_at=now,
            updated_at=now
        ),

        Favorite(
            user_id=2,
            board_id=4,
            created_at=now,
            updated_at=now
        ),
        
        Favorite(
            user_id=3,
            board_id=5,
            created_at=now,
            updated_at=now
        )
    ]

    db.session.add_all(demo_favorites)
    db.session.commit()

def undo_favorites():

    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.favorites RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM favorites"))
        
    db.session.commit()