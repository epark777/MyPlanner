from .db import db, environment, SCHEMA, add_prefix_for_prod
from datetime import datetime, timezone


class Board(db.Model):
  __tablename__ = 'boards'

  if environment == "production":
      __table_args__ = {'schema': SCHEMA}

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(255), nullable=False)
  user_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('users.id')), nullable=False)
  created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
  updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

  # Relationships
  user = db.relationship('User', back_populates='boards')
  card_sections = db.relationship('CardSection', back_populates='board', cascade='all, delete-orphan')
  favorites = db.relationship('Favorite', back_populates='board', cascade='all, delete-orphan')
  

  def to_dict_basic(self):
    return {
      "id": self.id,
      "name": self.name,
      "userId": self.user_id,
      "createdAt": self.created_at,
      "updatedAt": self.updated_at
    }

  def to_dict_detail(self):
     return {
        **self.to_dict_basic(),
        "CardSections": [card_section.to_dict_card() for card_section in self.card_sections]
     }
