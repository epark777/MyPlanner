from .db import db, environment, SCHEMA, add_prefix_for_prod
from datetime import datetime, timezone

class Favorite(db.Model):
  __tablename__ = 'favorites'

  if environment == "production":
      __table_args__ = {'schema': SCHEMA}
  
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('users.id')), nullable=False)
  board_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('boards.id')), nullable=False)
  created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
  updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

  # Relationships
  user = db.relationship('User', back_populates='favorites')
  board = db.relationship('Board', back_populates='favorites')

  def to_dict_basic(self):
    return {
      "id": self.id,
      "userId": self.user_id,
      "boardId": self.board_id,
      "createdAt": self.created_at,
      "updatedAt": self.updated_at
    }
  
  def to_dict_board(self):
     return {
        **self.to_dict_basic(),
        "Board": self.board.to_dict_basic()
     }