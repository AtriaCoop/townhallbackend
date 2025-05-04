from typing import Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class CreateVolunteerData:
    first_name: str
    last_name: str
    gender: str
    email: str
    password: str


@dataclass
class UpdateVolunteerData:
    id: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    gender: Optional[str] = None
    email: Optional[str] = None
    is_active: Optional[bool] = None
    pronouns: Optional[str] = None
    title: Optional[str] = None
    primary_organization: Optional[str] = None
    other_organizations: Optional[str] = None
    other_networks: Optional[str] = None
    about_me: Optional[str] = None
    skills_interests: Optional[str] = None
    profile_image: Optional[str] = None


@dataclass
class FilterVolunteerData:
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    gender: Optional[str] = None
    email: Optional[str] = None
    is_active: Optional[bool] = None


@dataclass
class ChangeVolunteerPasswordData:
    id: int
    email: str
    curr_password: str
    new_password: str


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
    volunteer_id: Optional[int] = None


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


@dataclass
class CreateTaskData:
    """
    Dataclass representing the data required to create a new task.
    """

    name: str
    description: str
    deadline: datetime
    status: str
    assigned_to: Optional[int]
    created_by: int
    organization_id: int


@dataclass
class UpdateTaskData:
    """
    Dataclass representing the fields that can be updated for a task.
    Optional fields allow partial updates.
    """

    id: int
    name: Optional[str] = None
    description: Optional[str] = None
    deadline: Optional[datetime] = None
    status: Optional[str] = None
    assigned_to: Optional[int] = None
    organization_id: Optional[int] = None


@dataclass
class CreatePostData:
    """
    Dataclass representing the fields that are needed to create a post
    """

    volunteer_id: int
    content: str
    created_at: datetime
    image: Optional[str] = None


@dataclass
class UpdatePostData:
    content: str
    image: Optional[str] = None


@dataclass
class CreateCommentData:
    """
    Dataclass representing the fields that are needed to create a comment
    """

    user_id: int
    post_id: int
    content: str
    created_at: datetime


@dataclass
class CreateEventData:

    title: str
    description: str
    start_time: datetime
    end_time: datetime
    location: str
    organization: int
