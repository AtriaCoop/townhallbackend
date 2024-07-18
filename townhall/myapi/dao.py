from .models import Volunteer
from .models import Opportunity
from .types import CreateVolunteerData
from .types import UpdateVolunteerData
from .types import CreateOpportunityData
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
            first_name=create_volunteer_data.first_name,
            last_name=create_volunteer_data.last_name,
            gender=create_volunteer_data.gender,
            age=create_volunteer_data.age,
            email=create_volunteer_data.email,
        )

    def update_volunteer(update_volunteer_data: UpdateVolunteerData):
        Volunteer.objects.update(
        first_name=update_volunteer_data.first_name,
        last_name=update_volunteer_data.last_name,
        gender=update_volunteer_data.gender,
        age=update_volunteer_data.age,
        email=update_volunteer_data.email,
    )

    def delete_volunteer(volunteer_id: int) -> Volunteer:
        try:
            Volunteer.objects.get(id=volunteer_id).delete()
        except Volunteer.DoesNotExist:
            return None
         
class OpportunityDao:

    def get_opportunity(id: int) -> Opportunity:
        try:
            opportunity = Opportunity.objects.get(id=id)
            return opportunity
        except Opportunity.DoesNotExist:
            return None

    def create_opportunity(create_opportunity_data: CreateOpportunityData):
        Opportunity.objects.create(
            name=create_opportunity_data.name,
            time=create_opportunity_data.time,
            description=create_opportunity_data.description,
            location=create_opportunity_data.location
        )
