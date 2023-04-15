# movies_auth_service
Service for Online cinema users authorisation

## Start app
- Navigate to root project folder
- docker-compose up --build

## Run tests
- Navigate to root tests/functional
- docker-compose up --build

## Create superuser example
- Start app
- Connect to app bash via - docker-compose exec flaskapp bash
- flask auth createsuperuser admin 123qwe