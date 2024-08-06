from typing import List
from .models import Volunteer
from .models import Opportunity
from .models import Organization

from .types import CreateVolunteerData
from .types import UpdateVolunteerData
from .types import CreateOpportunityData
from .types import UpdateOpportunityData
from .types import CreateOrganizationData
from .types import UpdateOrganizationData
from .types import FilteredOpportunityData

import types
import typing
from django.db.models.query import QuerySet

# Follows layered architecture pattern of views -> services -> dao

class VolunteerDao:

    def get_volunteer(id: int) -> typing.Optional[Volunteer]:
        try:
            volunteer = Volunteer.objects.get(id=id)
            return volunteer
        except Volunteer.DoesNotExist:
            return None
    
    def create_volunteer(create_volunteer_data: CreateVolunteerData) -> None:
        Volunteer.objects.create(
            first_name=create_volunteer_data.first_name,
            last_name=create_volunteer_data.last_name,
            gender=create_volunteer_data.gender,
            age=create_volunteer_data.age,
            email=create_volunteer_data.email,
        )

    def delete_volunteer(volunteer_id: int) -> None:
        try:
            Volunteer.objects.get(id=volunteer_id).delete()
        except Volunteer.DoesNotExist:
            pass

    def update_volunteer(update_volunteer_data: UpdateVolunteerData) -> None:
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

    def get_opportunity(id: int) -> typing.Optional[Opportunity]:
        try:
            opportunity = Opportunity.objects.get(id=id)
            return opportunity
        except Opportunity.DoesNotExist:
            return None
        
    def get_opportunity_all() -> List[Opportunity]:
        return Opportunity.objects.all()

    def create_opportunity(create_opportunity_data: CreateOpportunityData) -> None:
        Opportunity.objects.create(
            name=create_opportunity_data.name,
            time=create_opportunity_data.time,
            description=create_opportunity_data.description,
            location=create_opportunity_data.location
        )

    def filtered_opportunity(filtered_opportunity_data: FilteredOpportunityData) -> QuerySet[Opportunity]:
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

    def delete_opportunity(opportunity_id: int) -> None:
        try:
            Opportunity.objects.get(id=opportunity_id).delete()
        except Opportunity.DoesNotExist:
            pass

    def update_opportunity(update_opportunity_data: UpdateOpportunityData) -> None:
        try:
            opportunity = Opportunity.objects.get(id=update_opportunity_data.id)
            opportunity.name = update_opportunity_data.name
            opportunity.time = update_opportunity_data.time
            opportunity.description = update_opportunity_data.description
            opportunity.location = update_opportunity_data.location
            opportunity.save()
        except Opportunity.DoesNotExist:
            pass

          
class OrganizationDao:
    def create_organization(create_organization_data: CreateOrganizationData) -> None:
        Organization.objects.create(
            name = create_organization_data.name,
            location = create_organization_data.location,
            description = create_organization_data.description,
            email = create_organization_data.email
        )
        
    def get_organization(id: int) -> typing.Optional[Organization]:
        try:
            organization = Organization.objects.get(id=id)
            return organization
        except Organization.DoesNotExist:
            return None

    def delete_organization(organization_id: int) -> None:
        try:
            Organization.objects.get(id=organization_id).delete()
        except Organization.DoesNotExist:
            pass

    def update_organization(update_organization_data: UpdateOrganizationData) -> None:
        try:
            organization = Organization.objects.get(id=update_organization_data.id)
            organization.name = update_organization_data.name
            organization.location = update_organization_data.location
            organization.description = update_organization_data.description
            organization.email = update_organization_data.email
            organization.save()
        except Organization.DoesNotExist:
            pass

    def filtered_organization(filtered_organization_data: FilteredOrganizationData) -> QuerySet[Organization]:
        filters = {}

        if filtered_organization_data.name:
            filters['name__icontains'] = filtered_organization_data.name
        if filtered_organization_data.location:
            filters['location__icontains'] = filtered_organization_data.location
        
        return Organization.objects.filter(**filters)
