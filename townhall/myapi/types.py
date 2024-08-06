from typing import Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class CreateVolunteerData:
    first_name: str
    last_name: str
    gender: str
    email: str

@dataclass
class UpdateVolunteerData:
    id: int
    first_name: str
    last_name: str
    gender: str
    email: str

@dataclass
class CreateOpportunityData:
    name: str
    time: datetime
    description: str
    location: str

@dataclass
class UpdateOpportunityData:
    id: int
    name: str
    time: datetime
    description: str
    location: str

@dataclass
class FilteredOpportunityData:
    name: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    location: Optional[str] = None

@dataclass
class CreateOrganizationData:
    name: str
    location: str
    description: str
    email: str

@dataclass
class UpdateOrganizationData:
    id: int
    name: str
    location: str
    description: str
    email: str

@dataclass
class FilteredOrganizationData:
    name: Optional[str] = None
    location: Optional[str] = None


