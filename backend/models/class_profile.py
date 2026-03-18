from datetime import datetime
from backend.extensions import db


class ClassProfile(db.Model):
    __tablename__ = "class_profiles"

    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey("teacher_profiles.id"), nullable=False)
    school_id = db.Column(db.Integer, db.ForeignKey("schools.id"), nullable=False)

    class_name = db.Column(db.String(150), nullable=False)
    age_group = db.Column(db.String(50), nullable=False)
    class_size = db.Column(db.Integer, nullable=False)

    learning_focus = db.Column(db.Text, nullable=True)       # JSON string
    available_resources = db.Column(db.Text, nullable=True)  # JSON string
    special_needs = db.Column(db.Text, nullable=True)        # JSON string

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        import json

        return {
            "id": self.id,
            "teacher_id": self.teacher_id,
            "school_id": self.school_id,
            "class_name": self.class_name,
            "age_group": self.age_group,
            "class_size": self.class_size,
            "learning_focus": json.loads(self.learning_focus) if self.learning_focus else [],
            "available_resources": json.loads(self.available_resources) if self.available_resources else [],
            "special_needs": json.loads(self.special_needs) if self.special_needs else [],
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }