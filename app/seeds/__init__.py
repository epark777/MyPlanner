from flask.cli import AppGroup
from .users import seed_users, undo_users
from .boards import seed_boards, undo_boards
from .card_sections import seed_card_sections, undo_card_sections
from .cards import seed_cards, undo_cards
from .favorites import seed_favorites, undo_favorites

from app.models.db import db, environment, SCHEMA

# Creates a seed group to hold our commands
# So we can type `flask seed --help`
seed_commands = AppGroup('seed')


# Creates the `flask seed all` command
@seed_commands.command('all')
def seed():
    if environment == 'production':
        # Before seeding in production, you want to run the seed undo 
        # command, which will truncate all tables prefixed with 
        # the schema name (see comment in users.py undo_users function).
        undo_favorites()
        undo_cards()
        undo_card_sections()
        undo_boards()
        undo_users()
    
    # Add seed functions here
    seed_users()
    seed_boards()
    seed_card_sections()
    seed_cards()
    seed_favorites()
    # Add other seed functions here


# Creates the `flask seed undo` command
@seed_commands.command('undo')
def undo():
    # Add undo functions here
    undo_favorites()
    undo_cards()
    undo_card_sections()
    undo_boards()
    undo_users()