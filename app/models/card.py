from .db import db, environment, SCHEMA, add_prefix_for_prod
from datetime import datetime, timezone

class Card(db.Model):
    __tablename__ = 'cards'

    if environment == "production":
      __table_args__ = {'schema': SCHEMA}
  
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    labels = db.Column(db.String(255))
    due_date = db.Column(db.DateTime)
    order = db.Column(db.Integer)
    card_section_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('card_sections.id')), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    # Relationships
    card_section = db.relationship('CardSection', back_populates='cards')

    def to_dict_basic(self):
        return {
        "id": self.id,
        "name": self.name,
        "description": self.description,
        "labels": self.labels,
        "dueDate": self.due_date,
        "order": self.order,
        "cardSectionId": self.card_section_id,
        "createdAt": self.created_at,
        "updatedAt": self.updated_at,
        "userId": self.card_section.to_dict_basic()['userId']
    }