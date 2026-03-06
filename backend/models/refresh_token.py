from backend.extensions import db

class RefreshToken(db.Model):

    __tablename__ = "refresh_tokens"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    token = db.Column(db.Text, nullable=False)

    expires_at = db.Column(db.DateTime, nullable=False)