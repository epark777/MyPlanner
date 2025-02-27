from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.models import Card, CardSection, db
from app.forms import CardForm


# Initialize Blueprint
cards_blueprint = Blueprint("cards", __name__)


def verify_card_ownership(card_instance, user_id):
    """Helper function to verify card ownership"""
    if not card_instance:
        return {"error": "Card not found", "status": 404}

    if card_instance.to_dict_basic()["userId"] != user_id:
        return {"error": "Forbidden - You do not own this card", "status": 403}

    return None


@cards_blueprint.route("<int:card_id>", methods=["PUT"])
@login_required
def update_card(card_id):
    """Update a card if the current user is the owner"""
    # Find the card by ID
    target_card = Card.query.get(card_id)

    # Check if card exists and belongs to user
    ownership_check = verify_card_ownership(target_card, current_user.id)
    if ownership_check:
        return ownership_check["error"], ownership_check["status"]

    # Process the form data
    card_form = CardForm()
    card_form["csrf_token"].data = request.cookies["csrf_token"]

    if card_form.validate_on_submit():
        # Update card fields
        form_data = card_form.data
        target_card.name = form_data["name"]
        target_card.description = form_data["description"]
        target_card.labels = form_data["labels"]
        target_card.due_date = form_data["due_date"]

        # Save changes
        db.session.commit()
        return target_card.to_dict_basic()

    # Form validation failed
    return card_form.errors, 400


@cards_blueprint.route("<int:card_id>", methods=["DELETE"])
@login_required
def remove_card(card_id):
    """Remove a card if the current user is the owner"""
    # Find the card by ID
    target_card = Card.query.get(card_id)

    # Check if card exists and belongs to user
    ownership_check = verify_card_ownership(target_card, current_user.id)
    if ownership_check:
        return ownership_check["error"], ownership_check["status"]

    # Delete the card
    db.session.delete(target_card)
    db.session.commit()

    return {"message": "Card successfully deleted"}


@cards_blueprint.route("/reorder", methods=["PUT"])
@login_required
def update_card_order():
    """Update the order and section of multiple cards"""
    # Get JSON data from request
    request_data = request.get_json()
    cards_to_reorder = request_data.get("reorderedCards", [])

    # Validate data structure
    if not isinstance(cards_to_reorder, list):
        return {"error": "Data must be a list of cards"}, 400

    # Process each card in the reorder list
    for card_data in cards_to_reorder:
        # Validate required fields
        required_fields = ["id", "order", "cardSectionId"]
        if not all(field in card_data for field in required_fields):
            return {
                "error": f"Missing required fields in card: {card_data}",
                "required_fields": required_fields,
            }, 400

        # Validate data types
        if not isinstance(card_data["id"], int) or not isinstance(
            card_data["order"], int
        ):
            return {"error": f"Invalid data types in card: {card_data}"}, 400

        # Update card in database
        db_card = Card.query.get(card_data["id"])
        if db_card:
            db_card.order = card_data["order"]
            db_card.card_section_id = card_data["cardSectionId"]
            db.session.add(db_card)

    # Commit all changes at once
    db.session.commit()

    return jsonify(cards_to_reorder)
