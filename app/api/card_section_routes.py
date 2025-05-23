from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.models import CardSection, Card, db
from app.forms import CardSectionForm, CardForm
from sqlalchemy.exc import SQLAlchemyError


# Create Blueprint for section-related routes
section_api = Blueprint("card-sections", __name__)


def validate_section_access(section_id):
    """
    Helper function to validate section existence and user access
    Returns tuple of (section_object, error_response)
    """
    # Find the section
    section = CardSection.query.get(section_id)

    # Check if section exists
    if not section:
        return None, ({"error": "Not Found", "message": "Section not found"}, 404)

    # Check ownership
    board_owner_id = section.board.user_id
    if board_owner_id != current_user.id:
        return None, (
            {
                "error": "Forbidden",
                "message": "You don't have permission to access this section",
            },
            403,
        )

    # Section exists and user has access
    return section, None


@section_api.route("/<int:section_id>", methods=["PUT"])
@login_required
def update_section(section_id):
    """Modify an existing section's details"""
    # Validate access
    section, error = validate_section_access(section_id)
    if error:
        return jsonify(error[0]), error[1]

    # Process form data
    form = CardSectionForm()
    form["csrf_token"].data = request.cookies["csrf_token"]

    # Update section if form is valid
    if form.validate_on_submit():
        try:
            section.title = form.data["title"]
            db.session.commit()
            return jsonify(section.to_dict_basic())
        except SQLAlchemyError:
            db.session.rollback()
            return (
                jsonify(
                    {"error": "Database error", "message": "Failed to update section"}
                ),
                500,
            )

    # Return form errors if validation fails
    return jsonify({"error": "Validation failed", "details": form.errors}), 400


@section_api.route("/<int:section_id>", methods=["DELETE"])
@login_required
def remove_section(section_id):
    """Remove a section from the board"""
    # Validate access
    section, error = validate_section_access(section_id)
    if error:
        return jsonify(error[0]), error[1]

    # Delete the section
    try:
        db.session.delete(section)
        db.session.commit()
        return jsonify({"message": "Section successfully removed"})
    except SQLAlchemyError:
        db.session.rollback()
        return (
            jsonify({"error": "Database error", "message": "Failed to delete section"}),
            500,
        )


# Card management within sections
@section_api.route("/<int:section_id>/cards")
@login_required
def list_section_cards(section_id):
    """Retrieve all cards in a section"""
    # Validate access
    section, error = validate_section_access(section_id)
    if error:
        return jsonify(error[0]), error[1]

    # Return cards data
    return jsonify({"cards": section.to_dict_card()["Cards"]})


@section_api.route("/<int:section_id>/cards", methods=["POST"])
@login_required
def add_card_to_section(section_id):
    """Add a new card to a section"""
    # Validate access
    section, error = validate_section_access(section_id)
    if error:
        return jsonify(error[0]), error[1]

    # Process form data
    form = CardForm()
    form["csrf_token"].data = request.cookies["csrf_token"]

    if form.validate_on_submit():
        try:
            # Begin a transaction
            db.session.begin_nested()

            # Determine card order
            order_value = form.data["order"]
            if not order_value:
                # Auto-calculate order if not provided
                existing_cards = Card.query.filter_by(card_section_id=section_id).all()

                if not existing_cards:
                    order_value = 0
                else:
                    # Get highest order value and increment
                    highest_order = (
                        Card.query.filter_by(card_section_id=section_id)
                        .order_by(Card.order.desc())
                        .first()
                        .order
                    )
                    order_value = highest_order + 1

            # Create card
            card = Card(
                card_section_id=section_id,
                name=form.data["name"],
                description=form.data["description"],
                labels=form.data["labels"],
                due_date=form.data["due_date"],
                order=order_value,
            )

            # Save to database
            db.session.add(card)
            db.session.commit()

            return jsonify(card.to_dict_basic()), 201
        except SQLAlchemyError:
            db.session.rollback()
            return (
                jsonify(
                    {"error": "Database error", "message": "Failed to create card"}
                ),
                500,
            )

    # Return form errors if validation fails
    return jsonify({"error": "Validation failed", "details": form.errors}), 400
