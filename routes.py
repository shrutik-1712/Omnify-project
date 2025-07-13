from fastapi import APIRouter, HTTPException
from typing import List
from models import BookingRequest, BookingResponse, ClassResponse, EmailRequest
from database import get_db
from utils import format_datetime_for_response

router = APIRouter()

# Route 1: Get all classes
@router.get("/classes", response_model=List[ClassResponse])
def get_classes():
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM classes')
    classes = cursor.fetchall()
    
    # Format datetime for response
    formatted_classes = []
    for row in classes:
        class_dict = dict(row)
        class_dict['datetime'] = format_datetime_for_response(class_dict['datetime'])
        formatted_classes.append(class_dict)
    
    return formatted_classes

# Route 2: Book a class
@router.post("/book")
def book_class(booking: BookingRequest):
    conn = get_db()
    cursor = conn.cursor()
    
    # Check if class exists and has available slots
    cursor.execute('SELECT * FROM classes WHERE id = ?', (booking.class_id,))
    class_row = cursor.fetchone()
    
    if not class_row:
        raise HTTPException(status_code=404, detail="Class not found")
    
    if class_row['available_slots'] <= 0:
        return {"message": "Class full"}
    
    # Check if user exists
    cursor.execute('SELECT * FROM users WHERE email = ?', (booking.email,))
    user = cursor.fetchone()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if user already booked this class
    cursor.execute('SELECT * FROM booking WHERE email = ? AND class_id = ?', 
                  (booking.email, booking.class_id))
    existing_booking = cursor.fetchone()
    
    if existing_booking:
        raise HTTPException(status_code=400, detail="Already booked for this class")
    
    # Create booking
    cursor.execute('INSERT INTO booking (username, email, class_id) VALUES (?, ?, ?)',
                  (user['name'], booking.email, booking.class_id))
    
    # Update available slots
    cursor.execute('UPDATE classes SET available_slots = available_slots - 1 WHERE id = ?',
                  (booking.class_id,))
    
    conn.commit()
    
    return {"message": "Booking successful"}

# Route 3: Get user bookings
@router.post("/booking")
def get_bookings(request: EmailRequest):
    conn = get_db()
    cursor = conn.cursor()
    
    # Check if user exists
    cursor.execute('SELECT * FROM users WHERE email = ?', (request.email,))
    user = cursor.fetchone()
    
    if not user:
        return {"message": "No classes taken by user"}
    
    # Get user bookings with class details
    cursor.execute('''
        SELECT u.name, u.email, c.name as class_name, c.datetime as date_time
        FROM booking b
        JOIN users u ON b.email = u.email
        JOIN classes c ON b.class_id = c.id
        WHERE b.email = ?
    ''', (request.email,))
    
    bookings = cursor.fetchall()
    
    if not bookings:
        return {"message": "No classes taken by user"}
    
    # Format datetime for response
    formatted_bookings = []
    for row in bookings:
        booking_dict = dict(row)
        booking_dict['date_time'] = format_datetime_for_response(booking_dict['date_time'])
        formatted_bookings.append(booking_dict)
    
    return formatted_bookings