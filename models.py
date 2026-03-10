from app import db
from datetime import datetime

class User(db.Model):
    """
    User model representing people who give and request items.
    """
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # TEMPORARILY COMMENTED OUT - Will add back in Commit 3
    # items = db.relationship('Item', back_populates='giver', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User: {self.name} ({self.phone_number})>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'phone_number': self.phone_number,
            'location': self.location,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Category(db.Model):
    """
    Category model for classifying items.
    """
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(200))
    
    # TEMPORARILY COMMENTED OUT - Will add back in Commit 3
    # items = db.relationship('Item', back_populates='category')
    
    def __repr__(self):
        return f'<Category: {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
            # 'items_count': len(self.items) if self.items else 0  # Comment this out too
        }