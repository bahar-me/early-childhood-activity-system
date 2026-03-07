from datetime import datetime, timezone
from backend.extensions import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="teacher")
    school_id = db.Column(db.Integer, db.ForeignKey("schools.id"), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    school = db.relationship("School", back_populates="users")
    refresh_tokens = db.relationship(
        "RefreshToken", 
        back_populates="user", 
        lazy=True, 
        cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "role": self.role,
            "school_id": self.school_id,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }