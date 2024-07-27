from .models import Volunteer
from .models import Opportunity
from .models import Organization

from .types import CreateVolunteerData
from .types import UpdateVolunteerData
from .types import CreateOpportunityData
from .types import CreateOrganizationData
from .types import FilteredOpportunityData
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

    def delete_volunteer(volunteer_id: int):
        try:
            Volunteer.objects.get(id=volunteer_id).delete()
        except Volunteer.DoesNotExist:
            pass

    def update_volunteer(update_volunteer_data: UpdateVolunteerData):
        try:
            volunteer = Volunteer.objects.get(id=update_volunteer_data.id)
            volunteer.first_name = update_volunteer_data.first_name
            volunteer.last_name = update_volunteer_data.last_name
            volunteer.gender = update_volunteer_data.gender
            volunteer.age = update_volunteer_data.age
            volunteer.email = update_volunteer_data.email
            volunteer.save()
        except Volunteer.DoesNotExist:
            pass
         
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

    def filtered_opportunity(filtered_opportunity_data: FilteredOpportunityData):
        '''Method to filter opportunities based on various fields.
        Args:
            The data object containing the criteria for filtering opportunities.
        Returns:
            A queryset of opportunities that match the filtering criteria.
        '''
        filters = {}
        if filtered_opportunity_data.name:
            filters['name__icontains'] = filtered_opportunity_data.name
        if filtered_opportunity_data.start_time:
            filters['time__gte'] = filtered_opportunity_data.start_time
        if filtered_opportunity_data.end_time:
            filters['time__lte'] = filtered_opportunity_data.end_time
        if filtered_opportunity_data.location:
            filters['location__icontains'] = filtered_opportunity_data.location

        return Opportunity.objects.filter(**filters)

    def delete_opportunity(opportunity_id: int):
        try:
            Opportunity.objects.get(id=opportunity_id).delete()
        except Opportunity.DoesNotExist:
            pass