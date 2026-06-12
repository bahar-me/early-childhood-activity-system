from datetime import datetime, timezone
from backend.extensions import db


class TeacherProfile(db.Model):
    __tablename__ = "teacher_profiles"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, unique=True)
    school_id = db.Column(db.Integer, db.ForeignKey("schools.id"), nullable=False)

    school = db.relationship("School", backref="teacher_profiles", lazy=True)

    name = db.Column(db.String(150), nullable=False)
    years_experience = db.Column(db.Integer, nullable=False, default=0)
    specializations = db.Column(db.Text, nullable=True)  # JSON string
    teaching_style = db.Column(db.String(150), nullable=True)

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        import json

        try:
            specializations = json.loads(self.specializations) if self.specializations else []
        except (json.JSONDecodeError, TypeError):
            specializations = []

        return {
            "id": self.id,
            "user_id": self.user_id,
            "school_id": self.school_id,
            "school_name": self.school.name if self.school else None,
            "name": self.name,
            "years_experience": self.years_experience,
            "specializations": specializations,
            "teaching_style": self.teaching_style,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }