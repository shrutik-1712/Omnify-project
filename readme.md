# Class Booking System API

A FastAPI-based class booking system with SQLite3 in-memory database.

## Project Structure

```
├── main.py           # FastAPI application entry point
├── routes.py         # API route handlers
├── models.py         # Pydantic models for request/response
├── database.py       # Database connection and setup
├── requirements.txt  # Python dependencies
└── README.md        # Project documentation
```

## Features

- **In-memory SQLite3 database** (no SQLAlchemy)
- **Three main API endpoints**:
  - `GET /classes` - View all available classes
  - `POST /book` - Book a class for a user
  - `POST /booking` - View user's bookings
- **Thread-safe database connections**
- **Proper error handling**
- **Sample data pre-populated**

## Database Schema

### Classes Table
- `id` - Primary key
- `name` - Class name
- `instructor_name` - Instructor name
- `datetime` - Class date and time
- `max_slots` - Maximum available slots
- `available_slots` - Current available slots

### Users Table
- `id` - Primary key
- `email` - User email (unique)
- `name` - User name
- `classes_enrolled` - Classes enrolled (nullable)

### Booking Table
- `id` - Primary key
- `username` - User name
- `email` - User email
- `class_id` - Foreign key to classes table

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python main.py
```

The API will be available at `http://localhost:8000` with automatic documentation at `http://localhost:8000/docs`.

## API Endpoints

### 1. GET /classes
Returns all available classes.

**Response:**
```json
[
  {
        "id": 1,
        "name": "Yoga Basics",
        "instructor_name": "John Doe",
        "datetime": "2025-07-14 09:00:00 IST",
        "max_slots": 20,
        "available_slots": 15
    },
]
```

### 2. POST /book
Book a class for a user.

**Request Body:**
```json
{
  "email": "john@example.com",
  "class_id": 1
}
```

**Responses:**
- Success: `{"message": "Booking successful"}`
- Class full: `{"message": "Class full"}`
- User not found: `404 - User not found`
- Already booked: `400 - Already booked for this class`

### 3. POST /booking
Get user's bookings.

**Request Body:**
```json
{
  "email": "john@example.com"
}
```

**Responses:**
- Success:
```json
[
  {
    "name": "John User",
    "email": "john@example.com",
    "class_name": "Yoga Basics",
    "date_time": "2025-07-14 09:00:00 IST"
  }
]
```
- No bookings: `{"message": "No classes taken by user"}`
