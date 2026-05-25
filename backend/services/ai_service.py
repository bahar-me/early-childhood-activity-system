from typing import Dict, List, Any
import os
import json
from click import prompt
from google import genai
from google.genai import types 
#from openai import OpenAI

#client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
gemini_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

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
        "Balanced": "dengeli",
        "balanced": "dengeli",
        "Play-based": "oyun temelli",
        "play-based": "oyun temelli",
        "Structured": "yapılandırılmış",
        "structured": "yapılandırılmış",
        "Child-led": "çocuk merkezli",
        "child-led": "çocuk merkezli",
        "Creative": "yaratıcı",
        "creative": "yaratıcı",
        "Interactive": "etkileşimli",
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
    original_description = (activity.get("description") or "").strip() 
    original_materials = activity.get("materials", [])
    original_instructions = activity.get("instructions", [])
    original_learning_goals = activity.get("learningGoals", [])
    original_subject = activity.get("subject", "Math")
    original_duration = activity.get("duration", "15-30min")
    original_group_size = activity.get("groupSize", "Small Group")

    raw_age_group = class_profile.get("age_group") or class_profile.get("ageGroup") or "okul öncesi"
    raw_style = (
        teacher_profile.get("teaching_style") 
        or teacher_profile.get("teachingStyle") 
        or ""
    )
    style_map = {
        "Balanced": "dengeli",
        "balanced": "dengeli",
        "Play-based": "oyun temelli",
        "play-based": "oyun temelli",
        "Structured": "yapılandırılmış",
        "structured": "yapılandırılmış",
        "Child-led": "çocuk merkezli",
        "child-led": "çocuk merkezli",
        "Creative": "yaratıcı",
        "creative": "yaratıcı",
        "Interactive": "etkileşimli",
        "interactive": "etkileşimli",
    }
    display_style = style_map.get(raw_style, raw_style or "öğretmenin yaklaşımı")
    
    def strip_previous_adaptation_text(description: str) -> str:
        marker = "göz önünde bulundurulmuştur."
        if marker in description:
            return description.split(marker, 1)[-1].strip()
        return description
    
    base_description = strip_previous_adaptation_text(original_description)

    adapted_title = f"{original_title} - Uyarlanmış Versiyon"

    adapted_materials = original_materials[:]
    adapted_instructions = original_instructions[:]
    adapted_learning_goals = original_learning_goals[:]
    adapted_duration = original_duration
    adapted_group_size = original_group_size

    prompt_lower = adaptation_prompt.lower()

    if "materyalsiz" in prompt_lower or "malzemesiz" in prompt_lower:
        adapted_materials = ["Ek materyal gerektirmeden uygulanabilir."]
        adapted_instructions = [
            "Öğretmen etkinliği sözlü yönergelerle başlatır.",
            "Çocuklar etkinliği beden hareketleri, konuşma veya sınıf içi mevcut nesnelerle uygular.",
            "Etkinlik sonunda kısa bir değerlendirme yapılır.",
        ]

    if "5-15" in prompt_lower or "kısa" in prompt_lower or "15 dakikalık" in prompt_lower:
        adapted_duration = "5-15min"
    elif "15-30" in prompt_lower or "orta" in prompt_lower or "30 dakikalık" in prompt_lower:
        adapted_duration = "15-30min"  
    elif "30-45" in prompt_lower:
        adapted_duration = "30-45min"
    elif "45-60" in prompt_lower:
        adapted_duration = "45-60min"

    if "bireysel" in prompt_lower:
        adapted_group_size = "Individual"
    elif "küçük grup" in prompt_lower:
        adapted_group_size = "Small Group"
    elif "tüm sınıf" in prompt_lower or "whole class" in prompt_lower:
        adapted_group_size = "Whole Class"

    if "sadeleştir" in prompt_lower:
        adapted_learning_goals = adapted_learning_goals[:3]
        if len(adapted_instructions) > 3:
            adapted_instructions = adapted_instructions[:3]

    if "1-20" in prompt_lower or "1 den 20" in prompt_lower or "1'den 20" in prompt_lower:
        adapted_learning_goals = list(dict.fromkeys(adapted_learning_goals +["1-20 arası sayıları tanıma"]))

    adapted_description = (
        f"Bu etkinlik, '{adaptation_prompt}' isteği dikkate alınarak düzenlenmiştir. "
        f"{raw_age_group} yaş grubu ve {display_style} öğretim yaklaşımı göz önünde bulundurulmuştur. "
        f"{base_description}"
    ).strip()

    return {
        "activity_draft": {
            "title": adapted_title,
            "subject": original_subject,
            "duration": adapted_duration,
            "groupSize": adapted_group_size,
            "description": adapted_description,
            "materials": adapted_materials,
            "instructions": adapted_instructions,
            "learningGoals": adapted_learning_goals,
        },
        "source": "mock_ai",
    }

# def adapt_activity_with_llm(payload: dict) -> dict:
#     activity = payload.get("activity", {})
#     teacher_profile = payload.get("teacher_profile", {})
#     class_profile = payload.get("class_profile", {})
#     adaptation_prompt = (payload.get("adaptation_prompt") or "").strip()

#     if not activity:
#         raise ValueError("Etkinlik verisi eksik.")
#     if not adaptation_prompt:
#         raise ValueError("Uyarlama isteği boş olamaz.")

#     schema = {
#         "type": "object",
#         "properties": {
#             "title": {"type": "string"},
#             "subject": {
#                 "type": "string",
#                 "enum": [
#                     "Math",
#                     "Language",
#                     "Art",
#                     "Science",
#                     "Music",
#                     "Physical",
#                     "Social-Emotional",
#                 ],
#             },
#             "duration": {
#                 "type": "string",
#                 "enum": ["5-15min", "15-30min", "30-45min", "45-60min"],
#             },
#             "groupSize": {
#                 "type": "string",
#                 "enum": ["Individual", "Small Group", "Whole Class"],
#             },
#             "description": {"type": "string"},
#             "materials": {
#                 "type": "array",
#                 "items": {"type": "string"},
#             },
#             "instructions": {
#                 "type": "array",
#                 "items": {"type": "string"},
#             },
#             "learningGoals": {
#                 "type": "array",
#                 "items": {"type": "string"},
#             },
#         },
#         "required": [
#             "title",
#             "subject",
#             "duration",
#             "groupSize",
#             "description",
#             "materials",
#             "instructions",
#             "learningGoals",
#         ],
#         "additionalProperties": False,
#     }

#     prompt = f"""
# Sen okul öncesi eğitim alanında uzman bir yardımcı asistansın.

# Görev:
# Verilen mevcut etkinliği, öğretmenin isteğine göre yeniden uyarlayacaksın.

# Kurallar:
# - Çıktıyı yalnızca verilen şemaya uygun JSON olarak üret.
# - Dil: Türkçe
# - subject yalnızca verilen enumlardan biri olsun.
# - duration yalnızca verilen enumlardan biri olsun.
# - groupSize yalnızca verilen enumlardan biri olsun.
# - Etkinlik uygulanabilir, güvenli ve pedagojik olarak uygun olsun.
# - Eski uyarlama açıklamalarını tekrar etme; temiz ve tek bir yeni açıklama yaz.

# Öğretmen Profili:
# {json.dumps(teacher_profile, ensure_ascii=False)}

# Sınıf Profili:
# {json.dumps(class_profile, ensure_ascii=False)}

# Mevcut Etkinlik:
# {json.dumps(activity, ensure_ascii=False)}

# Öğretmenin Uyarlama İsteği:
# {adaptation_prompt}
# """.strip()

#     response = client.responses.create(
#         model="gpt-4.1-mini",
#         input=prompt,
#         text={
#             "format": {
#                 "type": "json_schema",
#                 "name": "adapted_activity",
#                 "schema": schema,
#                 "strict": True,
#             }
#         },
#     )

#     raw_text = response.output_text
#     draft = json.loads(raw_text)

#     return {
#         "activity_draft": draft,
#         "source": "openai",
#     }

def adapt_activity_with_gemini(payload: dict) -> dict:
    activity = payload.get("activity", {})
    teacher_profile = payload.get("teacher_profile", {})
    class_profile = payload.get("class_profile", {})
    adaptation_prompt = (payload.get("adaptation_prompt") or "").strip()

    if not activity:
        raise ValueError("Etkinlik verisi eksik.")
    if not adaptation_prompt:
        raise ValueError("Uyarlama isteği boş olamaz.")

    schema = {
        "type": "object",
        "properties": {
            "title": {"type": "string"},
            "subject": {
                "type": "string",
                "enum": [
                    "Math",
                    "Language",
                    "Art",
                    "Science",
                    "Music",
                    "Physical",
                    "Social-Emotional",
                ],
            },
            "duration": {
                "type": "string",
                "enum": ["5-15min", "15-30min", "30-45min", "45-60min"],
            },
            "groupSize": {
                "type": "string",
                "enum": ["Individual", "Small Group", "Whole Class"],
            },
            "description": {"type": "string"},
            "materials": {
                "type": "array",
                "items": {"type": "string"},
            },
            "instructions": {
                "type": "array",
                "items": {"type": "string"},
            },
            "learningGoals": {
                "type": "array",
                "items": {"type": "string"},
            },
        },
        "required": [
            "title",
            "subject",
            "duration",
            "groupSize",
            "description",
            "materials",
            "instructions",
            "learningGoals",
        ],
    }

    prompt = f"""
Sen okul öncesi eğitim alanında uzman bir yardımcı asistansın.

Görev:
Verilen mevcut etkinliği, öğretmenin isteğine göre yeniden uyarlayacaksın.

Kurallar:
- Çıktıyı yalnızca verilen JSON şemasına uygun üret.
- Dil Türkçe olsun.
- subject yalnızca verilen enumlardan biri olsun.
- duration yalnızca verilen enumlardan biri olsun.
- groupSize yalnızca verilen enumlardan biri olsun.
- Etkinlik uygulanabilir, güvenli ve pedagojik açıdan uygun olsun.
- Önceki yapay uyarlama cümlelerini tekrar etme.
- Açıklama doğal ve tek parça olsun.

Öğretmen Profili:
{json.dumps(teacher_profile, ensure_ascii=False)}

Sınıf Profili:
{json.dumps(class_profile, ensure_ascii=False)}

Mevcut Etkinlik:
{json.dumps(activity, ensure_ascii=False)}

Öğretmenin Uyarlama İsteği:
{adaptation_prompt}
""".strip()

    response = gemini_client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=schema,
        ),
    )

    raw_text = response.text
    draft = json.loads(raw_text)

    return {
        "activity_draft": draft,
        "source": "gemini",
    }
