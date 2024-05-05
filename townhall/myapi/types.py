from dataclasses import dataclass

@dataclass
class CreateVolunteerData:
    name: str
    gender: str
    age: int
    email: str