from pydantic import BaseModel

class BookingRequest(BaseModel):
    email: str
    class_id: int

class BookingResponse(BaseModel):
    name: str
    email: str
    class_name: str
    date_time: str

class ClassResponse(BaseModel):
    id: int
    name: str
    instructor_name: str
    datetime: str
    max_slots: int
    available_slots: int

class EmailRequest(BaseModel):
    email: str