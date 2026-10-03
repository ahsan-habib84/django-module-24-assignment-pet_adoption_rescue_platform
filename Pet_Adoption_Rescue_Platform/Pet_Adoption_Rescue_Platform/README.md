# Pet Adoption & Rescue Platform

Django + Django REST Framework assignment project.

## Features
- User registration, login, logout, profile
- Pet list, details, image upload
- Pet search/filter by name, animal type, breed, gender, location, status
- Adoption request form
- My Adoption Requests dashboard
- Business rules for available pets and duplicate active requests
- Django Admin for pets/adoption requests
- REST API for pets and adoption requests
- API search/filter
- Pagination
- DRF Token Authentication

## Setup

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open:
- Website: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/
- API: http://127.0.0.1:8000/api/pets/

For development, uploaded media is served automatically by Django when DEBUG=True.

## API Authentication
Obtain a token:
POST `/api/token/`
with JSON:
```json
{"username":"your_username","password":"your_password"}
```

Then use:
`Authorization: Token YOUR_TOKEN`

## API endpoints
- GET/POST `/api/pets/`
- GET/PUT/DELETE `/api/pets/<id>/`
- GET/POST `/api/adoptions/`
- GET/PUT `/api/adoptions/<id>/`
- GET `/api/pets/?search=golden`
- GET `/api/pets/?animal_type=Dog`
- GET `/api/pets/?gender=Male`
