from datetime import datetime
from backend.extensions import db


class ActivityPlan(db.Model):
    __tablename__ = "activity_plans"

    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey("teacher_profiles.id"), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey("class_profiles.id"), nullable=False)
    school_id = db.Column(db.Integer, db.ForeignKey("schools.id"), nullable=False)

    activity_ids = db.Column(db.Text, nullable=False)  # JSON string
    notes = db.Column(db.Text, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        import json

        return {
            "id": self.id,
            "teacher_id": self.teacher_id,
            "class_id": self.class_id,
            "school_id": self.school_id,
            "activity_ids": json.loads(self.activity_ids) if self.activity_ids else [],
            "notes": self.notes,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }