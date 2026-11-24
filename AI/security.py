from functools import wraps
from hashlib import sha256
from time import time

from django.conf import settings
from django.core.cache import cache
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404

from .models import InterviewSession


def owned_interview(request, session_id):
    try:
        session_id = int(session_id)
    except (ValueError, TypeError, OverflowError):
        raise Http404("Interview not found")
    if request.user.is_authenticated:
        return get_object_or_404(InterviewSession, pk=session_id, user=request.user)
    if request.session.get("interview_session_id") != session_id:
        raise Http404("Interview not found")
    return get_object_or_404(InterviewSession, pk=session_id, user__isnull=True)


def rate_limit(scope, limit):
    """Fixed-window limit. Shared cache required for multiple workers."""
    def decorate(view):
        @wraps(view)
        def wrapped(request, *args, **kwargs):
            maximum = getattr(settings, "AI_RATE_LIMITS", {}).get(scope, limit)
            window = int(time() // 60)
            identities = ["ip:" + request.META.get("REMOTE_ADDR", "unknown")]
            if request.user.is_authenticated:
                identities.append("user:" + str(request.user.pk))
            for identity in identities:
                digest = sha256(identity.encode()).hexdigest()
                key = f"ai-limit:{scope}:{window}:{digest}"
                cache.add(key, 0, timeout=120)
                try:
                    count = cache.incr(key)
                except ValueError:
                    return JsonResponse({"error": "Please retry shortly."}, status=503)
                if count > maximum:
                    response = JsonResponse({"error": "Too many requests. Please retry shortly."}, status=429)
                    response["Retry-After"] = str(60 - int(time()) % 60)
                    return response
            return view(request, *args, **kwargs)
        return wrapped
    return decorate
