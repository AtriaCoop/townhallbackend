from .models import Volunteer
# Follows layered architecture pattern of views -> services -> dao

class VolunteerDao:

    def get_volunteer(id: int):
        return Volunteer.objects.get(id=id)