from datetime import datetime, timezone
from backend.extensions import db

class Activity(db.Model):
    __tablename__ = "activities"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    subject = db.Column(db.String(50), nullable=False)
    duration = db.Column(db.String(20), nullable=False)
    group_size = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    materials = db.Column(db.Text, nullable=False)        # JSON string
    instructions = db.Column(db.Text, nullable=False)     # JSON string
    learning_goals = db.Column(db.Text, nullable=False)   # JSON string
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    source_type = db.Column(db.String(50), nullable=False, default="seed") 
    parent_activity_id = db.Column(db.Integer, db.ForeignKey("activities.id", name="fk_activities_parent_activity_id"), nullable=True)
    created_by_user_id = db.Column(db.Integer, db.ForeignKey("users.id", name="fk_activities_created_by_user_id"), nullable=True)