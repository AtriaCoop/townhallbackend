from .dao import VolunteerDao as volunteer_dao
from .models import Volunteer
# Follows layered architecture pattern of views -> services -> dao

class VolunteerServices:
    def get_volunteer(id: int) -> Volunteer:
        return volunteer_dao.get_volunteer(id=id)