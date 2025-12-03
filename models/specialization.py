"""
Specialization Model
Represents medical departments/specializations
"""

from extensions import db


class Specialization(db.Model):
    """
    Specialization/Department model
    Stores different medical specializations (Cardiology, Neurology, etc.)
    """

    __tablename__ = 'specializations'

    # Primary Key
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # Specialization details
    name = db.Column(db.String(100), unique=True, nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)

    # Relationships
    doctors = db.relationship('Doctor', backref='specialization', lazy='dynamic')

    def __init__(self, name, description=None):
        """Initialize a new Specialization"""
        self.name = name
        self.description = description

    def __repr__(self):
        """String representation of Specialization"""
        return f'<Specialization {self.name}>'

    @property
    def doctor_count(self):
        """Get count of doctors in this specialization"""
        return self.doctors.count()

    def to_dict(self):
        """Convert specialization to dictionary (for API responses)"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'doctor_count': self.doctor_count
        }

    @staticmethod
    def get_all_specializations():
        """Get all specializations"""
        return Specialization.query.order_by(Specialization.name).all()

    @staticmethod
    def get_by_name(name):
        """Get specialization by name"""
        return Specialization.query.filter_by(name=name).first()

    @staticmethod
    def search(query):
        """Search specializations by name"""
        return Specialization.query.filter(
            Specialization.name.ilike(f'%{query}%')
        ).all()
