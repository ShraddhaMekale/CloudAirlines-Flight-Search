from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uuid

app = FastAPI(title="Airlines API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class Flight(BaseModel):
    id: str
    airline: str
    origin: str
    destination: str
    price: float
    time: str

class Passenger(BaseModel):
    name: str
    email: str
    passport: str

class BookingRequest(BaseModel):
    flight_id: str
    passenger: Passenger
    seat: str
    meal: str
    discount_code: Optional[str] = None

class BookingResponse(BaseModel):
    booking_id: str
    flight: Flight
    passenger: Passenger
    seat: str
    meal: str
    original_price: float
    discount_applied: float
    final_price: float
    status: str

# Mock Data
mock_flights = [
    Flight(id="FL101", airline="SkyHigh Airlines", origin="New York (JFK)", destination="London (LHR)", price=450.00, time="08:00 AM"),
    Flight(id="FL202", airline="Oceanic Air", origin="Los Angeles (LAX)", destination="Tokyo (HND)", price=850.50, time="10:30 PM"),
    Flight(id="FL303", airline="Continental", origin="Chicago (ORD)", destination="Paris (CDG)", price=520.00, time="05:45 PM"),
    Flight(id="FL404", airline="SkyHigh Airlines", origin="Miami (MIA)", destination="Sao Paulo (GRU)", price=320.00, time="11:15 AM"),
    Flight(id="FL505", airline="Global Airways", origin="San Francisco (SFO)", destination="Sydney (SYD)", price=1050.00, time="11:55 PM"),
]

DISCOUNT_CODES = {
    "FLY20": 0.20,
    "SAVE10": 0.10,
    "WELCOME50": 0.50
}

MEALS = ["Standard", "Vegetarian", "Vegan", "Halal", "Kosher", "Low Fat"]
SEATS = [f"{row}{col}" for row in range(1, 21) for col in "ABCDEF"]

# Endpoints
@app.get("/api/flights", response_model=List[Flight])
def get_flights():
    return mock_flights

@app.get("/api/flights/{flight_id}/seats")
def get_seats(flight_id: str):
    # In a real app, filter by flight_id and check booked seats
    return {"seats": SEATS[:30]} # Return first 30 for simplicity

@app.get("/api/meals")
def get_meals():
    return {"meals": MEALS}

@app.post("/api/bookings", response_model=BookingResponse)
def create_booking(request: BookingRequest):
    flight = next((f for f in mock_flights if f.id == request.flight_id), None)
    if not flight:
        raise HTTPException(status_code=404, detail="Flight not found")
    
    original_price = flight.price
    discount_pct = DISCOUNT_CODES.get(request.discount_code, 0.0) if request.discount_code else 0.0
    discount_amount = original_price * discount_pct
    final_price = original_price - discount_amount
    
    booking = BookingResponse(
        booking_id=str(uuid.uuid4())[:8].upper(),
        flight=flight,
        passenger=request.passenger,
        seat=request.seat,
        meal=request.meal,
        original_price=original_price,
        discount_applied=discount_amount,
        final_price=final_price,
        status="Confirmed"
    )
    return booking

@app.get("/api/health")
def health_check():
    return {"status": "ok"}
