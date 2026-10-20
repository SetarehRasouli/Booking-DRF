# Booking API (Django REST Framework)

A backend REST API for an appointment booking system, built with Django and Django REST Framework. This project focuses on solving real-world concurrency challenges — specifically preventing double-booking when multiple users try to reserve the same time slot simultaneously.

## Key Engineering Highlight: Race Condition Protection

The core challenge of this project is: **what happens when two users try to book the exact same time slot at the exact same moment?**

A naive `if slot.is_available` check in Python code is not enough — there's always a gap between reading and writing that a second request can slip through. This project solves it at the database level with a `unique_together` constraint on `(provider, time)`, combined with a `transaction.atomic()` block that catches the resulting `IntegrityError` and converts it into a clean, user-friendly API response instead of a server crash.

This was verified with a real concurrency test — two simultaneous requests fired via Python's `threading` module — confirming that exactly one request succeeds (201) and the other is correctly rejected (400).

## Features

### Authentication (`user` app)
- User registration
- JWT-based login (access & refresh tokens)
- Become-a-Provider endpoint (any registered user can create a Provider profile)

### Booking (`booking` app)
- **Dynamic slot calculation**: available time slots are computed on-the-fly from the provider's working hours, existing bookings, and manually blocked times — not pre-generated and stored
- **Booking**: full CRUD, restricted to authenticated users
- **Race condition protection**: database-level uniqueness constraint prevents double-booking under concurrent requests
- **Manual blocking**: providers can block specific time ranges (e.g. for a break or day off)

## Tech Stack
- Python, Django, Django REST Framework
- SQLite (development)
- Simple JWT (`djangorestframework-simplejwt`) for authentication
- drf-spectacular for auto-generated API documentation (Swagger)
- python-decouple for environment variable management

## API Documentation
Interactive API docs are available via Swagger UI at:


## Endpoints Overview

| Endpoint | Method | Description |
|---|---|---|
| `/register/` | POST | Register a new user |
| `/login/` | POST | Obtain JWT access & refresh tokens |
| `/login/refresh/` | POST | Refresh an expired access token |
| `/become-provider/` | POST | Create a Provider profile for the logged-in user |
| `/providers/<id>/available-slots/?date=YYYY-MM-DD` | GET | Get dynamically calculated available slots for a provider on a given date |
| `/bookings/` | GET, POST | List or create bookings |
| `/bookings/<id>/` | GET, PATCH, DELETE | Retrieve, update, or delete a booking |



## Setup & Installation

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/Booking-DRF.git
cd Booking-DRF
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root:



5. Run migrations and start the server:
```bash
python manage.py migrate
python manage.py runserver
```

## Testing
All endpoints were manually tested using Postman. A Postman collection is included in this repo (`postman_collection.json`) for quick testing.

Race condition handling was additionally verified with a concurrency test script using Python's `threading` module, simulating two simultaneous booking requests for the same slot.



## Running with Docker

### Prerequisites
- Docker and Docker Compose


2. Create your environment file and fill in the values:
```bash
   cp .env.example .env
```
3. Build and start the containers:
```bash
   docker compose up --build
```
4. The API will be available at http://localhost:8000

### Environment variables
| Variable | Description |
|---|---|
| `SECRET_KEY` | Django secret key |
| `DEBUG` | `True` for development |
| `DB_NAME` | Database name |
| `DB_USER` | Database user |
| `DB_PASSWORD` | Database password |

### Useful commands
```bash
# Run migrations (if not run automatically)
docker compose exec web python manage.py migrate

# Create an admin user
docker compose exec web python manage.py createsuperuser

# Run tests
docker compose exec web python manage.py test

# Stop the containers
docker compose down

# Stop and delete the database volume
docker compose down -v
```

## Author
[Setareh Rasouli] — [https://github.com/setarehrasouli]