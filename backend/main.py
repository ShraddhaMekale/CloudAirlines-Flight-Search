from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Airlines API")

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Flight(BaseModel):
    id: str
    airline: str
    origin: str
    destination: str
    price: float
    time: str

mock_flights = [
    Flight(id="FL101", airline="SkyHigh Airlines", origin="New York (JFK)", destination="London (LHR)", price=450.00, time="08:00 AM"),
    Flight(id="FL202", airline="Oceanic Air", origin="Los Angeles (LAX)", destination="Tokyo (HND)", price=850.50, time="10:30 PM"),
    Flight(id="FL303", airline="Continental", origin="Chicago (ORD)", destination="Paris (CDG)", price=520.00, time="05:45 PM"),
    Flight(id="FL404", airline="SkyHigh Airlines", origin="Miami (MIA)", destination="Sao Paulo (GRU)", price=320.00, time="11:15 AM"),
    Flight(id="FL505", airline="Global Airways", origin="San Francisco (SFO)", destination="Sydney (SYD)", price=1050.00, time="11:55 PM"),
]

@app.get("/api/flights", response_model=List[Flight])
def get_flights():
    return mock_flights

@app.get("/api/health")
def health_check():
    return {"status": "ok"}
