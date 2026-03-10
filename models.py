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
    
    # Relationships
    # One-to-Many: A user can have many items they are giving away
    items = db.relationship('Item', back_populates='giver', cascade='all, delete-orphan')
    
    # One-to-Many: A user can make many requests (as a seeker)
    # foreign_keys specifies which column in Request identifies the seeker
    outgoing_requests = db.relationship('Request', 
                                       foreign_keys='Request.seeker_id', 
                                       back_populates='seeker',
                                       cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User: {self.name} ({self.phone_number})>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'phone_number': self.phone_number,
            'location': self.location,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'items_count': len(self.items) if self.items else 0
        }


class Category(db.Model):
    """
    Category model for classifying items.
    """
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(200))
    
    # One-to-Many: A category can have many items
    items = db.relationship('Item', back_populates='category')
    
    def __repr__(self):
        return f'<Category: {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'items_count': len(self.items) if self.items else 0
        }


class Item(db.Model):
    """
    Item model representing items people want to give away.
    
    This model has:
    - One-to-Many with User (one user has many items)
    - One-to-Many with Category (one category has many items)
    - One-to-Many with Request (one item can have many requests)
    """
    __tablename__ = 'items'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    photo_url = db.Column(db.String(500))
    condition = db.Column(db.String(50))  # "Like New", "Good", "Fair", "Needs Repair"
    
    # Pickup details (giver decides everything)
    pickup_location = db.Column(db.String(200), nullable=False)
    pickup_days = db.Column(db.String(100))  # e.g., "Saturdays 10am-2pm"
    pickup_times = db.Column(db.String(100))  # e.g., "10:00 - 14:00"
    special_instructions = db.Column(db.Text)
    
    # Status tracking
    is_available = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign Keys
    giver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    
    # Relationships
    # Many-to-One: Many items belong to one giver (User)
    giver = db.relationship('User', back_populates='items')
    
    # Many-to-One: Many items belong to one category
    category = db.relationship('Category', back_populates='items')
    
    # One-to-Many: One item can have many requests
    requests = db.relationship('Request', 
                              foreign_keys='Request.item_id',
                              back_populates='item',
                              cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Item: {self.title} (by {self.giver.name if self.giver else "Unknown"})>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'photo_url': self.photo_url,
            'condition': self.condition,
            'pickup_location': self.pickup_location,
            'pickup_days': self.pickup_days,
            'pickup_times': self.pickup_times,
            'special_instructions': self.special_instructions,
            'is_available': self.is_available,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'giver_id': self.giver_id,
            'giver_name': self.giver.name if self.giver else None,
            'category_id': self.category_id,
            'category_name': self.category.name if self.category else None,
            'requests_count': len([r for r in self.requests if r.status == 'pending']) if self.requests else 0
        }


class Request(db.Model):
    """
    Request model representing a seeker requesting an item from a giver.
    
    This is the MANY-TO-MANY relationship between User (seeker) and Item.
    
    USER-SUBMITTABLE ATTRIBUTE: message (the seeker writes why they need the item)
    
    A user can request many items (outgoing_requests)
    An item can be requested by many users (requests)
    
    But once a request is approved, the phone number is revealed and other requests
    should ideally be rejected/expired.
    """
    __tablename__ = 'requests'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # USER-SUBMITTABLE ATTRIBUTE - This is required by the project spec!
    # The seeker writes a message explaining why they need the item
    message = db.Column(db.Text, nullable=False)
    
    # Status tracking
    # pending: seeker has requested, giver hasn't decided
    # approved: giver approved this seeker, phone number revealed
    # rejected: giver chose someone else
    # completed: pickup happened successfully
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected, completed
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign Keys
    # seeker_id: The user who is requesting the item
    seeker_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # item_id: The item being requested
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)
    
    # Relationships
    # Many-to-One: Many requests belong to one seeker (User)
    seeker = db.relationship('User', foreign_keys=[seeker_id], back_populates='outgoing_requests')
    
    # Many-to-One: Many requests belong to one item
    item = db.relationship('Item', foreign_keys=[item_id], back_populates='requests')
    
    # We can access the giver through the item
    @property
    def giver(self):
        return self.item.giver if self.item else None
    
    @property
    def giver_phone(self):
        """
        Only reveal giver's phone number if request is approved.
        This is a security feature!
        """
        if self.status == 'approved' and self.item and self.item.giver:
            return self.item.giver.phone_number
        return None
    
    def __repr__(self):
        return f'<Request: {self.seeker.name if self.seeker else "Unknown"} -> {self.item.title if self.item else "Unknown"}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'message': self.message,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'seeker_id': self.seeker_id,
            'seeker_name': self.seeker.name if self.seeker else None,
            'item_id': self.item_id,
            'item_title': self.item.title if self.item else None,
            'giver_name': self.giver.name if self.giver else None,
            'giver_phone': self.giver_phone  # This will be None unless approved
        }