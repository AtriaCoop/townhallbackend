from .models import Volunteer
from .types import CreateVolunteerData
# Follows layered architecture pattern of views -> services -> dao

class VolunteerDao:

    def get_volunteer(id: int) -> Volunteer:
        try:
            volunteer = Volunteer.objects.get(id=id)
            return volunteer
        except Volunteer.DoesNotExist:
            return None
    
    def create_volunteer(create_volunteer_data: CreateVolunteerData):
        Volunteer.objects.create(
            name=create_volunteer_data.name,
            gender=create_volunteer_data.gender,
            age=create_volunteer_data.age,
            email=create_volunteer_data.email,
        )

    def delete_volunteer(volunteer_id: int) -> Volunteer:
        try:
            volunteer = Volunteer.objects.get(id=volunteer_id)
            volunteer.delete()
            return volunteer
        except Volunteer.DoesNotExist:
            return None
