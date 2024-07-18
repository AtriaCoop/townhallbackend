from dataclasses import dataclass
from datetime import datetime

@dataclass
class CreateVolunteerData:
    first_name: str
    last_name: str
    gender: str
    age: int
    email: str

@dataclass
class UpdateVolunteerData:
    first_name: str
    last_name: str
    gender: str
    age: int
    email: str

@dataclass
class CreateOpportunityData:
    name: str
    time: datetime
    description: str
    location: str