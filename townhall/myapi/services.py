from .dao import VolunteerDao as volunteer_dao
from .types import CreateVolunteerData
# Follows layered architecture pattern of views -> services -> dao

class VolunteerServices:
    def get_volunteer(id: int):
        return volunteer_dao.get_volunteer(id=id)
    
    def create_volunteer(create_volunteer_data: CreateVolunteerData):
        return volunteer_dao.create_volunteer(create_volunteer_data=create_volunteer_data)