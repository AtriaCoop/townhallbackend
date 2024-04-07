from .dao import VolunteerDao as volunteer_dao
# Follows layered architecture pattern of views -> services -> dao

class VolunteerServices:
    def get_volunteer(id: int):
        return volunteer_dao.get_volunteer(id=id)