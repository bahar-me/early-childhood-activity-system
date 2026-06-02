from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

import os
from backend.services.ai_service import (
    generate_recommendation_explanation, 
    adapt_activity_mock, 
    adapt_activity_with_gemini,  
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

    return jsonify({"error": result.get("error", "YZ Açıklaması oluşturulamadı")}), 400

@ai_bp.route("/adapt-activity", methods=["POST"])
@jwt_required()
@roles_required("teacher")
def adapt_activity():
    data = request.get_json() or {}

    try:
          if os.getenv("GEMINI_API_KEY"):  
            try:
                result = adapt_activity_with_gemini(data)
                return jsonify(result), 200
            except Exception as gemini_error:
                print(f"Gemini adapt hatası, mock fallback kullanılacak: {gemini_error}")

          result = adapt_activity_mock(data)
          return jsonify(result), 200
    
    except ValueError as error:
        return jsonify({"error": str(error)}), 400
    except Exception as error:
        print(f"Adapt activity error: {error}")
        return jsonify({"error": "Etkinlik uyarlanamadı."}), 500

