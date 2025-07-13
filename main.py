from fastapi import FastAPI
from routes import router

app = FastAPI(title="Class Booking System")

# Include all routes
app.include_router(router)

# Health check endpoint
@app.get("/")
def root():
    return {"message": "Class Booking System API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)