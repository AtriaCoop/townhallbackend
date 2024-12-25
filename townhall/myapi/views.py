from django.forms import ValidationError
from .models import Task

# Follows layered architecture pattern of views -> services -> dao
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response

from .services import VolunteerServices as volunteer_services
from .services import OpportunityServices as opportunity_services
from .services import OrganizationServices as organization_services
from .services import TaskServices

from .serializers import OpportunitySerializer, FilteredOpportunitySerializer
from .serializers import (
    VolunteerSerializer,
    CreateVolunteerSerializer,
    UpdateVolunteerSerializer,
    FilterVolunteerSerializer,
    ChangePasswordVolunteerSerializer,
)
from .serializers import OrganizationSerializer
from .serializers import TaskSerializer

from .types import (
    CreateVolunteerData,
    UpdateVolunteerData,
    FilterVolunteerData,
    ChangeVolunteerPasswordData,
)

from .types import FilteredOpportunityData

from .types import CreateTaskData
from .types import UpdateTaskData


class VolunteerViewSet(viewsets.ModelViewSet):

    # POST (Create) Volunteer
    @action(detail=False, methods=["post"], url_path="volunteer")
    def create_volunteer_request(self, request):
        # Transforms requests JSON data into a python dictionary
        serializer = CreateVolunteerSerializer(data=request.data)

        # If the data is NOT valid return with a message serializers errors
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # If data is valid, Take out the validated data
        validated_data = serializer.validated_data

        # Convert the validated data into the CreateVolunteerData type
        create_volunteer_data = CreateVolunteerData(
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            email=validated_data["email"],
            password=validated_data["password"],
            gender=validated_data["gender"],
        )

        try:
            # Call the service method to create the volunteer
            volunteer = volunteer_services.create_volunteer(create_volunteer_data)

            # Create the response serializer
            response_serializer = VolunteerSerializer(volunteer)

            # Return the successful response
            return Response(
                {
                    "message": "Volunteer Created Successfully",
                    "volunteer": response_serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        except ValidationError as e:
            # If services method returns an error, return an error Response
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # POST (Create) Add volunteer to Opportunity
    @action(detail=True, methods=["post"], url_path="opportunity")
    def add_volunteer_to_opportunity_request(self, request, vol_id, opp_id):
        # Get the volunteer id from the url
        volunteer_id = vol_id

        # Get the opportunity id from the url
        opportunity_id = opp_id

        try:
            # Call the service method to add volunteer to opportunity
            volunteer_services.add_volunteer_to_opportunity(
                volunteer_id, opportunity_id
            )

            # Return the successful response
            return Response(
                {"message": "Volunteer Added to Opportunity Successfully"},
                status=status.HTTP_201_CREATED,
            )
        except ValidationError as e:
            # If services method returns an error, return an error Response
            return Response({"message": str(e)}, status=status.HTTP_404_NOT_FOUND)

    # GET One Volunteer
    @action(detail=True, methods=["get"], url_path="volunteer")
    def get_volunteer_request(self, request, vol_id):
        # Get the volunteer id from the url
        volunteer_id = vol_id

        try:
            # Call the service method to get the volunteer
            volunteer = volunteer_services.get_volunteer(volunteer_id)

            # Create the response serializer
            response_serializer = VolunteerSerializer(volunteer)

            # Return the successful response
            return Response(
                {
                    "message": "Volunteer Retreived Successfully",
                    "volunteer": response_serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        except ValidationError as e:
            # If services method returns an error, return an error Response
            return Response({"message": str(e)}, status=status.HTTP_404_NOT_FOUND)

    # GET All Volunteers (Optional Volunteer Filter)
    @action(detail=False, methods=["get"], url_path="volunteer")
    def get_all_volunteers_optional_filter_request(self, request):
        # Transforms requests JSON data into a python dictionary
        serializer = FilterVolunteerSerializer(data=request.query_params)

        # If the data is NOT valid return with a message serializers errors
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # If data is valid, Take out the validated data
        validated_data = serializer.validated_data

        # Get Should Filter value
        should_filter = validated_data["should_filter"]

        # If should filter, then create proceed with filter, otherwise do not
        volunteers = None
        if should_filter:
            # Convert the validated data into the FilterVolunteerData type
            filter_volunteer_data = FilterVolunteerData(
                first_name=validated_data.get("first_name", None),
                last_name=validated_data.get("last_name", None),
                email=validated_data.get("email", None),
                gender=validated_data.get("gender", None),
                is_active=validated_data.get("is_active", None),
            )

            volunteers = volunteer_services.get_all_volunteers_optional_filter(
                filter_volunteer_data
            )
        else:
            volunteers = volunteer_services.get_all_volunteers_optional_filter(None)

        # If no volunteers exist, return an empty list
        if not volunteers:
            return Response(
                {"message": "No Volunteers were found"},
                status=status.HTTP_200_OK,
            )

        # Create the response serializer for the list of volunteers
        response_serializer = VolunteerSerializer(volunteers, many=True)
        return Response(
            {
                "message": "All Volunteers retreived successfully",
                "data": response_serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    # GET All Opportunities of a Volunteer (Optional Opportunity Filter)
    @action(detail=True, methods=["get"], url_path="opportunity")
    def get_all_filtered_opportunities_of_a_volunteer_request(self, request, vol_id):
        # Get the volunteer id from the url
        volunteer_id = vol_id

        # Transforms requests JSON data into a python dictionary
        serializer = FilteredOpportunitySerializer(data=request.query_params)

        # If the data is NOT valid return with a message serializers errors
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # If data is valid, Take out the validated data
        validated_data = serializer.validated_data

        # Convert the validated data into the FilteredOpportunityData type
        filtered_opportunity_data = FilteredOpportunityData(
            title=validated_data.get("title", None),
            starting_start_time=validated_data.get("starting_start_time", None),
            starting_end_time=validated_data.get("starting_end_time", None),
            ending_start_time=validated_data.get("ending_start_time", None),
            ending_end_time=validated_data.get("ending_end_time", None),
            location=validated_data.get("location", None),
            organization_id=validated_data.get("organization", None),
            volunteer_id=volunteer_id,
        )

        # Call the service method to get the opportunities for the volunteer
        opportunities = (
            volunteer_services.get_all_filtered_opportunities_of_a_volunteer(
                filtered_opportunity_data
            )
        )

        # If no opportunities were found, send an appropriate message
        if not opportunities:
            return Response(
                {"message": "No Opportunities were found with the specified filters"},
                status=status.HTTP_200_OK,
            )

        # Create the response serializer for the list of volunteers
        response_serializer = OpportunitySerializer(opportunities, many=True)
        return Response(
            {
                "message": "Filtered Opportunities of this "
                + "Volunteer retreived successfully",
                "data": response_serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    # DELETE A Volunteer
    @action(detail=True, methods=["delete"], url_path="volunteer")
    def delete_volunteer_request(self, request, vol_id):
        # Get the volunteer id from the url
        volunteer_id = vol_id

        try:
            # Call the service method to delete the volunteer
            volunteer_services.delete_volunteer(volunteer_id)

            # Return the successful response
            return Response(
                {"message": "Volunteer Deleted Successfully"},
                status=status.HTTP_200_OK,
            )
        except ValidationError as e:
            # If services method returns an error, return an error Response
            return Response({"message": str(e)}, status=status.HTTP_404_NOT_FOUND)

    # DELETE (Remove) An Opportunity from a Volunteer
    @action(detail=True, methods=["delete"], url_path="opportunity")
    def remove_opportunity_from_a_volunteer_request(self, request, vol_id, opp_id):
        # Get the volunteer id from the url
        volunteer_id = vol_id

        # Get the opportunity id from the url
        opportunity_id = opp_id

        try:
            # Call the service method to remove the opportunity from the volunteer
            volunteer_services.remove_volunteer_from_opportunity(
                volunteer_id, opportunity_id
            )

            # Create and return the response
            return Response(
                {"message": "Opportunity removed from Volunteer successfully"},
                status=status.HTTP_200_OK,
            )
        except ValidationError as e:
            # If services method returns an error, return an error Response
            return Response({"message": str(e)}, status=status.HTTP_404_NOT_FOUND)

    # PATCH (Update) A Volunteer by ID
    @action(detail=True, methods=["patch"], url_path="volunteer")
    def update_volunteer_request(self, request, vol_id):
        # Get the volunteer id from the url
        volunteer_id = vol_id

        # Create a serializer to check if the data is valid
        serializer = UpdateVolunteerSerializer(data=request.data)

        # If the data is NOT valid return with message serializers errors
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Take out the validated data
        validated_data = serializer.validated_data

        # Convert the validated data into the UpdateVolunteerData type
        update_volunteer_data = UpdateVolunteerData(
            id=volunteer_id,
            first_name=validated_data.get("first_name", None),
            last_name=validated_data.get("last_name", None),
            email=validated_data.get("email", None),
            gender=validated_data.get("gender", None),
            is_active=validated_data.get("is_active", None),
        )

        try:
            # Call the service method to update the volunteer
            volunteer_services.update_volunteer(update_volunteer_data)

            # Return the successful response
            return Response(
                {
                    "message": "Volunteer Updated Successfully",
                },
                status=status.HTTP_200_OK,
            )
        except ValidationError as e:
            # If services method returns an error, return an error Response
            return Response({"message": str(e)}, status=status.HTTP_404_NOT_FOUND)

    # PATCH (Change) A Volunteers Password by ID
    @action(detail=True, methods=["patch"], url_path="change_password")
    def change_password_volunteer_request(self, request, vol_id):
        # Get the volunteer id from the url
        volunteer_id = vol_id

        # Create a serializer to check if the data is valid
        serializer = ChangePasswordVolunteerSerializer(data=request.data)

        # If the data is NOT valid return with message serializers errors
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Take out the validated data
        validated_data = serializer.validated_data

        # Convert the validated data into the UpdateVolunteerData type
        change_volunteer_password_data = ChangeVolunteerPasswordData(
            id=volunteer_id,
            email=validated_data["email"],
            curr_password=validated_data["curr_password"],
            new_password=validated_data["new_password"],
        )

        try:
            # Call the service method to update the volunteer
            volunteer_services.change_volunteers_password(
                change_volunteer_password_data
            )

            # Return the successful response
            return Response(
                {
                    "message": "Volunteers Password Changed Successfully",
                },
                status=status.HTTP_200_OK,
            )
        except ValidationError as e:
            # If services method returns an error, return an error Response
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class OpportunityViewSet(viewsets.ModelViewSet):

    # GET Opportunity
    @action(detail=False, methods=["get"], url_path="opportunity")
    def handle_opportunity_request(self, request):
        opportunity_id = self.request.query_params.get("id")
        if opportunity_id:
            # Fetching opportunity by ID
            opportunity_obj = opportunity_services.get_opportunity(id=opportunity_id)
            if not opportunity_obj:
                return Response(
                    {"error": "Opportunity not found"}, status=status.HTTP_404_NOT_FOUND
                )

            serializer = OpportunitySerializer(opportunity_obj)
            return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            # Fetching ALL opportunities
            opportunities = opportunity_services.get_opportunity_all()
            if not opportunities:
                return Response(
                    {"No opportunities found"}, status=status.HTTP_404_NOT_FOUND
                )

            serializer = OpportunitySerializer(opportunities, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    # DELETE Opportunity
    @action(detail=False, methods=["delete"], url_path="opportunity")
    def handle_opportunity_delete(self, request):
        opportunity_id = self.request.query_params.get("id")

        if not opportunity_id:
            raise ValidationError("The 'id' query parameter is required.")

        opportunity_obj = opportunity_services.get_opportunity(id=opportunity_id)
        if not opportunity_obj:
            return Response(
                {"error": "Opportunity not found"}, status=status.HTTP_404_NOT_FOUND
            )

        opportunity_services.delete_opportunity(id=opportunity_id)
        return Response(
            {"message": "Opportunity deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )

    # UPDATE Opportunity
    @action(detail=False, methods=["put"], url_path="opportunity")
    def handle_opportunity_update(self, request):
        opportunity_id = self.request.query_params.get("id")
        if not opportunity_id:
            return Response(
                {"error": "ID is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        opportunity_obj = opportunity_services.get_opportunity(id=int(opportunity_id))
        if not opportunity_obj:
            return Response(
                {"error": "Opportunity not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = OpportunitySerializer(
            opportunity_obj, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Opportunity updated successfully"},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrganizationViewSet(viewsets.ModelViewSet):

    # GET Organization
    @action(detail=False, methods=["get"], url_path="organization")
    def handle_organization_request(self, request):
        organization_id = self.request.query_params.get("id")
        if organization_id:
            # Fetching organization by ID
            organization_obj = organization_services.get_organization(
                id=organization_id
            )
            if not organization_obj:
                return Response(
                    {"error": "Organization not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            serializer = OrganizationSerializer(organization_obj)
            return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            # Fetching ALL organizations
            organization = organization_services.get_organization_all(id)
            if not organization:
                return Response(
                    {"No organizations found"}, status=status.HTTP_404_NOT_FOUND
                )

            serializer = OrganizationSerializer(organization, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    # DELETE Organization
    @action(detail=False, methods=["delete"], url_path="organization")
    def handle_organization_delete(self, request):
        organization_id = self.request.query_params.get("id")

        if not organization_id:
            raise ValidationError("The 'id' query parameter is required.")

        organization_obj = organization_services.get_organization(id=organization_id)
        if not organization_obj:
            return Response(
                {"error": "Organization not found"}, status=status.HTTP_404_NOT_FOUND
            )

        organization_services.delete_organization(id=organization_id)
        return Response(
            {"message": "Organization deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )

    # UPDATE Organization
    @action(detail=False, methods=["put"], url_path="organization")
    def handle_organization_update(self, request):
        organization_id = self.request.query_params.get("id")
        if not organization_id:
            return Response(
                {"error": "ID is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        organization_obj = organization_services.get_organization(
            id=int(organization_id)
        )
        if not organization_obj:
            return Response(
                {"error": "Organization not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = OrganizationSerializer(
            organization_obj, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Organization updated successfully"},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskViewSet(viewsets.ViewSet):

    @action(detail=False, methods=["get"])
    def get_all_tasks(self, request):

        tasks = TaskServices.get_all_tasks()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def get_task(self, request, pk=None):

        task = TaskServices.get_task_by_id(pk)
        if task:
            return Response(TaskSerializer(task).data)
        return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=["post"])
    def create_task(self, request, *args, **kwargs):
        task_data = CreateTaskData(
            name=request.data.get("name"),
            description=request.data.get("description", None),
            deadline=request.data.get("deadline", None),
            status=request.data.get("status", Task.TaskStatus.OPEN),
            assigned_to=request.data.get("assigned_to", None),
            created_by=request.data.get("created_by"),
            organization_id=request.data.get("organization", None),
        )

        task = TaskServices.create_task(task_data)
        return Response(TaskSerializer(task).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["put"])
    def update_task(self, request, pk=None, *args, **kwargs):
        task_data = UpdateTaskData(
            id=pk,
            name=request.data.get("name"),
            description=request.data.get("description", None),
            deadline=request.data.get("deadline", None),
            status=request.data.get("status", None),
            assigned_to=request.data.get("assigned_to", None),
            organization_id=request.data.get("organization", None),
        )

        task = TaskServices.update_task(pk, task_data)
        if task:
            return Response(TaskSerializer(task).data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=["delete"])
    def delete_task(self, request, pk=None):

        TaskServices.delete_task(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
