# Deployed Service link: https://orders-sms-service.onrender.com

# Django Order Management System

<p>This project is a Django REST API for managing customers and orders, with secure user authentication via OIDC with Auth0 and SMS  service using Africa's Talking.<p>

## Project Overview
* Purpose: Build a REST API to manage customers and orders, with Auth0 for user authentication and Africa's Talking for sending SMS notifications when orders are created.
* Tech Stack
  - Backend Framework & Core
    - Djngo 4.2+ - Web framework
    - Django REST Framework 3.14+ - API framework for building REST APIs
    - Python 3.8+ - Programming language
  - Database Layer
    - SQLite (development/testing, built into Django)
    - **PostgreSQL** (for production) with psycopg2-binary
  - API Integration & Communication
    - **Africa's Talking SMS API** - SMS gateway service
    - Requests library - HTTP client for API calls
    - **REST API endpoints** - Communication protocol
  - Development Tools
    - mozilla-django-oidc with Auth0 for OpenID Connect (OIDC)
  - Testing & Quality
    - **pytest** - Testing framework
    - pytest-django - Django-specific testing tools
    - Postman - API testing tool
  - Configuration management
    - **Ansible** used for dependency installation and migrations

  - Production & Deployment
    - Gunicorn - WSGI HTTP server
    - Apache/Nginx - Web server
  - Architecture Pattern
    - REST API Architecture - Resource-oriented URLs, HTTP methods, JSON responses
    - MVC Pattern - Models, Views, Serializers separation
    - Client-Server Architecture - Stateless communication
  - External Services
    - Africa's Talking Sandbox - Testing environment
    - Africa's Talking Production API - Live SMS service
    - Simulator - Message testing platform
  - Data Flow
    - Frontend/Client → Django REST API → Database
    - Django API → Africa's Talking SMS API → Customer's Phone
    - Webhook callbacks → Django API (for delivery reports)
  - Development Environment
    - Virtual Environment (venv/virtualenv)
    - Git - Version control
    - IDE/Editor (VS Code)

## Feat 1: Project Setup
* Initialized Django project and app.
* Set up SQLite database.
* Created models for customers (name, code, phone) and orders (customer, item, amount, time).
* Built REST API endpoints for customers and orders using Django REST Framework.
* Added a homepage with login and dashboard templates.
* Installed dependencies and configured environment variables.

## Feat 2: Auth0 Authentication
* Integrated Auth0 for secure authentication using mozilla-django-oidc.
* Configured authentication settings and environment variables for Auth0 client ID and secret.
* Added OIDC routes for login, callback, and logout.
* Created templates for login (with Auth0 link) and dashboard (showing user info and logout).
* Fixed an HTTP 405 error on logout by using a form-based POST request instead of a direct link.
* Tested login flow: users authenticate via Auth0 and access the dashboard.

## Feat 3: SMS Integration
* Signed up for Africa's Talking sandbox and obtained API key and username.
* Installed Africa's Talking Python SDK and configured credentials in environment variables.
* Added SMS sending when an order is created via the API, notifying the customer with order details (item, amount, time).
* Created a service class to handle SMS logic, resolving a sandbox error ("Sandbox is currently not available") by moving initialization to the class constructor.
* Faced a token expiration error in Postman ("The token has expired"); resolved by refreshing the Auth0 token.
* Planned to test SMS delivery using Postman and verify in the Africa's Talking sandbox dashboard or simulator.
* Noted potential sandbox issues due to reported SMS service degradation; prepared to mock SMS for testing if needed.

## Feat 4: Testing and CI/CD pipeline
- **Unit Tests**: Tests cover Customer/Order models, serializers, views (GET, POST, DELETE), and SMS integration. 
- Achieved a 80.28% coverage using `pytest-django` and `pytest-cov`.
- Mocked SMS for reliability.  (see `htmlcov/index.html`).
- Run: `pytest --cov=core --cov-report=html`.
- **Triggers**: Set up GitHub Actions (`.github/workflows/ci-cd.yml`) to run `ci-tests` on PRs tp `main` and `dev` (tests, Ansible). Configured secrets for Auth0 and Africa's Talking.
- Runs `ci-test` and `cd-deploy` on pushes to `main` (Render deployment)
- **Testing Instructions**:
  1. Push code to GitHub `dev` branch or `main` branch.
  2. Check GitHub Actions for test results and coverage.

## Container Runtime 
- **Tool**: Colima (suitable macOS Monterey 12.7.6, alternative to Docker Desktop which requires later MacOS versions)
- **Setup**: `brew install colima docker`, then `colima start --cpu 2 --memory 4`.
- **Usage**: Runs Docker-compatible containers for development and GAE deployment.
- **Troubleshooting**: Resolved QEMU errors via `brew install qemu` or `colima delete`.

## Testing Instructions
- (for customer and order creation and Africas talking sms)
1. Use Postman to get a fresh Auth0 token via OAuth 2.0.
1. Create a customer via the API with a name, unique code, and registered phone number.
1. Create an order via the API, linking to the customer.
1. Check the Africa's Talking sandbox dashboard (Outbound Messages) or simulator for the SMS.
1. Review server logs for SMS success or failure messages.

 ## Maintenance

- Africa's Talking sandbox may be unavailable due to service degradation; monitor status page and contact support if needed.
- Auth0 tokens expire (default 24 hours); refresh in Postman before testing.

