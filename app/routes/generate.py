import os
import json
import time
import base64
import logging
from collections import deque
from functools import lru_cache

from flask import Blueprint, request, jsonify
from google import genai
from google.genai import types
from google.oauth2 import service_account

from app.config import Config

generate_bp = Blueprint("generate", __name__)
logger = logging.getLogger("gemini-app")

_history = deque(maxlen=Config.HISTORY_SIZE)

_stats = {
    "total_requests": 0,
    "cache_hits": 0,
    "errors": 0,
}

SYSTEM_INSTRUCTION = (
    "You are an expert Google Cloud Solutions Architect and DevOps engineer. "
    "Provide clear, concise, and production-ready guidance on Google Cloud services, "
    "architecture patterns, security standards, and CLI configurations. "
    "If a question is completely unrelated to cloud computing or software engineering, "
    "politely inform the user that you only answer technical Google Cloud architectural queries."
)


def get_genai_client():
    creds_b64 = os.environ.get("GOOGLE_CREDENTIALS_B64")

    if creds_b64:
        creds_json = base64.b64decode(creds_b64).decode("utf-8")
        credentials = service_account.Credentials.from_service_account_info(
            json.loads(creds_json),
            scopes=["https://www.googleapis.com/auth/cloud-platform"],
        )
        return genai.Client(
            vertexai=True,
            project=Config.PROJECT_ID,
            location=Config.LOCATION,
            credentials=credentials,
        )

    return genai.Client(vertexai=True, project=Config.PROJECT_ID, location=Config.LOCATION)


@lru_cache(maxsize=Config.CACHE_SIZE)
def _cached_generate(prompt: str) -> str:
    client = get_genai_client()
    config = types.GenerateContentConfig(
        system_instruction=SYSTEM_INSTRUCTION,
        temperature=0.7,
        max_output_tokens=1024,
    )
    response = client.models.generate_content(
        model=Config.MODEL_NAME,
        contents=prompt,
        config=config,
    )
    return response.text


@generate_bp.route("/generate", methods=["POST"])
def generate_content():
    data = request.get_json() or {}
    prompt = data.get("prompt", "").strip()

    if not prompt:
        return jsonify({"status": "error", "message": "Prompt text is required."}), 400

    if len(prompt) > Config.MAX_PROMPT_LENGTH:
        return jsonify({
            "status": "error",
            "message": f"Prompt too long ({len(prompt)} chars). Limit is {Config.MAX_PROMPT_LENGTH}."
        }), 400

    _stats["total_requests"] += 1
    cache_info_before = _cached_generate.cache_info().hits
    start = time.perf_counter()

    try:
        answer = _cached_generate(prompt)
        elapsed = round(time.perf_counter() - start, 3)

        was_cache_hit = _cached_generate.cache_info().hits > cache_info_before
        if was_cache_hit:
            _stats["cache_hits"] += 1

        logger.info("prompt_len=%d elapsed=%.3fs cache_hit=%s", len(prompt), elapsed, was_cache_hit)

        _history.append({
            "prompt": prompt[:120],
            "response_preview": answer[:160],
            "cached": was_cache_hit,
            "elapsed_seconds": elapsed,
        })

        return jsonify({"status": "success", "response": answer, "cached": was_cache_hit}), 200

    except Exception as e:
        _stats["errors"] += 1
        logger.error("Vertex AI call failed: %s", str(e))
        return jsonify({"status": "error", "message": f"Vertex AI API failure: {str(e)}"}), 500


@generate_bp.route("/history", methods=["GET"])
def history():
    return jsonify({"status": "success", "history": list(_history)}), 200


@generate_bp.route("/stats", methods=["GET"])
def stats():
    cache_info = _cached_generate.cache_info()
    return jsonify({
        "status": "success",
        "total_requests": _stats["total_requests"],
        "cache_hits": _stats["cache_hits"],
        "errors": _stats["errors"],
        "cache_size": cache_info.currsize,
        "cache_max_size": cache_info.maxsize,
    }), 200