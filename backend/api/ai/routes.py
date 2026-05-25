from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

import os
from backend.services.ai_service import (
    generate_recommendation_explanation, 
    adapt_activity_mock, 
    adapt_activity_with_gemini,  #adapt_activity_with_llm
)

from backend.utils.auth_middleware import roles_required

ai_bp = Blueprint("ai", __name__)


@ai_bp.route("/explain-recommendations", methods=["POST"])
@jwt_required()
@roles_required("teacher")
def explain_recommendations_route():
    data = request.get_json() or {}

    result = generate_recommendation_explanation(data)

    if result.get("success"):
        return jsonify(result), 200

    return jsonify({"error": result.get("error", "AI explanation failed")}), 400

@ai_bp.route("/adapt-activity", methods=["POST"])
@jwt_required()
@roles_required("teacher")
def adapt_activity():
    data = request.get_json() or {}

    try:
#         if os.getenv("OPENAI_API_KEY"):
          if os.getenv("GEMINI_API_KEY"):  
            try:
                result = adapt_activity_with_gemini(data)
                print("Adapt source:", result.get("source"))
                return jsonify(result), 200
            except Exception as gemini_error:
                print(f"Gemini adapt hatası, mock fallback kullanılacak: {gemini_error}")

#                 result = adapt_activity_with_llm(data)
#                 print("Adapt source:", result.get("source"))
#                 print("LLM draft title:", result.get("activity_draft", {}).get("title"))
#                 return jsonify(result), 200
#             except Exception as llm_error:
#                 print(f"LLM adapt hatası, mock fallback kullanılacak: {llm_error}")


          result = adapt_activity_mock(data)
          print("Adapt source:", result.get("source"))
          return jsonify(result), 200
    
    except ValueError as error:
        return jsonify({"error": str(error)}), 400
    except Exception as error:
        print(f"Adapt activity error: {error}")
        return jsonify({"error": "Etkinlik uyarlanamadı."}), 500

