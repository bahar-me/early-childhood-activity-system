import json

from backend.extensions import db
from backend.models.activity import Activity


def serialize_activity(activity: Activity) -> dict:
    return {
        "id": str(activity.id),
        "title": activity.title,
        "subject": activity.subject,
        "duration": activity.duration,
        "groupSize": activity.group_size,
        "description": activity.description,
        "materials": json.loads(activity.materials),
        "instructions": json.loads(activity.instructions),
        "learningGoals": json.loads(activity.learning_goals),
        "sourceType": activity.source_type,
        "parentActivityId": str(activity.parent_activity_id) if activity.parent_activity_id else None,
        "createdByUserId": str(activity.created_by_user_id) if activity.created_by_user_id else None,
    }


def get_all_activities() -> list[dict]:
    activities = Activity.query.order_by(Activity.id.asc()).all()
    return [serialize_activity(activity) for activity in activities]

def create_activity(data: dict) -> dict:
    required_fields = ["title", "subject", "duration", "groupSize", "description", "materials", "instructions", "learningGoals"]
    for field in required_fields:
        if field not in data:
            raise ValueError(f"Missing required field: {field}")

    activity = Activity(
        title=data["title"],
        subject=data["subject"],
        duration=data["duration"],
        group_size=data["groupSize"],
        description=data["description"],
        materials=json.dumps(data["materials"], ensure_ascii=False),
        instructions=json.dumps(data["instructions"], ensure_ascii=False),
        learning_goals=json.dumps(data["learningGoals"], ensure_ascii=False),
        source_type=data.get("sourceType", "manual_edit"),
        parent_activity_id=int(data["parentActivityId"]) if data.get("parentActivityId") else None,
        created_by_user_id=int(data["createdByUserId"]) if data.get("createdByUserId") else None,
    )
    

    db.session.add(activity)
    db.session.commit()

    return serialize_activity(activity)