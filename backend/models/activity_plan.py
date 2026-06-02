from datetime import datetime, timezone
from backend.extensions import db


class ActivityPlan(db.Model):
    __tablename__ = "activity_plans"

    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey("teacher_profiles.id"), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey("class_profiles.id"), nullable=False)
    school_id = db.Column(db.Integer, db.ForeignKey("schools.id"), nullable=False)

    activity_ids = db.Column(db.Text, nullable=False)  # JSON string
    notes = db.Column(db.Text, nullable=True)

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        import json

        try:
            activity_ids = json.loads(self.activity_ids) if self.activity_ids else []   

        except (json.JSONDecodeError, TypeError):
            activity_ids = []

        return {
            "id": self.id,
            "teacher_id": self.teacher_id,
            "class_id": self.class_id,
            "school_id": self.school_id,
            "activity_ids": activity_ids,
            "notes": self.notes,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }