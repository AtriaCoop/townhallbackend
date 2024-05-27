from .dao import VolunteerDao as volunteer_dao
from .types import CreateVolunteerData
from .models import Volunteer

class VolunteerServices:
    def get_volunteer(id: int) -> Volunteer:
        return volunteer_dao.get_volunteer(id=id)
    
    def create_volunteer(create_volunteer_data: CreateVolunteerData) -> None:
        return volunteer_dao.create_volunteer(create_volunteer_data=create_volunteer_data)
