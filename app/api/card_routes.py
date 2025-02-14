from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.models import Card, CardSection, db
from app.forms import CardForm


card_routes = Blueprint('cards', __name__)


@card_routes.route('<int:cardId>', methods=['PUT'])
@login_required
def edit_card(cardId):
  """
  Update a card based on its id when the user is logged in
  """
  card = Card.query.get(cardId)
  if not card:
    return {'message': 'Card couldn\'t be found'}, 404
  
  if card.to_dict_basic()['userId'] != current_user.id:
    return {"message" : "Forbidden"}, 403

  form = CardForm()
  form['csrf_token'].data = request.cookies['csrf_token']

  if form.validate_on_submit():
    card.name = form.data['name']
    card.description = form.data['description']
    card.labels = form.data['labels']
    card.due_date = form.data['due_date']
    db.session.commit()
    return card.to_dict_basic()
  
  return form.errors, 400


@card_routes.route('<int:cardId>', methods=['DELETE'])
@login_required
def delete_card(cardId):
  """
  Delete a card based on its id when the user is logged in
  """
  card = Card.query.get(cardId)
  if not card:
    return {"message": "Card couldn't be found"}
  
  if card.to_dict_basic()['userId'] != current_user.id:
    return {"message" : "Forbidden"}, 403
  
  db.session.delete(card)
  db.session.commit()
  return {"message": "Successfully deleted"}


@card_routes.route('/reorder', methods=['PUT'])
@login_required
def reorder_card():
  data = request.get_json()
  reordered_cards = data['reorderedCards']
  print(reordered_cards)
  if not isinstance(reordered_cards, list):
    return {"message" : "Invalid data format"}, 400
  
  for card in reordered_cards:
    print(card)
    if not all(key in card for key in ['id', 'order', 'cardSectionId']):
      return {"message": f"Missing required fields in card data: {card}"}, 400
    
    if not isinstance(card['id'], int) or not isinstance(card['order'], int):
      return {"message": f"Invalid data types in card: {card}"}, 400
    
    card_in_db = Card.query.get(card['id'])
    print(card_in_db)
    if card_in_db:
      card_in_db.order = card['order']
      card_in_db.card_section_id = card['cardSectionId']
      db.session.add(card_in_db)
  db.session.commit()

  return jsonify(reordered_cards)