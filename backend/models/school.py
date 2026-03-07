from datetime import datetime, timezone
from backend.extensions import db

class School(db.Model):
    __tablename__ = "schools"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    address = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    users = db.relationship("User", back_populates="school", lazy=True, cascade="all, delete")    

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "address": self.address,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f"<School {self.name}>"