# AI Interview

> **AI-powered mock interview application built with Django and OpenAI, with session-based interview flows and production deployment configuration.**

**Developer:** SSVPrasad  
**Stack:** Django · Python · OpenAI · JavaScript · Gunicorn · WhiteNoise

## Product Overview

AI Interview provides a structured interview-practice experience with AI-generated questions, interview sessions and feedback-oriented workflows.

The project focuses on integrating AI into a real web application while handling session state, request security and production deployment.

## What I Built

- Django-based interview application
- OpenAI integration for AI-powered interview interactions
- Session-based interview state
- CSRF-aware request handling
- Production configuration for hosted deployment
- Gunicorn application server setup
- WhiteNoise static-file serving
- Environment-based configuration for deployment

## Engineering Focus

**AI application development**  
Integrating model-powered interactions into a structured user workflow.

**Backend engineering**  
Building Django views, session flows and application logic around the interview lifecycle.

**Security**  
Handling CSRF-aware requests and authenticated/session state safely.

**Deployment**  
Preparing the application for production hosting with Gunicorn, WhiteNoise and environment configuration.

## Tech Stack

| Layer | Technologies |
|---|---|
| Backend | Python · Django |
| AI | OpenAI API |
| Web | HTML · CSS · JavaScript |
| Production | Gunicorn · WhiteNoise · Render |

## Run Locally

```bash
git clone https://github.com/ssvprasad144/AI_interview.git
cd AI_interview
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Set the required environment variables before enabling OpenAI-powered functionality.

## Developer

**SSVPrasad**  
Full-Stack Developer · AI Integration · Backend Engineering

GitHub: https://github.com/ssvprasad144

## Security hardening branch

Local development: set DJANGO_DEBUG=1 and OPENAI_API_KEY in .env. Production requires a random DJANGO_SECRET_KEY of at least 50 characters, DJANGO_ALLOWED_HOSTS, HTTPS, and REDIS_URL with the redis Python package installed for shared rate limits. Set DJANGO_TRUST_PROXY=1 only behind a trusted proxy that sanitizes forwarded headers. Configure DJANGO_CSRF_TRUSTED_ORIGINS if needed. IP limits use REMOTE_ADDR; configure the deployment to expose trusted client addresses or use edge rate limiting. Default limits are per minute and can be tuned in AI_RATE_LIMITS. Guest access is restricted to the active interview; signed-in access is restricted to owned records. Signing in mid-guest-interview does not transfer ownership. Feedback is browser-session scoped. Run Django tests and browser smoke tests before deployment. Review public media and historical summary files separately.
