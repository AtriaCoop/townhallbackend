from .models import Volunteer
from .models import Opportunity
from .models import Organization

from .types import CreateVolunteerData
from .types import UpdateVolunteerData

from .types import CreateOpportunityData
from .types import UpdateOpportunityData
from .types import FilteredOpportunityData

from .types import CreateOrganizationData
from .types import UpdateOrganizationData
from .types import FilteredOrganizationData

import typing
from django.db.models.query import QuerySet
from django.contrib.auth.hashers import make_password

# Follows layered architecture pattern of views -> services -> dao


class VolunteerDao:

    def get_volunteers_all() -> typing.List[Volunteer]:
        return Volunteer.objects.all()

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
            email=create_volunteer_data.email,
            password=make_password(
                create_volunteer_data.password
            ),  # Hashing the password before saving
            is_active=True,
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
            volunteer.email = update_volunteer_data.email
            if (
                update_volunteer_data.password
            ):  # Check if password is provided for update
                volunteer.password = make_password(update_volunteer_data.password)
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

    def get_opportunity_all() -> typing.List[Opportunity]:
        return Opportunity.objects.all()

    def create_opportunity(create_opportunity_data: CreateOpportunityData) -> None:
        Opportunity.objects.create(
            title=create_opportunity_data.title,
            description=create_opportunity_data.description,
            start_time=create_opportunity_data.start_time,
            end_time=create_opportunity_data.end_time,
            location=create_opportunity_data.location,
        )

    def filtered_opportunity(
        filtered_opportunity_data: FilteredOpportunityData,
    ) -> QuerySet[Opportunity]:
        """Method to filter opportunities based on various fields.
        Args:
            The data object containing the criteria for filtering opportunities.
        Returns:
            A queryset of opportunities that match the filtering criteria.
        """
        filters = {}
        if filtered_opportunity_data.title:
            filters["title__icontains"] = filtered_opportunity_data.title
        if filtered_opportunity_data.starting_start_time:
            filters["start_time__gte"] = filtered_opportunity_data.starting_start_time
        if filtered_opportunity_data.starting_end_time:
            filters["start_time__lte"] = filtered_opportunity_data.starting_end_time
        if filtered_opportunity_data.ending_start_time:
            filters["end_time__gte"] = filtered_opportunity_data.ending_start_time
        if filtered_opportunity_data.ending_end_time:
            filters["end_time__lte"] = filtered_opportunity_data.ending_end_time
        if filtered_opportunity_data.location:
            filters["location__icontains"] = filtered_opportunity_data.location

        return Opportunity.objects.filter(**filters)

    def delete_opportunity(opportunity_id: int) -> None:
        try:
            Opportunity.objects.get(id=opportunity_id).delete()
        except Opportunity.DoesNotExist:
            pass

    def update_opportunity(
        id: int, update_opportunity_data: UpdateOpportunityData
    ) -> None:
        try:
            opportunity = Opportunity.objects.get(id=id)
            opportunity.title = update_opportunity_data.title
            opportunity.description = update_opportunity_data.description
            opportunity.start_time = update_opportunity_data.start_time
            opportunity.end_time = update_opportunity_data.end_time
            opportunity.location = update_opportunity_data.location
            opportunity.save()
        except Opportunity.DoesNotExist:
            pass

    def add_volunteer_to_opportunity(opportunity_id: int, volunteer_id: int) -> None:
        try:
            opportunity = Opportunity.objects.get(id=opportunity_id)
            volunteer = Volunteer.objects.get(id=volunteer_id)
            opportunity.volunteers.add(volunteer)
            opportunity.save()
        except (Opportunity.DoesNotExist, Volunteer.DoesNotExist):
            pass

    def remove_volunteer_from_opportunity(
        opportunity_id: int, volunteer_id: int
    ) -> None:
        try:
            opportunity = Opportunity.objects.get(id=opportunity_id)
            volunteer = Volunteer.objects.get(id=volunteer_id)
            opportunity.volunteers.remove(volunteer)
            opportunity.save()
        except (Opportunity.DoesNotExist, Volunteer.DoesNotExist):
            pass

    def remove_all_volunteers_from_opportunity(opportunity_id: int) -> None:
        try:
            opportunity = Opportunity.objects.get(id=opportunity_id)
            opportunity.volunteers.clear()
            opportunity.save()
        except (Opportunity.DoesNotExist, Volunteer.DoesNotExist):
            pass


class OrganizationDao:
    def create_organization(create_organization_data: CreateOrganizationData) -> None:
        Organization.objects.create(
            name=create_organization_data.name,
            location=create_organization_data.location,
            email=create_organization_data.email,
            phone_number=create_organization_data.phone_number,
            website=create_organization_data.website,
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
            organization.email = update_organization_data.email
            organization.phone_number = update_organization_data.phone_number
            organization.website = update_organization_data.website
            organization.save()
        except Organization.DoesNotExist:
            pass

    def filtered_organization(
        filtered_organization_data: FilteredOrganizationData,
    ) -> QuerySet[Organization]:
        filters = {}

        if filtered_organization_data.name:
            filters["name__icontains"] = filtered_organization_data.name
        if filtered_organization_data.location:
            filters["location__icontains"] = filtered_organization_data.location

        return Organization.objects.filter(**filters)
