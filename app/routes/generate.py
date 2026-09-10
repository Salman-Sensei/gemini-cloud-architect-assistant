import os
from flask import Blueprint, request, jsonify
from google import genai
from google.genai import types

generate_bp = Blueprint("generate", __name__)

def get_genai_client():
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT") or os.environ.get("PROJECT_ID")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "europe-west1")
    return genai.Client(vertexai=True, project=project_id, location=location)

SYSTEM_INSTRUCTION = (
    "You are an expert Google Cloud Solutions Architect and DevOps engineer. "
    "Provide clear, concise, and production-ready guidance on Google Cloud services, "
    "architecture patterns, security standards, and CLI configurations. "
    "If a question is completely unrelated to cloud computing or software engineering, "
    "politely inform the user that you only answer technical Google Cloud architectural queries."
)

@generate_bp.route("/generate", methods=["POST"])
def generate_content():
    data = request.get_json() or {}
    prompt = data.get("prompt", "").strip()

    if not prompt:
        return jsonify({"status": "error", "message": "Prompt text is required."}), 400

    try:
        client = get_genai_client()
        config = types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
            temperature=0.7,
            max_output_tokens=1024,
        )
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=config,
        )
        return jsonify({
            "status": "success",
            "response": response.text
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Vertex AI API failure: {str(e)}"
        }), 500
