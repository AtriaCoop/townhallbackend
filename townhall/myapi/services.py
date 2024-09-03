from django.contrib.auth import authenticate, get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import check_password, make_password
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _
from django.core.cache import cache
from django.conf import settings
from django.contrib.auth.password_validation import validate_password
from django.db.models.query import QuerySet
import logging
import typing

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

User = get_user_model()

logger = logging.getLogger(__name__)


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

    @staticmethod
    def authenticate_volunteer(
        username: str, password: str
    ) -> typing.Optional[Volunteer]:
        """
        Authenticate a volunteer using their username and password.

        :param username: The volunteer's username
        :param password: The volunteer's password
        :return: Volunteer object if authentication is successful, None otherwise
        """
        # Rate limiting
        rate_limit_key = f"login_attempts_{username}"
        attempts = cache.get(rate_limit_key, 0)
        if attempts >= 5:  # Assuming a limit of 5 attempts
            logger.warning(f"Rate limit exceeded for username: {username}")
            raise ValidationError(_("Too many login attempts. Please try again later."))

        volunteer = authenticate(username=username, password=password)

        if volunteer is not None:
            if not volunteer.is_active:
                logger.warning(f"Inactive account: {username}")
                raise ValidationError(_("Account is inactive."))

            logger.info(f"Successful login for username: {username}")
            cache.delete(rate_limit_key)  # Reset on successful login
            return volunteer
        else:
            logger.warning(f"Failed login attempt for username: {username}")
            cache.set(rate_limit_key, attempts + 1, timeout=300)  # 5-minute timeout
            return None

    @staticmethod
    def validate_username_and_password(username: str, password: str) -> None:
        """
        Validate the username and password before authentication.

        :param username: The volunteer's username
        :param password: The volunteer's password
        :raises ValidationError: If the username or password is invalid
        """
        if not username or len(username) < 3:
            logger.error(f"Invalid username: {username}")
            raise ValidationError(_("Username must be at least 3 characters long."))

        try:
            validate_password(password)
        except ValidationError as e:
            logger.error(f"Password validation error for username: {username}")
            raise e

        # Prevent usernames that are too similar to the password
        if username.lower() in password.lower():
            logger.error(f"Username is too similar to the password: {username}")
            raise ValidationError(_("Username is too similar to the password."))

        # Add any additional validation logic here

    @staticmethod
    def encrypt_password(password: str) -> str:
        """
        Securely encrypt the volunteer's password.

        :param password: The plain-text password
        :return: The hashed password
        :raises ValidationError: If the password is empty or invalid
        """
        if not password:
            logger.error("Attempted to encrypt an empty password.")
            raise ValidationError(_("Password cannot be empty."))

        try:
            VolunteerServices.validate_username_and_password("", password)
        except ValidationError as e:
            logger.error("Password validation failed before encryption.")
            raise e

        hashed_password = make_password(password)
        logger.info("Password successfully encrypted.")
        return hashed_password

    @staticmethod
    def change_password(
        volunteer_id: int, old_password: str, new_password: str
    ) -> None:
        """
        Handle changing a volunteer's password.

        :param volunteer_id: The volunteer's ID
        :param old_password: The volunteer's current password
        :param new_password: The volunteer's new password
        :raises AuthenticationError: If the old password is incorrect
        :raises ValidationError: If new password fails validation or is recent password
        """
        volunteer = volunteer_dao.get_volunteer(id=volunteer_id)
        if not volunteer:
            logger.error(f"Volunteer not found with ID: {volunteer_id}")
            raise ValidationError(_("Volunteer not found."))

        if not check_password(old_password, volunteer.password):
            logger.warning(f"Invalid old password for volunteer ID: {volunteer_id}")
            raise ValidationError(_("Old password is incorrect."))

        try:
            VolunteerServices.validate_username_and_password(
                volunteer.email, new_password
            )
        except ValidationError as e:
            logger.error("New password validation failed.")
            raise e

        # Password history check (e.g., last 5 passwords)
        recent_passwords = cache.get(f"recent_passwords_{volunteer_id}", [])
        if new_password in recent_passwords:
            logger.warning(f"Attempted password reuse for volunteer ID: {volunteer_id}")
            raise ValidationError(_("You cannot reuse a recent password."))

        encrypted_password = VolunteerServices.encrypt_password(new_password)
        volunteer.password = encrypted_password
        volunteer.save()

        # Update recent passwords cache
        recent_passwords = (
            recent_passwords[-4:] if len(recent_passwords) >= 5 else recent_passwords
        ) + [new_password]
        cache.set(f"recent_passwords_{volunteer_id}", recent_passwords, timeout=None)

        # Send notification email
        send_mail(
            subject=_("Password Change Notification"),
            message=_("Your password has been successfully changed."),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[volunteer.email],
        )
        logger.info(f"Password changed for volunteer ID: {volunteer_id}")


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


class OrganizationServices:

    def get_organization(id: int) -> typing.Optional[Organization]:
        return organization_dao.get_organization(id=id)

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
