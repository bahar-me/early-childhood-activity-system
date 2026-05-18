import json

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
    }


def get_all_activities() -> list[dict]:
    activities = Activity.query.order_by(Activity.id.asc()).all()
    return [serialize_activity(activity) for activity in activities]