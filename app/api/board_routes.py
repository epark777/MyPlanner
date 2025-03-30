from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.models import Board, CardSection, db
from app.forms import BoardForm, CardSectionForm
from sqlalchemy.exc import SQLAlchemyError

board_api = Blueprint("boards", __name__)


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
            return None, ({"error": "Not Found", "message": "Board not found"}, 404)

        # Check ownership
        if board.user_id != current_user.id:
            return None, ({"error": "Forbidden", "message": "You don't have permission to access this board"}, 403)

        # Board exists and user has access
        return board, None

    except Exception as e:
        return None, ({"error": "Server Error", "message": str(e)}, 500)


@board_api.route("")
@login_required
def get_user_boards():
    """Retrieve all boards belonging to the current user"""
    # Query the database for user's boards
    user_boards = Board.query.filter(Board.user_id == current_user.id).all()

    # Format response
    response = {
        "count": len(user_boards),
        "boards": [board.to_dict_basic() for board in user_boards],
    }

    return jsonify(response)


@board_api.route("/<int:board_id>")
@login_required
def get_board(board_id):
    """Get complete details for a specific board"""
    # Check board access
    board, error = verify_board_access(board_id)
    if error:
        return jsonify(error[0]), error[1]

    # Return detailed board information
    return jsonify(board.to_dict_detail())


@board_api.route("", methods=["POST"])
@login_required
def create_board():
    """Create a new board for the current user"""
    # Process form data
    form = BoardForm()
    form["csrf_token"].data = request.cookies["csrf_token"]

    # Validate form data
    if not form.validate_on_submit():
        return jsonify({"error": "Validation failed", "details": form.errors}), 400

    try:
        # Create new board
        board = Board(name=form.data["name"], user_id=current_user.id)

        # Save to database
        db.session.add(board)
        db.session.commit()

        # Return the new board 201 status
        return jsonify({
            "message": "Board created successfully",
            "board": board.to_dict_basic(),
        }), 201
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"error": "Database error", "message": "Failed to create board"}), 500


@board_api.route("/<int:board_id>", methods=["PUT"])
@login_required
def update_board(board_id):
    """Update an existing board's properties"""
    # Check board access
    board, error = verify_board_access(board_id)
    if error:
        return jsonify(error[0]), error[1]

    # Process form data
    form = BoardForm()
    form["csrf_token"].data = request.cookies["csrf_token"]

    # Update board if form is valid
    if form.validate_on_submit():
        try:
            board.name = form.data["name"]
            db.session.commit()
            return jsonify({"message": "Board updated successfully", "board": board.to_dict_basic()})
        except SQLAlchemyError:
            db.session.rollback()
            return jsonify({"error": "Database error", "message": "Failed to update board"}), 500

    # Return validation errors
    return jsonify({"error": "Validation failed", "details": form.errors}), 400


@board_api.route("/<int:board_id>", methods=["DELETE"])
@login_required
def delete_board(board_id):
    """Remove a board and all associated data"""
    # Check board access
    board, error = verify_board_access(board_id)
    if error:
        return jsonify(error[0]), error[1]

    try:
        # Delete the board (cascade will handle related entities)
        db.session.delete(board)
        db.session.commit()

        # Return success message
        return jsonify({"message": "Board and all associated data deleted successfully"})
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"error": "Database error", "message": "Failed to delete board"}), 500


# Section Management Routes
@board_api.route("/<int:board_id>/sections")
@login_required
def get_board_sections(board_id):
    """List all sections in a board"""
    # Check board access
    board, error = verify_board_access(board_id)
    if error:
        return jsonify(error[0]), error[1]

    # Return sections
    return jsonify({
        "board_name": board.name,
        "section_count": len(board.card_sections),
        "sections": board.to_dict_detail()["CardSections"],
    })


@board_api.route("/<int:board_id>/sections", methods=["POST"])
@login_required
def add_board_section(board_id):
    """Add a new section to a board"""
    # Check board access
    board, error = verify_board_access(board_id)
    if error:
        return jsonify(error[0]), error[1]

    # Process form data
    form = CardSectionForm()
    form["csrf_token"].data = request.cookies["csrf_token"]

    # Create section if form is valid
    if form.validate_on_submit():
        try:
            section = CardSection(board_id=board.id, title=form.data["title"])

            # Save to database
            db.session.add(section)
            db.session.commit()

            return jsonify({
                "message": "Section added successfully",
                "section": section.to_dict_basic(),
            })
        except SQLAlchemyError:
            db.session.rollback()
            return jsonify({"error": "Database error", "message": "Failed to create section"}), 500

    # Return validation errors
    return jsonify({"error": "Validation failed", "details": form.errors}), 400