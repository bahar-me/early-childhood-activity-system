import os
import sys

import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.app import create_app
from backend.extensions import db
from backend.services.activity_service import (
    safe_json_loads,
    create_activity,
    get_all_activities,
    update_activity,
)


@pytest.fixture
def app_context():
    app = create_app("testing")

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


def activity_payload():
    return {
        "title": "Geometrik Şekiller",
        "subject": "Math",
        "duration": "15-30min",
        "groupSize": "Small Group",
        "description": "Çocukların şekilleri tanımasını sağlayan etkinlik.",
        "materials": ["Şekil kartları", "Renkli kâğıt"],
        "instructions": ["Kartları göster", "Çocuklardan şekilleri eşleştirmelerini iste"],
        "learningGoals": ["Şekilleri tanıma", "Eşleştirme becerisi"],
        "assessmentQuestions": ["Hangi şekli seçtin?"],
        "differentiationNotes": "Gerektiğinde daha az kart kullanılabilir.",
        "familyCommunityNotes": "Aileler evde şekil arama oyunu oynayabilir.",
        "learningOutcomesSummary": "Çocukların şekil farkındalığı desteklenir.",
    }


def test_safe_json_loads_returns_default_for_invalid_json():
    assert safe_json_loads("invalid-json", []) == []
    assert safe_json_loads(None, []) == []


def test_create_activity_success(app_context):
    result = create_activity(activity_payload())

    assert result["title"] == "Geometrik Şekiller"
    assert result["subject"] == "Math"
    assert result["materials"] == ["Şekil kartları", "Renkli kâğıt"]


def test_create_activity_missing_required_field(app_context):
    payload = activity_payload()
    del payload["title"]

    with pytest.raises(ValueError):
        create_activity(payload)


def test_get_all_activities(app_context):
    create_activity(activity_payload())

    activities = get_all_activities()

    assert len(activities) == 1
    assert activities[0]["title"] == "Geometrik Şekiller"


def test_update_activity_success(app_context):
    created = create_activity(activity_payload())

    updated_payload = activity_payload()
    updated_payload["title"] = "Güncellenmiş Etkinlik"

    result = update_activity(int(created["id"]), updated_payload)

    assert result["title"] == "Güncellenmiş Etkinlik"


def test_update_activity_not_found(app_context):
    with pytest.raises(ValueError):
        update_activity(9999, activity_payload())