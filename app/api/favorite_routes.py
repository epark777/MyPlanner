from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.models import Favorite, Board, db
from sqlalchemy import and_

# Initialize blueprint with a different name
favorites_api = Blueprint('favorites', __name__)


@favorites_api.route('/list')
@login_required
def retrieve_all_favorites():
    """
    Retrieve all favorited boards for the authenticated user
    Returns a list of board data through the favorites relationship
    """
    # Query all favorites for the current user
    user_favorites = Favorite.query.filter(
        Favorite.user_id == current_user.id
    ).all()
    
    # Transform to dictionary representation
    favorite_data = [favorite.to_dict_board() for favorite in user_favorites]
    
    return jsonify(favorite_data)


@favorites_api.route('/add', methods=['POST'])
@login_required
def add_favorite():
    """
    Add a board to user's favorites
    Requires board_id in the request JSON
    """
    # Extract board ID from request
    request_data = request.get_json()
    target_board_id = request_data.get('board_id')
    
    # Validate board exists
    target_board = Board.query.get(target_board_id)
    if not target_board:
        return {"error": "Board not found"}, 404
    
    # Verify user has access to board
    if target_board.user_id != current_user.id:
        return {"error": "You don't have permission to favorite this board"}, 403
    
    # Check if already favorited
    existing_favorite = Favorite.query.filter(
        and_(
            Favorite.board_id == target_board_id,
            Favorite.user_id == current_user.id
        )
    ).first()
    
    if existing_favorite:
        return {"error": "Board is already in your favorites"}, 409
    
    # Create new favorite
    favorite = Favorite(
        user_id=current_user.id,
        board_id=target_board_id
    )
    
    # Save to database
    db.session.add(favorite)
    db.session.commit()
    
    return favorite.to_dict_board(), 201


@favorites_api.route('/remove/<int:favorite_id>', methods=['DELETE'])
@login_required
def remove_favorite(favorite_id):
    """
    Remove a favorite from user's collection
    """
    # Find the favorite
    favorite = Favorite.query.get(favorite_id)
    
    # Validate favorite exists
    if not favorite:
        return {"error": "Favorite not found"}, 404
    
    # Verify ownership
    if favorite.user_id != current_user.id:
        return {"error": "You don't have permission to remove this favorite"}, 403
    
    # Remove favorite
    db.session.delete(favorite)
    db.session.commit()
    
    return {"status": "Favorite successfully removed"}