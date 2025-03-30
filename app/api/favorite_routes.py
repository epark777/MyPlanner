from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.models import Favorite, Board, db
from sqlalchemy import and_
from sqlalchemy.exc import SQLAlchemyError

# Initialize blueprint
favorites_api = Blueprint("favorites", __name__)


@favorites_api.route("")
@login_required
def get_favorites():
    """
    Retrieve all favorite boards for the authenticated user
    Returns a list of board data through the favorites relationship
    """
    # Query all favorites for the current user
    user_favorites = Favorite.query.filter(Favorite.user_id == current_user.id).all()

    # Transform to dictionary representation
    favorite_data = [favorite.to_dict_board() for favorite in user_favorites]

    return jsonify(favorite_data)


@favorites_api.route("", methods=["POST"])
@login_required
def add_favorite():
    """
    Add a board to user's favorites
    Requires board_id in the request JSON
    """
    # Extract board ID from request
    request_data = request.get_json()

    # Ensure CSRF token is present
    if "csrf_token" not in request.cookies:
        return jsonify({"error": "CSRF token missing"}), 400

    target_board_id = request_data.get("board_id")

    # Validate input
    if not target_board_id:
        return jsonify({"error": "Bad Request", "message": "board_id is required"}), 400

    # Validate board exists
    target_board = Board.query.get(target_board_id)
    if not target_board:
        return jsonify({"error": "Not Found", "message": "Board not found"}), 404

    # Verify user has access to board
    if target_board.user_id != current_user.id:
        return (
            jsonify(
                {
                    "error": "Forbidden",
                    "message": "You don't have permission to favorite this board",
                }
            ),
            403,
        )

    # Check if favorite already
    existing_favorite = Favorite.query.filter(
        and_(Favorite.board_id == target_board_id, Favorite.user_id == current_user.id)
    ).first()

    if existing_favorite:
        return (
            jsonify(
                {"error": "Conflict", "message": "Board is already in your favorites"}
            ),
            409,
        )

    try:
        # Create new favorite
        favorite = Favorite(user_id=current_user.id, board_id=target_board_id)

        # Save to database
        db.session.add(favorite)
        db.session.commit()

        return jsonify(favorite.to_dict_board()), 201
    except SQLAlchemyError:
        db.session.rollback()
        return (
            jsonify({"error": "Database error", "message": "Failed to add favorite"}),
            500,
        )


@favorites_api.route("/<int:favorite_id>", methods=["DELETE"])
@login_required
def remove_favorite(favorite_id):
    """
    Remove a favorite from user's collection
    """
    # Ensure CSRF token is present
    if "csrf_token" not in request.cookies:
        return jsonify({"error": "CSRF token missing"}), 400

    # Find the favorite
    favorite = Favorite.query.get(favorite_id)

    # Validate favorite exists
    if not favorite:
        return jsonify({"error": "Not Found", "message": "Favorite not found"}), 404

    # Verify ownership
    if favorite.user_id != current_user.id:
        return (
            jsonify(
                {
                    "error": "Forbidden",
                    "message": "You don't have permission to remove this favorite",
                }
            ),
            403,
        )

    try:
        # Remove favorite
        db.session.delete(favorite)
        db.session.commit()

        return jsonify({"message": "Favorite successfully removed"})
    except SQLAlchemyError:
        db.session.rollback()
        return (
            jsonify(
                {"error": "Database error", "message": "Failed to remove favorite"}
            ),
            500,
        )
