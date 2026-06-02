import json

from backend.extensions import db
from backend.models.activity import Activity

def safe_json_loads(value: str | None, default):
    if not value:
        return default

    try:
        return json.loads(value)
    except (json.JSONDecodeError, TypeError):
        return default

def serialize_activity(activity: Activity) -> dict:
    return {
        "id": str(activity.id),
        "title": activity.title,
        "subject": activity.subject,
        "duration": activity.duration,
        "groupSize": activity.group_size,
        "description": activity.description,
        "materials": safe_json_loads(activity.materials, []),
        "instructions": safe_json_loads(activity.instructions, []),
        "learningGoals": safe_json_loads(activity.learning_goals, []),

        "assessmentQuestions": safe_json_loads(activity.assessment_questions, []),
        "differentiationNotes": activity.differentiation_notes,
        "familyCommunityNotes": activity.family_community_notes,
        "learningOutcomesSummary": activity.learning_outcomes_summary,

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
        
        assessment_questions=json.dumps(data.get("assessmentQuestions", []), ensure_ascii=False),
        differentiation_notes=data.get("differentiationNotes"),
        family_community_notes=data.get("familyCommunityNotes"),
        learning_outcomes_summary=data.get("learningOutcomesSummary"),
        
        source_type=data.get("sourceType", "manual_edit"),
        parent_activity_id=int(data["parentActivityId"]) if data.get("parentActivityId") else None,
        created_by_user_id=int(data["createdByUserId"]) if data.get("createdByUserId") else None,
    )

    db.session.add(activity)
    db.session.commit()
    return serialize_activity(activity)
    
def update_activity(activity_id: int, data: dict) -> dict:
    activity = db.session.get(Activity, activity_id)
    if not activity:
        raise ValueError("Etkinlik bulunamadı.")

    required_fields = [
        "title",
        "subject",
        "duration",
        "groupSize",
        "description",
        "materials",
        "instructions",
        "learningGoals",
    ]
    for field in required_fields:
        if field not in data:
            raise ValueError(f"Missing required field: {field}")

    activity.title = data["title"]
    activity.subject = data["subject"]
    activity.duration = data["duration"]
    activity.group_size = data["groupSize"]
    activity.description = data["description"]
    activity.materials = json.dumps(data["materials"], ensure_ascii=False)
    activity.instructions = json.dumps(data["instructions"], ensure_ascii=False)
    activity.learning_goals = json.dumps(data["learningGoals"], ensure_ascii=False)

    activity.assessment_questions = json.dumps(data.get("assessmentQuestions", []), ensure_ascii=False)
    activity.differentiation_notes = data.get("differentiationNotes")
    activity.family_community_notes = data.get("familyCommunityNotes")
    activity.learning_outcomes_summary = data.get("learningOutcomesSummary")


    db.session.commit()

    return serialize_activity(activity)