from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.models import Board, CardSection, db
from app.forms import BoardForm, CardSectionForm

# Create a new blueprint with a different name
board_controller = Blueprint("boards", __name__)


# Helper function to verify board ownership
def verify_board_access(board_id):
    """
    Validates board existence and user access rights
    Returns tuple (board_object, error_response)
    """
    try:
        # Find board by ID
        board = Board.query.get(board_id)

        # Check if board exists
        if not board:
            return None, ({"error": "No board found with the specified ID"}, 404)

        # Check ownership
        if board.user_id != current_user.id:
            return None, ({"error": "Access denied: You don't own this board"}, 403)

        # Board exists and user has access
        return board, None

    except Exception as e:
        return None, ({"error": f"Server error: {str(e)}"}, 500)


# Board Management Routes
@board_controller.route("/mine")
@login_required
def list_user_boards():
    """Retrieve all boards belonging to the current user"""
    # Query the database for user's boards
    user_boards = Board.query.filter(Board.user_id == current_user.id).all()

    # Format the response
    response = {
        "count": len(user_boards),
        "results": [board.to_dict_basic() for board in user_boards],
    }

    return response


@board_controller.route("/view/<int:board_id>")
@login_required
def retrieve_board_details(board_id):
    """Get complete details for a specific board"""
    # Check board access
    board, error = verify_board_access(board_id)
    if error:
        return error

    # Return detailed board information
    return board.to_dict_detail()


@board_controller.route("/create", methods=["POST"])
@login_required
def establish_new_board():
    """Create a new board for the current user"""
    # Process form data
    form = BoardForm()
    form["csrf_token"].data = request.cookies["csrf_token"]

    # Validate form data
    if not form.validate_on_submit():
        return {"validation_errors": form.errors}, 400

    # Create new board
    board = Board(name=form.data["name"], user_id=current_user.id)

    # Save to database
    db.session.add(board)
    db.session.commit()

    # Return the new board with 201 Created status
    return {
        "message": "Board created successfully",
        "board": board.to_dict_basic(),
    }, 201


@board_controller.route("/update/<int:board_id>", methods=["PUT"])
@login_required
def modify_board(board_id):
    """Update an existing board's properties"""
    # Check board access
    board, error = verify_board_access(board_id)
    if error:
        return error

    # Process form data
    form = BoardForm()
    form["csrf_token"].data = request.cookies["csrf_token"]

    # Update board if form is valid
    if form.validate_on_submit():
        board.name = form.data["name"]
        db.session.commit()
        return {"message": "Board updated successfully", "board": board.to_dict_basic()}

    # Return validation errors
    return {"validation_errors": form.errors}, 400


@board_controller.route("/delete/<int:board_id>", methods=["DELETE"])
@login_required
def remove_board(board_id):
    """Remove a board and all associated data"""
    # Check board access
    board, error = verify_board_access(board_id)
    if error:
        return error

    # Delete the board
    db.session.delete(board)
    db.session.commit()

    # Return success message
    return {"message": "Board and all associated data deleted successfully"}


# Section Management Routes
@board_controller.route("/<int:board_id>/sections")
@login_required
def list_board_sections(board_id):
    """List all sections in a board"""
    # Check board access
    board, error = verify_board_access(board_id)
    if error:
        return error

    # Return sections
    return {
        "board_name": board.name,
        "section_count": len(board.card_sections),
        "sections": board.to_dict_detail()["CardSections"],
    }


@board_controller.route("/<int:board_id>/sections/add", methods=["POST"])
@login_required
def add_board_section(board_id):
    """Add a new section to a board"""
    # Check board access
    board, error = verify_board_access(board_id)
    if error:
        return error

    # Process form data
    form = CardSectionForm()
    form["csrf_token"].data = request.cookies["csrf_token"]

    # Create section if form is valid
    if form.validate_on_submit():
        section = CardSection(board_id=board.id, title=form.data["title"])

        # Save to database
        db.session.add(section)
        db.session.commit()

        return {
            "message": "Section added successfully",
            "section": section.to_dict_basic(),
        }

    # Return validation errors
    return {"validation_errors": form.errors}, 400
