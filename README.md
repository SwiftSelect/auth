# SwiftSelect Auth Service

The authentication and authorization service for SwiftSelect, handling user authentication, authorization, and session management.

## Overview

This service provides:
- User authentication (login/signup)
- JWT token management
- Role-based access control
- Session management
- Password hashing and security

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- JWT for token management
- Pydantic for data validation

## Prerequisites

- Python 3.8+
- pip (Python package manager)
- Virtual environment (recommended)

## Setup

1. Create and activate a virtual environment:
```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file in the root directory with the following variables:
```
DATABASE_USER=
DATABASE_PASSWORD=
DATABASE_HOST=
DATABASE_PORT=
SECRET_KEY=
```

## Running the Service

Development server:
```bash
uvicorn app.main:app --reload
```

Production server:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## API Documentation

Once the server is running, you can access:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Testing

Run tests using pytest:
```bash
pytest
```

## Security Considerations

- All passwords are hashed using bcrypt
- JWT tokens are used for stateless authentication
- Rate limiting is implemented for security
- CORS is properly configured
- Input validation is enforced

## Contributing

1. Create a new branch for your feature
2. Make your changes
3. Add tests for new functionality
4. Submit a pull request

## License

This project is proprietary and confidential.
