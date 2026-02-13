from shifu.app import db
from datetime import datetime, timezone


VALID_LOOKING_FOR = [
    'Request a Demo',
    'Start a Pilot Program',
    'General Inquiry',
    'Schedule a Briefing',
]


class ShifuForm(db.Model):
    """
    Form 2 - "Let's Get Started"
    Fields:
      Name*
      Work Email*
      Company*
      Role
      What are you looking for?*
      Tell us about your goals
    """
    __tablename__ = 'shifu_form'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    work_email = db.Column(db.String(255), nullable=False)
    company = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(255), nullable=True)
    looking_for = db.Column(db.String(255), nullable=False)
    goals = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'work_email': self.work_email,
            'company': self.company,
            'role': self.role,
            'looking_for': self.looking_for,
            'goals': self.goals,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self):
        return f'<ShifuForm {self.id} - {self.name}>'
