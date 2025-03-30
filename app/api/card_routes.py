from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.models import Card, db
from app.forms import CardForm
from sqlalchemy.exc import SQLAlchemyError


# Initialize Blueprint
cards_api = Blueprint("cards", __name__)


def verify_card_ownership(card_instance, user_id):
    """Helper function to verify card ownership"""
    if not card_instance:
        return {"error": "Card not found", "status": 404}

    if card_instance.to_dict_basic()["userId"] != user_id:
        return {"error": "Forbidden - You do not own this card", "status": 403}

    return None


@cards_api.route("/<int:card_id>", methods=["PUT"])
@login_required
def update_card(card_id):
    """Update a card if the current user is the owner"""

    # Find card by ID
    target_card = Card.query.get(card_id)

    # Check if card exists and belongs to user
    ownership_check = verify_card_ownership(target_card, current_user.id)
    if ownership_check:
        return ownership_check["error"], ownership_check["status"]

    # Process the form data
    card_form = CardForm()
    card_form["csrf_token"].data = request.cookies["csrf_token"]

    if card_form.validate_on_submit():
        try:
            # Update card fields
            form_data = card_form.data
            target_card.name = form_data["name"]
            target_card.description = form_data["description"]
            target_card.labels = form_data["labels"]
            target_card.due_date = form_data["due_date"]

            # Save changes
            db.session.commit()
            return jsonify(target_card.to_dict_basic())
        except SQLAlchemyError:
            db.session.rollback()
            return jsonify({"error": "Database error", "message": "Failed to update card"}), 500

    # Form validation failed
    return jsonify({"error": "Validation failed", "details": card_form.errors}), 400


@cards_api.route("/<int:card_id>", methods=["DELETE"])
@login_required
def remove_card(card_id):
    """Remove a card if the current user is the owner"""

    # Find the card by ID
    target_card = Card.query.get(card_id)

    # Check if card exists and belongs to user
    error_response = verify_card_ownership(target_card, current_user.id)
    if error_response:
        return jsonify(error_response[0]), error_response[1]

    try:
        # Delete the card
        db.session.delete(target_card)
        db.session.commit()
        return jsonify({"message": "Card successfully deleted"})
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"error": "Database error", "message": "Failed to delete card"}), 500


@cards_api.route("/reorder", methods=["PUT"])
@login_required
def update_card_order():
    """Update the order and section of multiple cards"""
    # Get JSON data from request
    request_data = request.get_json()
    
    # Ensure CSRF token is present
    if 'csrf_token' not in request.cookies:
        return jsonify({"error": "CSRF token missing"}), 400
        
    cards_to_reorder = request_data.get("reorderedCards", [])

    # Validate data structure
    if not isinstance(cards_to_reorder, list):
        return jsonify({"error": "Invalid format", "message": "Data must be a list of cards"}), 400

    # Collect all card IDs to verify ownership
    card_ids = [card_data.get('id') for card_data in cards_to_reorder if 'id' in card_data]
    
    # Verify user has access to all cards
    cards_from_db = Card.query.filter(Card.id.in_(card_ids)).all()
    
    # Create a map for quick lookup
    card_map = {card.id: card for card in cards_from_db}
    
    # Check if all cards exist and belong to user
    for card_id in card_ids:
        if card_id not in card_map:
            return jsonify({"error": "Not found", "message": f"Card with id {card_id} not found"}), 404
        
        if card_map[card_id].to_dict_basic()["userId"] != current_user.id:
            return jsonify({"error": "Forbidden", "message": "You do not have permission to update some cards"}), 403

    try:
        # Start a transaction
        db.session.begin_nested()
        
        # Process each card in the reorder list
        for card_data in cards_to_reorder:
            # Validate required fields
            required_fields = ["id", "order", "cardSectionId"]
            if not all(field in card_data for field in required_fields):
                db.session.rollback()
                return jsonify({
                    "error": "Missing data", 
                    "message": f"Missing required fields in card: {card_data}",
                    "required_fields": required_fields
                }), 400

            # Validate data types
            if not isinstance(card_data["id"], int) or not isinstance(card_data["order"], int):
                db.session.rollback()
                return jsonify({"error": "Invalid type", "message": f"Invalid data types in card: {card_data}"}), 400

            # Update card in database
            db_card = card_map.get(card_data["id"])
            if db_card:
                db_card.order = card_data["order"]
                db_card.card_section_id = card_data["cardSectionId"]

        # Commit all changes at once
        db.session.commit()
        return jsonify({"message": "Cards reordered successfully", "cards": cards_to_reorder})
    
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Database error", "message": "Failed to reorder cards"}), 500