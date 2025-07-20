# Contact Manager System - 2025

This simple Flask application lets each user manage their own contacts. Users
must register and log in before creating or viewing contacts. Authentication is
handled via signed cookies and every contact is associated with the current
user.

## Endpoints

- `POST /register` – create a new user.
- `POST /login` – authenticate and start a session.
- `POST /logout` – end the current session.
- `POST /contacts` – create a contact for the logged in user.
- `GET /contacts` – list your contacts.
- `GET /contacts/<id>` – retrieve a specific contact (only if it is yours).