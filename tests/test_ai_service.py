import os
import sys

import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.services.ai_service import (
    generate_recommendation_explanation,
    adapt_activity_mock,
    translate_subject,
    translate_duration,
    translate_group_size,
    translate_teaching_style,
)


def sample_activity():
    return {
        "id": "1",
        "title": "Renkli Sayılar",
        "subject": "Math",
        "duration": "15-30min",
        "groupSize": "Small Group",
        "description": "Çocuklarla sayı tanıma etkinliği.",
        "materials": ["Sayı kartları"],
        "instructions": [
            "Kartları göster",
            "Çocuklardan sayıları söylemelerini iste",
        ],
        "learningGoals": ["Sayıları tanıma"],
    }


def test_translate_helpers():
    assert translate_subject("Math") == "Matematik"
    assert translate_duration("15-30min") == "15-30 dakika"
    assert translate_group_size("Small Group") == "küçük grup çalışması"
    assert translate_teaching_style("structured") == "yapılandırılmış"


def test_generate_recommendation_explanation_requires_activity():
    result = generate_recommendation_explanation({"activities": []})

    assert result["success"] is False
    assert "error" in result


def test_generate_recommendation_explanation_success():
    result = generate_recommendation_explanation(
        {
            "teacher_profile": {
                "teaching_style": "structured",
            },
            "class_profile": {
                "class_name": "Çiçek Sınıfı",
                "age_group": "4-5",
            },
            "activities": [sample_activity()],
            "recommendation_reasons": ["Yaş grubuna uygun"],
        }
    )

    assert result["success"] is True
    assert result["source"] == "mock_ai"
    assert len(result["activity_explanations"]) == 1
    assert "Çiçek Sınıfı" in result["summary"]


def test_adapt_activity_mock_requires_activity():
    with pytest.raises(ValueError):
        adapt_activity_mock(
            {
                "adaptation_prompt": "kısa etkinlik yap",
            }
        )


def test_adapt_activity_mock_requires_prompt():
    with pytest.raises(ValueError):
        adapt_activity_mock(
            {
                "activity": sample_activity(),
                "adaptation_prompt": "",
            }
        )


def test_adapt_activity_mock_material_free_short_individual():
    result = adapt_activity_mock(
        {
            "activity": sample_activity(),
            "teacher_profile": {
                "teachingStyle": "structured",
            },
            "class_profile": {
                "ageGroup": "4-5",
            },
            "adaptation_prompt": "materyalsiz, kısa, bireysel ve sadeleştir",
        }
    )

    draft = result["activity_draft"]

    assert result["source"] == "mock_ai"
    assert draft["duration"] == "5-15min"
    assert draft["groupSize"] == "Individual"
    assert draft["materials"] == ["Ek materyal gerektirmeden uygulanabilir."]
    assert "Uyarlanmış Versiyon" in draft["title"]


def test_adapt_activity_mock_counting_goal_and_group():
    result = adapt_activity_mock(
        {
            "activity": sample_activity(),
            "teacher_profile": {
                "teachingStyle": "play-based",
            },
            "class_profile": {
                "ageGroup": "5-6",
            },
            "adaptation_prompt": "1'den 20'ye kadar sayılarla tüm sınıf etkinliği olsun",
        }
    )

    draft = result["activity_draft"]

    assert draft["groupSize"] == "Whole Class"
    assert "1-20 arası sayıları tanıma" in draft["learningGoals"]