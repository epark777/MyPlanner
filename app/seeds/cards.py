from app.models import db, Card, environment, SCHEMA
from sqlalchemy.sql import text
from datetime import datetime, timezone, timedelta

def seed_cards():

    now = datetime.now(timezone.utc)
    
    demo_cards = [
        # Work Tasks board - To Do section
        Card(
            name="Write project proposal",
            description="Create a detailed proposal for the new client project including scope, timeline, and resource requirements.",
            labels="High Priority, Documentation",
            due_date=now + timedelta(days=5),
            order=0,
            card_section_id=1,
            created_at=now,
            updated_at=now
        ),
        Card(
            name="Schedule team meeting",
            description="Set up a team meeting to discuss quarterly goals and upcoming projects.",
            labels="Low Priority",
            due_date=now + timedelta(days=2),
            order=1,
            card_section_id=1,
            created_at=now,
            updated_at=now
        ),
        Card(
            name="Review budget reports",
            description="Go through Q1 budget reports and prepare summary for management.",
            labels="Finance, Medium Priority",
            due_date=now + timedelta(days=7),
            order=2,
            card_section_id=1,
            created_at=now,
            updated_at=now
        ),
        
        # Work Tasks board - In Progress section
        Card(
            name="Client presentation",
            description="Prepare slides for next week's client presentation.",
            labels="High Priority, Client",
            due_date=now + timedelta(days=3),
            order=0,
            card_section_id=2,
            created_at=now,
            updated_at=now
        ),
        Card(
            name="Onboarding materials",
            description="Update onboarding documents for new team members.",
            labels="HR, Documentation",
            due_date=now + timedelta(days=10),
            order=1,
            card_section_id=2,
            created_at=now,
            updated_at=now
        ),
        
        #  Work Tasks board - Done section
        Card(
            name="Weekly report",
            description="Complete and submit weekly progress report to management.",
            labels="Recurring, Documentation",
            due_date=now - timedelta(days=1),
            order=0,
            card_section_id=3,
            created_at=now - timedelta(days=2),
            updated_at=now - timedelta(days=1)
        ),
        
        # Personal Projects board - Ideas section
        Card(
            name="Learn photography",
            description="Research beginner photography courses and equipment needed.",
            labels="Hobby, Learning",
            due_date=None,
            order=0,
            card_section_id=4,
            created_at=now,
            updated_at=now
        ),
        Card(
            name="Write a novel",
            description="Brainstorm plot ideas and character concepts for a sci-fi novel.",
            labels="Creative, Long-term",
            due_date=None,
            order=1,
            card_section_id=4,
            created_at=now,
            updated_at=now
        ),
        
        # Personal Projects board - Planning section
        Card(
            name="Build a website",
            description="Plan structure and content for a personal portfolio website.",
            labels="Tech, Medium Priority",
            due_date=now + timedelta(days=14),
            order=0,
            card_section_id=5,
            created_at=now,
            updated_at=now
        ),
        
        # Personal Projects board - In Progress section
        Card(
            name="Home workout routine",
            description="Develop and test a 30-minute home workout routine.",
            labels="Health, Recurring",
            due_date=now + timedelta(days=7),
            order=0,
            card_section_id=6,
            created_at=now - timedelta(days=5),
            updated_at=now
        ),
        
        # Study Plan board - Week 1 section
        Card(
            name="Python basics review",
            description="Go through Python basics: data types, control flow, functions.",
            labels="Programming, Fundamentals",
            due_date=now + timedelta(days=2),
            order=0,
            card_section_id=8,
            created_at=now,
            updated_at=now
        ),
        Card(
            name="Data structures practice",
            description="Solve 5 array and linked list problems from practice set.",
            labels="Algorithms, Practice",
            due_date=now + timedelta(days=4),
            order=1,
            card_section_id=8,
            created_at=now,
            updated_at=now
        ),
        
        # Vacation Planning board - Destinations section
        Card(
            name="Research Japan",
            description="Look into potential cities to visit in Japan, costs, and best times to travel.",
            labels="Research, International",
            due_date=now + timedelta(days=14),
            order=0,
            card_section_id=11,
            created_at=now,
            updated_at=now
        ),
        Card(
            name="National Parks options",
            description="Compare different national parks for a summer road trip.",
            labels="Research, Domestic",
            due_date=now + timedelta(days=10),
            order=1,
            card_section_id=11,
            created_at=now,
            updated_at=now
        ),
        
        # Home Renovation board - Planning section
        Card(
            name="Kitchen remodel ideas",
            description="Collect inspiration and ideas for kitchen renovation.",
            labels="Design, High Priority",
            due_date=None,
            order=0,
            card_section_id=14,
            created_at=now,
            updated_at=now
        ),
        Card(
            name="Contractor quotes",
            description="Contact three contractors for quotes on bathroom renovation.",
            labels="Budget, High Priority",
            due_date=now + timedelta(days=7),
            order=1,
            card_section_id=14,
            created_at=now,
            updated_at=now
        ),
        
        # Home Renovation board - Shopping section
        Card(
            name="Paint samples",
            description="Pick up paint samples for living room from Home Depot.",
            labels="Materials, Low Priority",
            due_date=now + timedelta(days=3),
            order=0,
            card_section_id=15,
            created_at=now,
            updated_at=now
        )
    ]

    db.session.add_all(demo_cards)
    db.session.commit()

def undo_cards():

    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.cards RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM cards"))
        
    db.session.commit()