import os
import uuid

from django.conf import settings
from openai import OpenAI

# NIT Jamshedpur/AI/interview_utils.py

INTRO_QUESTIONS = [
    "Tell me about yourself",
    "What are your strengths?",
    "What are your weaknesses?",
]


def generate_tts(*args, **kwargs):
    """Generate TTS audio and return a media URL.

    Accepts either `generate_tts(text)` or `generate_tts(session_id, text)`.
    Returns an empty string if TTS generation fails so frontend can fall back.
    """
    # Determine arguments
    session_id = None
    text = None

    if args:
        if len(args) >= 2:
            session_id = args[0]
            text = args[1]
        else:
            text = args[0]
    else:
        session_id = kwargs.get("session_id")
        text = kwargs.get("text")

    text = (text or "").strip()
    if not text:
        return ""

    api_key = getattr(settings, "OPENAI_API_KEY", None)
    if not api_key:
        return ""

    try:
        client = OpenAI(api_key=api_key)
        tts_dir = os.path.join(settings.MEDIA_ROOT, "tts")
        os.makedirs(tts_dir, exist_ok=True)

        file_name = f"session_{session_id or 'na'}_{uuid.uuid4().hex}.mp3"
        file_path = os.path.join(tts_dir, file_name)

        # Keep request text within reasonable limits for TTS.
        tts_text = text[:1200]
        response = client.audio.speech.create(
            model="gpt-4o-mini-tts",
            voice=getattr(settings, "OPENAI_TTS_VOICE", "alloy"),
            input=tts_text,
        )

        # Handle SDK variations safely.
        if hasattr(response, "stream_to_file"):
            response.stream_to_file(file_path)
        elif hasattr(response, "read"):
            with open(file_path, "wb") as f:
                f.write(response.read())
        elif hasattr(response, "content"):
            with open(file_path, "wb") as f:
                f.write(response.content)
        else:
            return ""

        return f"{settings.MEDIA_URL}tts/{file_name}"
    except Exception:
        return ""
