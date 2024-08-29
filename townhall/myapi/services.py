from .dao import VolunteerDao as volunteer_dao
from .dao import OpportunityDao as opportunity_dao
from .dao import OrganizationDao as organization_dao

from .types import CreateVolunteerData
from .types import UpdateVolunteerData

from .types import CreateOpportunityData
from .types import UpdateOpportunityData
from .types import FilteredOpportunityData

from .types import CreateOrganizationData
from .types import UpdateOrganizationData
from .types import FilteredOrganizationData

from .models import Volunteer
from .models import Opportunity
from .models import Organization

import typing
from django.db.models.query import QuerySet

class VolunteerServices:
    
    def get_volunteers_all() -> typing.List[Volunteer]:
        return volunteer_dao.get_volunteers_all()

    def get_volunteer(id: int) -> typing.Optional[Volunteer]:
        return volunteer_dao.get_volunteer(id=id)
    
    def create_volunteer(create_volunteer_data: CreateVolunteerData) -> None:
        volunteer_dao.create_volunteer(create_volunteer_data=create_volunteer_data)
    
    def update_volunteer(update_volunteer_data: UpdateVolunteerData) -> None:
        volunteer_dao.update_volunteer(update_volunteer_data=update_volunteer_data)
    
    def delete_volunteer(id: int) -> None:
        volunteer_dao.delete_volunteer(volunteer_id=id)

class OpportunityServices:

    def get_opportunity(id: int) -> typing.Optional[Opportunity]:
        print(f"Fetching opportunity with ID: {id}")
        opportunity = opportunity_dao.get_opportunity(id=id)
        print(f"Fetched opportunity: {opportunity}")
        return opportunity
    
    def get_opportunity_all() -> typing.List[Opportunity]:
        print("Fetching opportunities")
        opportunities = opportunity_dao.get_opportunity_all()
        print(f"Fetched opportunities{opportunities}")
        return opportunities
    
    def create_opportunity(create_opportunity_data: CreateOpportunityData) -> None:
        opportunity_dao.create_opportunity(create_opportunity_data=create_opportunity_data)
    
    def filtered_opportunity(filtered_opportunity_data: FilteredOpportunityData) -> QuerySet[Opportunity]:
        return opportunity_dao.filtered_opportunity(filtered_opportunity_data=filtered_opportunity_data)
    
    def delete_opportunity(id: int) -> None:
        print(f"Deleting opportunity with ID: {id}")
        opportunity_dao.delete_opportunity(opportunity_id=id)

    def update_opportunity(id: int, update_opportunity_data: UpdateOpportunityData) -> None:
        opportunity_dao.update_opportunity(id=id, update_opportunity_data=update_opportunity_data)
    
    def add_volunteer_to_opportunity(opportunity_id: int, volunteer_id: int) -> None:
        opportunity_dao.add_volunteer_to_opportunity(opportunity_id=opportunity_id, volunteer_id=volunteer_id)

    def remove_volunteer_from_opportunity(opportunity_id: int, volunteer_id: int) -> None:
        opportunity_dao.remove_volunteer_from_opportunity(opportunity_id=opportunity_id, volunteer_id=volunteer_id)

    def remove_all_volunteers_from_opportunity(opportunity_id: int) -> None:
        opportunity_dao.remove_all_volunteers_from_opportunity(opportunity_id=opportunity_id)
        
class OrganizationServices:

    def get_organization(id: int) -> typing.Optional[Organization]:
        return organization_dao.get_organization(id=id)
    
    def get_organization_all(id: int) -> typing.List[Organization]:
        print("Fetching organization")
        organization = organization_dao.get_organization_all()
        print(f"Fetched organization{organization}")
        return organization
    
    def create_organization(create_organization_data: CreateOrganizationData) -> None:
        organization_dao.create_organization(create_organization_data=create_organization_data)
    
    def update_organization(update_organization_data: UpdateOrganizationData) -> None:
        organization_dao.update_organization(update_organization_data=update_organization_data)

    def delete_organization(id: int) -> None:
        organization_dao.delete_organization(organization_id=id)

    def filtered_organization(filtered_organization_data: FilteredOrganizationData) -> QuerySet[Organization]:
        return organization_dao.filtered_organization(filtered_organization_data=filtered_organization_data)