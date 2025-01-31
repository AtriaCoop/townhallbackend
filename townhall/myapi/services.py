from django.contrib.auth import authenticate, get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password

# from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _
from django.core.cache import cache

# from django.conf import settings
from django.contrib.auth.password_validation import validate_password
from django.db.models.query import QuerySet
from django.core.validators import EmailValidator
import logging
import typing

from .dao import VolunteerDao as volunteer_dao
from .dao import OpportunityDao as opportunity_dao
from .dao import OrganizationDao as organization_dao
from .dao import TaskDao as task_dao
from .dao import ChatDao as chat_dao
from .dao import ProjectDao as project_dao

from .types import CreateVolunteerData
from .types import UpdateVolunteerData
from .types import FilterVolunteerData
from .types import ChangeVolunteerPasswordData

from .types import CreateTaskData
from .types import UpdateTaskData

from .types import CreateOpportunityData
from .types import UpdateOpportunityData
from .types import FilteredOpportunityData

from .types import CreateOrganizationData
from .types import UpdateOrganizationData
from .types import FilteredOrganizationData

from .models import Volunteer
from .models import Opportunity
from .models import Organization
from .models import Task
from .models import Project

User = get_user_model()

logger = logging.getLogger(__name__)


class VolunteerServices:
    def get_volunteer(id: int) -> typing.Optional[Volunteer]:
        try:
            volunteer = volunteer_dao.get_volunteer(id=id)
            return volunteer
        except Volunteer.DoesNotExist:
            raise ValidationError(f"Volunteer with the given id: {id}, does not exist.")

    def create_volunteer(create_volunteer_data: CreateVolunteerData) -> None:
        try:
            VolunteerServices.validate_volunteer(
                create_volunteer_data.email, create_volunteer_data.password
            )
            create_volunteer_data.password = make_password(
                create_volunteer_data.password
            )
            volunteer = volunteer_dao.create_volunteer(
                create_volunteer_data=create_volunteer_data
            )

            return volunteer
        except ValidationError:
            raise

    def update_volunteer(update_volunteer_data: UpdateVolunteerData) -> None:
        try:
            volunteer_dao.update_volunteer(update_volunteer_data=update_volunteer_data)
        except Volunteer.DoesNotExist:
            id = update_volunteer_data.id
            raise ValidationError(f"Volunteer with the given id: {id}, does not exist.")

    def delete_volunteer(id: int) -> None:
        try:
            volunteer_dao.delete_volunteer(volunteer_id=id)
        except Volunteer.DoesNotExist:
            raise ValidationError(f"Volunteer with the given id: {id}, does not exist.")

    def get_all_volunteers_optional_filter(
        filter_volunteer_data: typing.Optional[FilterVolunteerData] = None,
    ) -> QuerySet[Volunteer]:
        if filter_volunteer_data is not None:
            filters = {}

            if filter_volunteer_data.first_name:
                filters["first_name__icontains"] = filter_volunteer_data.first_name
            if filter_volunteer_data.last_name:
                filters["last_name__icontains"] = filter_volunteer_data.last_name
            if filter_volunteer_data.email:
                filters["email__iexact"] = filter_volunteer_data.email
            if filter_volunteer_data.is_active is not None:
                filters["is_active"] = filter_volunteer_data.is_active
            if filter_volunteer_data.gender:
                filters["gender__icontains"] = filter_volunteer_data.gender

            return volunteer_dao.filter_all_volunteers(filtersDict=filters)
        else:
            return volunteer_dao.get_volunteers_all()

    def get_all_filtered_opportunities_of_a_volunteer(
        filtered_opportunity_data: FilteredOpportunityData,
    ) -> QuerySet[Opportunity]:
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
        if filtered_opportunity_data.volunteer_id:
            filters["volunteers__id"] = filtered_opportunity_data.volunteer_id

        return volunteer_dao.get_all_filtered_opportunities_of_a_volunteer(
            filters_dict=filters
        )

    def add_volunteer_to_opportunity(volunteer_id: int, opportunity_id: int) -> None:
        try:
            volunteer_dao.add_volunteer_to_opportunity(volunteer_id, opportunity_id)
        except Volunteer.DoesNotExist:
            raise ValidationError(
                f"Volunteer with the given id: {volunteer_id}, does not exist."
            )
        except Opportunity.DoesNotExist:
            raise ValidationError(
                f"Opportunity with the given id: {opportunity_id}, does not exist."
            )

    def remove_volunteer_from_opportunity(
        volunteer_id: int, opportunity_id: int
    ) -> None:
        try:
            volunteer_dao.remove_volunteer_from_opportunity(
                volunteer_id, opportunity_id
            )
        except Volunteer.DoesNotExist:
            raise ValidationError(
                f"Volunteer with the given id: {volunteer_id}, does not exist."
            )
        except Opportunity.DoesNotExist:
            raise ValidationError(
                f"Opportunity with the given id: {opportunity_id}, does not exist."
            )

    def change_volunteers_password(
        change_vounteer_password_data: ChangeVolunteerPasswordData,
    ) -> None:
        try:
            # Authenticate the Volunteer with their email and original password
            volunteer = VolunteerServices.authenticate_volunteer(
                change_vounteer_password_data.email,
                change_vounteer_password_data.curr_password,
            )

            # Ensure that the Authentication passed
            if volunteer is None:
                raise ValidationError(
                    "Volunteer could not be authenticated, try again later"
                )

            # Validate the email and new password
            VolunteerServices.validate_volunteer(
                change_vounteer_password_data.email,
                change_vounteer_password_data.new_password,
            )

            # Ensure that the new password isn't an old password
            recent_passwords = cache.get(
                f"recent_passwords_{change_vounteer_password_data.id}", []
            )
            if change_vounteer_password_data.new_password in recent_passwords:
                id = change_vounteer_password_data.id
                logger.warning(f"Attempted password reuse for volunteer ID: {id}")
                raise ValidationError(_("You cannot reuse a recent password."))

            # Change the Password (Give the DAO method the hashed password)
            change_vounteer_password_data.new_password = make_password(
                change_vounteer_password_data.new_password
            )
            volunteer_dao.change_volunteers_password(change_vounteer_password_data)

            # Update recent passwords cache
            recent_passwords = (
                recent_passwords[-4:]
                if len(recent_passwords) >= 5
                else recent_passwords
            ) + [change_vounteer_password_data.new_password]
            cache.set(
                f"recent_passwords_{change_vounteer_password_data.id}",
                recent_passwords,
                timeout=None,
            )

            # Send notification email
            # Commented out as SMTP emailing is not yet setup and was causing errors
            """send_mail(
                subject=_("Password Change Notification"),
                message=_("Your password has been successfully changed."),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[volunteer.email],
            )"""
            logger.info(
                f"Password changed for volunteer ID: {change_vounteer_password_data.id}"
            )
        except Volunteer.DoesNotExist:
            id = change_vounteer_password_data.id
            raise ValidationError(f"Volunteer with the given id: {id}, does not exist.")
        except ValidationError:
            raise

    def authenticate_volunteer(email: str, password: str) -> typing.Optional[Volunteer]:
        # This method returns the volunteer on successful authentication
        # Rate limiting
        rate_limit_key = f"login_attempts_{email}"
        attempts = cache.get(rate_limit_key, 0)
        if attempts >= 5:  # Assuming a limit of 5 attempts
            logger.warning(f"Rate limit exceeded for email: {email}")
            raise ValidationError("Too many login attempts. Please try again later.")

        volunteer = authenticate(username=email, password=password)

        if volunteer is not None:
            if not volunteer.is_active:
                logger.warning(f"Inactive account: {email}")
                raise ValidationError("Account is inactive.")

            logger.info(f"Successful login for email: {email}")
            cache.delete(rate_limit_key)  # Reset on successful login
            return volunteer
        else:
            logger.warning(f"Failed login attempt for email: {email}")
            cache.set(rate_limit_key, attempts + 1, timeout=300)  # 5-minute timeout
            return None

    def validate_volunteer(email: str, password: str) -> None:
        # Validates the email
        validator = EmailValidator()
        try:
            validator(email)
        except ValidationError:
            logger.error(f"Invalid email format: {email}")
            raise ValidationError("Invalid email format.")

        # Validates the password
        try:
            validate_password(password)
        except ValidationError:
            logger.error(f"Password validation error for email: {email}")
            raise ValidationError("Invalid password.")

        # Prevent emails that are too similar to the password
        if email.lower() in password.lower() or password.lower() in email.lower():
            logger.error(f"Password is too similar to the email: {email}")
            raise ValidationError("Password is too similar to the email.")

        # Add any additional validation logic here


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
        opportunity_dao.create_opportunity(
            create_opportunity_data=create_opportunity_data
        )

    def filtered_opportunity(
        filtered_opportunity_data: FilteredOpportunityData,
    ) -> QuerySet[Opportunity]:
        return opportunity_dao.filtered_opportunity(
            filtered_opportunity_data=filtered_opportunity_data
        )

    def delete_opportunity(id: int) -> None:
        print(f"Deleting opportunity with ID: {id}")
        opportunity_dao.delete_opportunity(opportunity_id=id)

    def update_opportunity(
        id: int, update_opportunity_data: UpdateOpportunityData
    ) -> None:
        opportunity_dao.update_opportunity(
            id=id, update_opportunity_data=update_opportunity_data
        )

    def add_volunteer_to_opportunity(opportunity_id: int, volunteer_id: int) -> None:
        opportunity_dao.add_volunteer_to_opportunity(
            opportunity_id=opportunity_id, volunteer_id=volunteer_id
        )

    def get_all_volunteers_of_a_opportunity(opportunity_id: int) -> QuerySet[Volunteer]:
        return opportunity_dao.get_all_volunteers_of_a_opportunity(
            opportunity_id=opportunity_id
        )

    def get_all_opportunities_of_a_volunteer(
        volunteer_id: int,
    ) -> QuerySet[Opportunity]:
        return opportunity_dao.get_all_opportunities_of_a_volunteer(
            volunteer_id=volunteer_id
        )

    def remove_volunteer_from_opportunity(
        opportunity_id: int, volunteer_id: int
    ) -> None:
        opportunity_dao.remove_volunteer_from_opportunity(
            opportunity_id=opportunity_id, volunteer_id=volunteer_id
        )

    def remove_all_volunteers_from_opportunity(opportunity_id: int) -> None:
        opportunity_dao.remove_all_volunteers_from_opportunity(
            opportunity_id=opportunity_id
        )

    def remove_all_opportunities_from_volunteer(volunteer_id: int) -> None:
        opportunity_dao.remove_all_opportunities_from_volunteer(
            volunteer_id=volunteer_id
        )


class OrganizationServices:

    def get_organization(id: int) -> typing.Optional[Organization]:
        return organization_dao.get_organization(id=id)

    def get_organization_all(id: int) -> typing.List[Organization]:
        print("Fetching organization")
        organization = organization_dao.get_organization_all()
        print(f"Fetched organization{organization}")
        return organization

    def create_organization(create_organization_data: CreateOrganizationData) -> None:
        organization_dao.create_organization(
            create_organization_data=create_organization_data
        )

    def update_organization(update_organization_data: UpdateOrganizationData) -> None:
        organization_dao.update_organization(
            update_organization_data=update_organization_data
        )

    def delete_organization(id: int) -> None:
        organization_dao.delete_organization(organization_id=id)

    def filtered_organization(
        filtered_organization_data: FilteredOrganizationData,
    ) -> QuerySet[Organization]:
        return organization_dao.filtered_organization(
            filtered_organization_data=filtered_organization_data
        )


class TaskServices:

    @staticmethod
    def get_all_tasks() -> typing.List[Task]:
        return task_dao.get_all_tasks()

    @staticmethod
    def get_task_by_id(task_id: int) -> typing.Optional[Task]:
        return task_dao.get_task_by_id(task_id)

    @staticmethod
    def create_task(create_task_data: CreateTaskData) -> Task:
        # Fetch related instances (User, Organization)
        assigned_to = (
            Volunteer.objects.get(id=create_task_data.assigned_to)
            if create_task_data.assigned_to
            else None
        )
        created_by = Volunteer.objects.get(id=create_task_data.created_by)
        organization = Organization.objects.get(id=create_task_data.organization_id)

        # Create the task using dataclass attributes
        return Task.objects.create(
            name=create_task_data.name,
            description=create_task_data.description,
            deadline=create_task_data.deadline,
            status=create_task_data.status,
            assigned_to=assigned_to,
            created_by=created_by,
            organization=organization,
        )

    @staticmethod
    def update_task(
        task_id: int, update_task_data: UpdateTaskData
    ) -> typing.Optional[Task]:

        task = task_dao.get_task_by_id(task_id)

        if not task:
            return None

        # Fetch the User and Organization instances from IDs (if provided)
        if update_task_data.assigned_to:
            assigned_to = User.objects.get(id=update_task_data.assigned_to)
            task.assigned_to = assigned_to

        if update_task_data.organization_id:
            organization = Organization.objects.get(id=update_task_data.organization_id)
            task.organization = organization

        # Update task fields
        task.name = update_task_data.name or task.name
        task.description = update_task_data.description or task.description
        task.deadline = update_task_data.deadline or task.deadline
        task.status = update_task_data.status or task.status

        task.save()

        return task

    @staticmethod
    def delete_task(task_id: int) -> None:
        task_dao.delete_task(task_id)


class chatServices:
    @staticmethod
    def get_chat(user_id):
        try:
            # Check if the user exists
            User.objects.get(id=user_id)
            chat = chat_dao.get_chat(user_id)
            if not chat:
                return {"message": "No chats found for this user", "data": []}
            return {"message": "Success", "data": chat}
        except User.DoesNotExist:
            return {"error": f"User with ID {user_id} does not exist."}
        except Exception as e:
            return {"error": "An unexpected error occurred", "details": str(e)}

    @staticmethod
    def start_chat(participants_id):
        # Calling DAO method to create chat
        chat = chat_dao.start_chat(participants_id)
        return {"message": "Chat created successfully", "data": chat}

    @staticmethod
    def delete_chat(chat_id):
        if not isinstance(chat_id, int) or chat_id <= 0:
            return {"error": "Invalid chat ID provided."}

        try:
            chat_dao.delete_chat(chat_id)
            return {"message": "Chat deleted successfully."}
        except ValueError as ve:
            return {"error": str(ve)}
        except Exception as e:
            return {"error": "An unexpected error occurred.", "details": str(e)}


class ProjectServices:

    @staticmethod
    def get_project(id: int) -> typing.Optional[Project]:
        return project_dao.get_project(id=id)

    @staticmethod
    def get_all_projects() -> typing.List[Project]:
        return list(project_dao.get_project_all())
