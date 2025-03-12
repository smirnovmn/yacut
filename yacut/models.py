from datetime import datetime

from yacut import db
from .constans import ORIGINAL_LINK_MAX_LENGTH, SHORT_LINK_MAX_LENGTH


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(ORIGINAL_LINK_MAX_LENGTH))
    short = db.Column(db.String(SHORT_LINK_MAX_LENGTH))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        return dict(
            original=self.original,
            short=self.short,
        )

    def from_dict(self, data):
        for field in ['original', 'short']:
            if field in data:
                setattr(self, field, data[field])