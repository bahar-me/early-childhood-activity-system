from typing import Dict, List, Any


def translate_subject(subject: str) -> str:
    translations = {
        "Math": "Matematik",
        "Language": "Dil Gelişimi",
        "Art": "Sanat",
        "Science": "Fen ve Doğa",
        "Music": "Müzik",
        "Physical": "Fiziksel Gelişim",
        "Social-Emotional": "Sosyal-Duygusal Gelişim",
    }
    return translations.get(subject, subject or "genel gelişim")


def translate_group_size(group_size: str) -> str:
    translations = {
        "Individual": "bireysel çalışma",
        "Small Group": "küçük grup çalışması",
        "Whole Class": "tüm sınıf çalışması",
    }
    return translations.get(group_size, group_size or "uygun grup yapısı")


def translate_teaching_style(style: str) -> str:
    translations = {
        "balanced": "dengeli",
        "play-based": "oyun temelli",
        "structured": "yapılandırılmış",
        "creative": "yaratıcı",
        "interactive": "etkileşimli",
    }
    return translations.get(style, style or "öğretmenin yaklaşımı")


def translate_duration(duration: str) -> str:
    translations = {
        "5-15min": "5-15 dakika",
        "15-30min": "15-30 dakika",
        "30-45min": "30-45 dakika",
        "45-60min": "45-60 dakika",
    }
    return translations.get(duration, duration or "uygun süre")

def generate_recommendation_explanation(data: Dict[str, Any]) -> Dict[str, Any]:
    teacher_profile = data.get("teacher_profile") or {}
    class_profile = data.get("class_profile") or {}
    activities: List[Dict[str, Any]] = data.get("activities") or []
    recommendation_reasons = data.get("recommendation_reasons") or []

    if not activities:
        return {
            "success": False,
            "error": "At least one activity is required for AI explanation.",
        }

    class_name = class_profile.get("class_name") or "bu sınıf"
    age_group = class_profile.get("age_group") or "seçilen yaş grubu"
    teaching_style = translate_teaching_style(teacher_profile.get("teaching_style") or "öğretmenin yaklaşımı")

    activity_explanations = []

    for activity in activities:
        activity_id = activity.get("id")
        title = activity.get("title", "Selected activity")
        subject = translate_subject(activity.get("subject") or "genel gelişim")
        duration = translate_duration(activity.get("duration") or "uygun süre")
        group_size = translate_group_size(activity.get("groupSize") or activity.get("group_size") or "uygun grup yapısı")

        activity_explanations.append(
            {
                "activity_id": activity_id,
                "title": title,
                "explanation": (
                    f"'{title}' etkinliği {age_group} yaş grubu için uygun görülebilir. "
                    f"Etkinlik, {subject} alanını destekler ve {group_size} çalışma yapısına uygundur."
                ),
                "teacher_guidance": (
                    f"Öğretmen, etkinliği uygulamadan önce kısa ve anlaşılır yönergeler verebilir. "
                    f"{duration} süresine dikkat ederek çocukların aktif katılımını destekleyebilir."
                ),
                "adaptation": (
                    "Sınıftaki çocukların ihtiyaçlarına göre yönergeler sadeleştirilebilir, "
                    "materyaller azaltılabilir veya küçük grup desteği sağlanabilir."
                ),
            }
        )

    return {
        "success": True,
        "summary": (
            f"Bu plan, {class_name} için hazırlanmış etkinliklerden oluşmaktadır. "
            f"Öneriler, sınıf profili, yaş grubu, öğrenme hedefleri ve {teaching_style} öğretim stili "
            f"dikkate alınarak pedagojik açıdan destekleyici hale getirilmiştir."
        ),
        "activity_explanations": activity_explanations,
        "recommendation_reasons": recommendation_reasons,
        "source": "mock_ai",
    }

def adapt_activity_mock(payload: dict) -> dict:
    activity = payload.get("activity", {})
    teacher_profile = payload.get("teacher_profile", {})
    class_profile = payload.get("class_profile", {})
    adaptation_prompt = (payload.get("adaptation_prompt") or "").strip()

    if not activity:
        raise ValueError("Etkinlik verisi eksik.")
    if not adaptation_prompt:
        raise ValueError("Uyarlama isteği boş olamaz.")

    original_title = activity.get("title", "Yeni Etkinlik")
    original_description = activity.get("description", "")
    original_materials = activity.get("materials", [])
    original_instructions = activity.get("instructions", [])
    original_learning_goals = activity.get("learningGoals", [])
    original_subject = activity.get("subject", "Math")
    original_duration = activity.get("duration", "15-30min")
    original_group_size = activity.get("groupSize", "Small Group")

    age_group = class_profile.get("age_group") or class_profile.get("ageGroup") or "okul öncesi"
    teaching_style = teacher_profile.get("teaching_style") or teacher_profile.get("teachingStyle") or "öğretmenin yaklaşımı"

    adapted_title = f"{original_title} - Uyarlanmış Versiyon"

    adapted_description = (
        f"Bu etkinlik, '{adaptation_prompt}' isteği dikkate alınarak yeniden düzenlenmiştir. "
        f"{age_group} yaş grubu ve {teaching_style} öğretim yaklaşımı göz önünde bulundurulmuştur. "
        f"{original_description}"
    )

    adapted_materials = original_materials[:]
    adapted_instructions = original_instructions[:]
    adapted_learning_goals = original_learning_goals[:]

    prompt_lower = adaptation_prompt.lower()

    if "materyalsiz" in prompt_lower or "malzemesiz" in prompt_lower:
        adapted_materials = ["Ek materyal gerektirmeden uygulanabilir."]
        adapted_instructions = [
            "Öğretmen etkinliği sözlü yönergelerle başlatır.",
            "Çocuklar etkinliği beden hareketleri, konuşma veya sınıf içi mevcut nesnelerle uygular.",
            "Etkinlik sonunda kısa bir değerlendirme yapılır.",
        ]

    if "15 dakika" in prompt_lower or "kısa" in prompt_lower:
        original_duration = "15-30min"

    if "bireysel" in prompt_lower:
        original_group_size = "Individual"
    elif "küçük grup" in prompt_lower:
        original_group_size = "Small Group"
    elif "tüm sınıf" in prompt_lower or "whole class" in prompt_lower:
        original_group_size = "Whole Class"

    adapted_learning_goals = adapted_learning_goals[:]
    if "sadeleştir" in prompt_lower:
        adapted_learning_goals = adapted_learning_goals[:3]

    return {
        "activity_draft": {
            "title": adapted_title,
            "subject": original_subject,
            "duration": original_duration,
            "groupSize": original_group_size,
            "description": adapted_description,
            "materials": adapted_materials,
            "instructions": adapted_instructions,
            "learningGoals": adapted_learning_goals,
        },
        "source": "mock_ai",
    }