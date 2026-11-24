from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import include, path
from django.views.decorators.http import require_safe


def root_redirect(_request):
    return redirect("ai-mock-interview")


def preview_page(template):
    @require_safe
    def view(request):
        return render(request, template)
    return view


def preview_unavailable(_request, **_kwargs):
    return HttpResponse(
        "Read-only portfolio preview. Live interview features require server-side AI configuration.",
        status=503,
        content_type="text/plain",
    )


if settings.OPENAI_API_KEY:
    interview_urls = "AI.urls"
else:
    # Public UI-only showcase. Do not import AI clients or expose interview
    # state, voice processing, feedback or mutations without configuration.
    interview_urls = [
        path("", preview_page("ai/ai_mock_interview.html"), name="ai_index"),
        path("ai-mock-interview/", preview_page("ai/ai_mock_interview.html"), name="ai-mock-interview"),
        path("ai-interview-select/", preview_page("ai/ai_interview_select.html"), name="ai-interview-select"),
        path("interview-preparation/", preview_page("ai/interview_preparation.html"), name="interview-preparation"),
        path("interview-preparation/types/", preview_unavailable, name="interview-types"),
        path("interview-preparation/tips/", preview_unavailable, name="interview-tips"),
        path("interview-preparation/myths/", preview_unavailable, name="interview-myths"),
        path("interview-preparation/question-bank/", preview_unavailable, name="interview-question-bank"),
        path("interview-preparation/resume-prep/", preview_unavailable, name="interview-resume-prep"),
        path("interview-preparation/communication/", preview_unavailable, name="interview-communication"),
        path("ai-interview-config/<str:interview_type>/", preview_unavailable, name="ai-interview-config"),
        path("ai-interview-start/", preview_unavailable, name="ai-interview-start"),
        path("ai-interview-live/", preview_unavailable, name="ai-interview-live"),
        path("voice/next/", preview_unavailable, name="ai-voice-next"),
        path("voice/hint/", preview_unavailable, name="ai-voice-hint"),
        path("voice/skip/", preview_unavailable, name="ai-voice-skip"),
        path("stt/", preview_unavailable, name="ai-stt"),
        path("finish/", preview_unavailable, name="finish_interview"),
        path("feedback/<int:session_id>/", preview_unavailable, name="interview-feedback"),
        path("feedback/<int:session_id>/details/", preview_unavailable, name="interview-feedback-details"),
        path("feedback/<int:session_id>/details/<int:question_index>/reference-answer/", preview_unavailable, name="interview-reference-answer"),
        path("feedback/<int:session_id>/download/", preview_unavailable, name="interview-feedback-download"),
        path("submit_code/", preview_unavailable, name="ai_submit_code"),
    ]


urlpatterns = [
    path("", root_redirect),
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("ai/", include(interview_urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
