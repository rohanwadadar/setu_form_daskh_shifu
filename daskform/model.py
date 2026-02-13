from daskform.app import db
from datetime import datetime, timezone


class DakshForm(db.Model):
    """
    Form 1 - "Let's Connect"
    Fields:
      // YOUR_EMAIL
      // WHAT_BEST_DESCRIBES_YOU?
      // WHAT_ARE_YOU_HOPING_TO_ACHIEVE?
      // TELL_US_MORE (OPTIONAL)
    """
    __tablename__ = 'daksh_form'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    your_email = db.Column(db.String(255), nullable=False)
    what_best_describes_you = db.Column(db.String(500), nullable=False)
    what_are_you_hoping_to_achieve = db.Column(db.String(500), nullable=False)
    tell_us_more = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            'id': self.id,
            'your_email': self.your_email,
            'what_best_describes_you': self.what_best_describes_you,
            'what_are_you_hoping_to_achieve': self.what_are_you_hoping_to_achieve,
            'tell_us_more': self.tell_us_more,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self):
        return f'<DakshForm {self.id} - {self.your_email}>'
