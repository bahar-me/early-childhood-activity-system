from datetime import datetime, timezone
from backend.extensions import db


class ClassProfile(db.Model):
    __tablename__ = "class_profiles"

    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey("teacher_profiles.id"), nullable=False)
    school_id = db.Column(db.Integer, db.ForeignKey("schools.id"), nullable=False)
    
    school = db.relationship("School", backref="class_profiles", lazy=True)

    class_name = db.Column(db.String(150), nullable=False)
    age_group = db.Column(db.String(50), nullable=False)
    class_size = db.Column(db.Integer, nullable=False)

    learning_focus = db.Column(db.Text, nullable=True)       # JSON string
    available_resources = db.Column(db.Text, nullable=True)  # JSON string
    special_needs = db.Column(db.Text, nullable=True)        # JSON string

    morning_activities = db.Column(db.Integer, nullable=False, default=45)  # JSON string
    afternoon_activities = db.Column(db.Integer, nullable=False, default=30)  # JSON string

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        import json

        try:
            learning_focus = json.loads(self.learning_focus) if self.learning_focus else []
        except (json.JSONDecodeError, TypeError):
            learning_focus = []
        try:            
            available_resources = json.loads(self.available_resources) if self.available_resources else []
        except (json.JSONDecodeError, TypeError):
            available_resources = []
        try:
            special_needs = json.loads(self.special_needs) if self.special_needs else []
        except (json.JSONDecodeError, TypeError):
            special_needs = []

        return {
            "id": self.id,
            "teacher_id": self.teacher_id,
            "school_id": self.school_id,
            "school_name": self.school.name if self.school else None,
            "class_name": self.class_name,
            "age_group": self.age_group,
            "class_size": self.class_size,
            "learning_focus": learning_focus,
            "available_resources": available_resources,
            "special_needs": special_needs,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "daily_schedule": {
                "morning_activities": self.morning_activities,
                "afternoon_activities": self.afternoon_activities,
            }
        }