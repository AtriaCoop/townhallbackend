from .models import Volunteer
from .models import Opportunity
from .types import CreateVolunteerData
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
            name=create_volunteer_data.name,
            gender=create_volunteer_data.gender,
            age=create_volunteer_data.age,
            email=create_volunteer_data.email,
        )

class OpportunityDao:

    def create_opportunity(create_opportunity_data: CreateOpportunityData):
        Opportunity.objects.create(
            name=create_opportunity_data.name,
            time=create_opportunity_data.time,
            description=create_opportunity_data.description,
            location=create_opportunity_data.location
        )