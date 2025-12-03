"""
Admin Model
Represents hospital administrative staff
"""

from extensions import db


class Admin(db.Model):
    """
    Admin model for hospital staff
    Linked to User model via user_id
    """

    __tablename__ = 'admins'

    # Primary Key
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # Foreign Key to User
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)

    # Admin details
    name = db.Column(db.String(100), nullable=False)
    contact_number = db.Column(db.String(15), nullable=True)

    def __init__(self, user_id, name, contact_number=None):
        """Initialize a new Admin"""
        self.user_id = user_id
        self.name = name
        self.contact_number = contact_number

    def __repr__(self):
        """String representation of Admin"""
        return f'<Admin {self.name}>'

    def to_dict(self):
        """Convert admin to dictionary (for API responses)"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'contact_number': self.contact_number,
            'username': self.user.username if self.user else None,
            'email': self.user.email if self.user else None
        }

    @staticmethod
    def get_by_user_id(user_id):
        """Get admin by user ID"""
        return Admin.query.filter_by(user_id=user_id).first()

    @staticmethod
    def get_all_admins():
        """Get all admins"""
        return Admin.query.all()
