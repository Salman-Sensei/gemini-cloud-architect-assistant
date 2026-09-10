import os
import logging


class Config:
    """Centralized configuration, read once at startup with sane defaults."""

    PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT") or os.environ.get("PROJECT_ID")
    LOCATION = os.environ.get("GOOGLE_CLOUD_LOCATION", "europe-west1")
    MODEL_NAME = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")

    MAX_PROMPT_LENGTH = 2000
    HISTORY_SIZE = 10
    CACHE_SIZE = 64

    @classmethod
    def validate(cls):
        """Raise a clear error early if required config is missing,
        instead of letting a cryptic Vertex AI auth error surface later."""
        if not cls.PROJECT_ID:
            raise RuntimeError(
                "GOOGLE_CLOUD_PROJECT is not set. "
                "Export it before running: export GOOGLE_CLOUD_PROJECT=<your-project-id>"
            )


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
    return logging.getLogger("gemini-app")