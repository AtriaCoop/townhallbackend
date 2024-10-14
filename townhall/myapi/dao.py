from .models import Volunteer
from .models import Opportunity
from .models import Organization
from .models import Task

from .types import CreateVolunteerData
from .types import UpdateVolunteerData
from .types import ChangeVolunteerPasswordData

from .types import CreateOpportunityData
from .types import UpdateOpportunityData
from .types import FilteredOpportunityData

from .types import CreateOrganizationData
from .types import UpdateOrganizationData
from .types import FilteredOrganizationData

from .types import CreateTaskData, UpdateTaskData

import typing
from typing import Optional, List
from django.db.models.query import QuerySet
from django.core.exceptions import ObjectDoesNotExist
from django.forms import ValidationError

# Follows layered architecture pattern of views -> services -> dao


class VolunteerDao:
    def get_volunteers_all() -> typing.List[Volunteer]:
        return Volunteer.objects.all()

    def get_volunteer(id: int) -> typing.Optional[Volunteer]:
        return Volunteer.objects.get(id=id)

    def create_volunteer(create_volunteer_data: CreateVolunteerData) -> None:
        Volunteer.objects.create(
            first_name=create_volunteer_data.first_name,
            last_name=create_volunteer_data.last_name,
            gender=create_volunteer_data.gender,
            email=create_volunteer_data.email,
            password=create_volunteer_data.password,
            is_active=True,
        )

    def delete_volunteer(volunteer_id: int) -> None:
        Volunteer.objects.get(id=volunteer_id).delete()

    def update_volunteer(update_volunteer_data: UpdateVolunteerData) -> None:
        volunteer = Volunteer.objects.get(id=update_volunteer_data.id)

        if update_volunteer_data.first_name:
            volunteer.first_name = update_volunteer_data.first_name
        if update_volunteer_data.last_name:
            volunteer.last_name = update_volunteer_data.last_name
        if update_volunteer_data.gender:
            volunteer.gender = update_volunteer_data.gender
        if update_volunteer_data.email:
            volunteer.email = update_volunteer_data.email
        if update_volunteer_data.is_active is not None:
            volunteer.is_active = update_volunteer_data.is_active

        volunteer.save()

    def get_all_opportunities_of_a_volunteer(
        volunteer_id: int,
    ) -> QuerySet[Opportunity]:
        volunteer = Volunteer.objects.get(id=volunteer_id)
        return volunteer.opportunities.all()

    def add_volunteer_to_opportunity(volunteer_id: int, opportunity_id: int) -> None:
        opportunity = Opportunity.objects.get(id=opportunity_id)
        volunteer = Volunteer.objects.get(id=volunteer_id)
        opportunity.volunteers.add(volunteer)
        opportunity.save()

    def remove_volunteer_from_opportunity(
        volunteer_id: int, opportunity_id: int
    ) -> None:
        opportunity = Opportunity.objects.get(id=opportunity_id)
        volunteer = Volunteer.objects.get(id=volunteer_id)
        opportunity.volunteers.remove(volunteer)
        opportunity.save()

    def change_volunteers_password(
        change_vounteer_password_data: ChangeVolunteerPasswordData,
    ) -> None:
        volunteer = Volunteer.objects.get(id=change_vounteer_password_data.id)

        volunteer.password = change_vounteer_password_data.new_password

        volunteer.save()


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
        try:
            valid_organization = Organization.objects.get(
                id=create_opportunity_data.organization_id
            )
        except Organization.DoesNotExist:
            raise ValidationError("This organization does not exist.")

        Opportunity.objects.create(
            title=create_opportunity_data.title,
            description=create_opportunity_data.description,
            start_time=create_opportunity_data.start_time,
            end_time=create_opportunity_data.end_time,
            location=create_opportunity_data.location,
            organization=valid_organization,
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
        if filtered_opportunity_data.organization_id:
            filters["organization_id"] = filtered_opportunity_data.organization_id

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
            valid_organization = Organization.objects.get(
                id=update_opportunity_data.organization_id
            )
            opportunity.title = update_opportunity_data.title
            opportunity.description = update_opportunity_data.description
            opportunity.start_time = update_opportunity_data.start_time
            opportunity.end_time = update_opportunity_data.end_time
            opportunity.location = update_opportunity_data.location
            opportunity.organization = valid_organization
            opportunity.save()
        except Opportunity.DoesNotExist:
            pass
        except Organization.DoesNotExist:
            raise ValidationError("This organization does not exist.")

    def add_volunteer_to_opportunity(opportunity_id: int, volunteer_id: int) -> None:
        try:
            opportunity = Opportunity.objects.get(id=opportunity_id)
            volunteer = Volunteer.objects.get(id=volunteer_id)
            opportunity.volunteers.add(volunteer)
            opportunity.save()
        except (Opportunity.DoesNotExist, Volunteer.DoesNotExist):
            pass

    def get_all_volunteers_of_a_opportunity(opportunity_id: int) -> QuerySet[Volunteer]:
        try:
            opportunity = Opportunity.objects.get(id=opportunity_id)
            return opportunity.volunteers.all()
        except Opportunity.DoesNotExist:
            pass

    def get_all_opportunities_of_a_volunteer(
        volunteer_id: int,
    ) -> QuerySet[Opportunity]:
        try:
            volunteer = Volunteer.objects.get(id=volunteer_id)
            return volunteer.opportunities.all()
        except Volunteer.DoesNotExist:
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
        except Opportunity.DoesNotExist:
            pass

    def remove_all_opportunities_from_volunteer(volunteer_id: int) -> None:
        try:
            volunteer = Volunteer.objects.get(id=volunteer_id)
            volunteer.opportunities.clear()
            volunteer.save()
        except Volunteer.DoesNotExist:
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

    def get_organization_all() -> typing.List[Organization]:
        return Organization.objects.all()

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


class TaskDao:
    """
    Data Access Object for handling Task-related database operations.
    """

    @staticmethod
    def get_all_tasks() -> List[Task]:

        return Task.objects.all()

    @staticmethod
    def get_task_by_id(task_id: int) -> Optional[Task]:

        try:
            return Task.objects.get(id=task_id)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def create_task(task_data: CreateTaskData) -> Task:

        return Task.objects.create(
            name=task_data.name,
            description=task_data.description,
            deadline=task_data.deadline,
            status=task_data.status,
            assigned_to_id=task_data.assigned_to,
            created_by_id=task_data.created_by,
            organization_id=task_data.organization_id,
        )

    @staticmethod
    def update_task(task_data: UpdateTaskData) -> Optional[Task]:

        try:
            task = Task.objects.get(id=task_data.id)
            # Update only the fields provided in UpdateTaskData (partial updates)
            if task_data.name is not None:
                task.name = task_data.name
            if task_data.description is not None:
                task.description = task_data.description
            if task_data.deadline is not None:
                task.deadline = task_data.deadline
            if task_data.status is not None:
                task.status = task_data.status
            if task_data.assigned_to is not None:
                task.assigned_to_id = task_data.assigned_to
            if task_data.organization_id is not None:
                task.organization_id = task_data.organization_id
            task.save()
            return task
        except Task.DoesNotExist:
            return None

    @staticmethod
    def delete_task(task_id: int) -> None:

        try:
            task = Task.objects.get(id=task_id)
            task.delete()
        except Task.DoesNotExist:
            pass
