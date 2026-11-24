from django.test import TestCase, Client, override_settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from .models import InterviewSession


@override_settings(SECURE_SSL_REDIRECT=False, SESSION_COOKIE_SECURE=False, CSRF_COOKIE_SECURE=False)
class SecurityTests(TestCase):
    def setUp(self):
        cache.clear()
        self.user = get_user_model().objects.create_user(username="owner", password="test-password-123")
        self.record = InterviewSession.objects.create(user=self.user, interview_type="technical")

    def test_guest_cannot_read_owned_feedback(self):
        self.assertEqual(self.client.get(f"/ai/feedback/{self.record.pk}/details/").status_code, 404)

    def test_other_user_cannot_read_owned_feedback(self):
        other = get_user_model().objects.create_user(username="other")
        self.client.force_login(other)
        self.assertEqual(self.client.get(f"/ai/feedback/{self.record.pk}/details/").status_code, 404)

    def test_guest_can_read_active_feedback(self):
        record = InterviewSession.objects.create(interview_type="technical")
        session = self.client.session
        session["interview_session_id"] = record.pk
        session.save()
        self.assertEqual(self.client.get(f"/ai/feedback/{record.pk}/").status_code, 200)

    def test_csrf_required(self):
        client = Client(enforce_csrf_checks=True)
        self.assertEqual(client.post("/ai/voice/next/", {}, content_type="application/json").status_code, 403)

    @override_settings(AI_RATE_LIMITS={"voice": 1})
    def test_rate_limit(self):
        self.client.post("/ai/voice/next/", {"session_id": self.record.pk}, content_type="application/json")
        self.assertEqual(self.client.post("/ai/voice/next/", {"session_id": self.record.pk}, content_type="application/json").status_code, 429)
