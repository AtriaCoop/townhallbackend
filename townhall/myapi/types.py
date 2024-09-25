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
    title: str
    description: str
    start_time: datetime
    end_time: datetime
    location: str
    organization_id: int


@dataclass
class UpdateOpportunityData:
    id: int
    title: str
    description: str
    start_time: datetime
    end_time: datetime
    location: str
    organization_id: int


@dataclass
class FilteredOpportunityData:
    title: Optional[str] = None
    starting_start_time: Optional[datetime] = None
    starting_end_time: Optional[datetime] = None
    ending_start_time: Optional[datetime] = None
    ending_end_time: Optional[datetime] = None
    location: Optional[str] = None
    organization_id: Optional[int] = None


@dataclass
class CreateOrganizationData:
    name: str
    location: str
    email: str
    phone_number: str
    website: str


@dataclass
class UpdateOrganizationData:
    id: int
    name: str
    location: str
    email: str
    phone_number: str
    website: str


@dataclass
class FilteredOrganizationData:
    name: Optional[str] = None
    location: Optional[str] = None
