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

from .serializers import OpportunitySerializer
from .serializers import ResponseVolunteerSerializer, CreateVolunteerSerializer
from .serializers import OrganizationSerializer
from .serializers import TaskSerializer
from .serializers import ValidIDSerializer

from .types import CreateVolunteerData

from .types import CreateTaskData
from .types import UpdateTaskData


class VolunteerViewSet(viewsets.ModelViewSet):

    # Define the get_queryset method to fetch all volunteers
    # Returns all volunteers for use with the ModelViewSet's built-in functionality.
    def get_queryset(self):

        return volunteer_services.get_volunteers_all()

    # Helper method to fetch volunteer by ID and handle case where volunteer not found
    def get_volunteer_object(self, pk):

        volunteer = volunteer_services.get_volunteer(id=pk)
        if not volunteer:
            return None, Response(
                {"error": "Volunteer not found"}, status=status.HTTP_404_NOT_FOUND
            )
        return volunteer, None

    # POST (Create) Volunteer
    @action(detail=False, methods=["post"], url_path="create_volunteer")
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
            response_serializer = ResponseVolunteerSerializer(volunteer)

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
    @action(detail=True, methods=["post"], url_path="add_volunteer_to_opportunity")
    def add_volunteer_to_opportunity_request(self, request, vol_id=None):
        # Get the volunteer id from the url
        volunteer_id = vol_id

        # Create a serializer to check if the data is valid
        serializer = ValidIDSerializer(data=request.data)

        # If the data is NOT valid return with message serializers errors
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Take out the validated data
        validated_data = serializer.validated_data
        opportunity_id = validated_data["opportunity_id"]

        try:
            # Call the service method to add volunteer to opportunity
            volunteer_services.add_volunteer_to_opportunity(
                volunteer_id, opportunity_id
            )

            # Return the successful response
            return Response(
                {
                    "message": "Volunteer Added to Opportunity Successfully",
                },
                status=status.HTTP_201_CREATED,
            )
        except ValidationError as e:
            # If services method returns an error, return an error Response
            return Response({"message": str(e)}, status=status.HTTP_404_NOT_FOUND)

    # GET all volunteers
    @action(detail=False, methods=["get"], url_path="volunteers")
    def get_all_volunteers(self, request):
        volunteers = volunteer_services.get_volunteers_all()

        # If no volunteers exist, return an empty list
        if not volunteers:
            return Response([], status=status.HTTP_200_OK)

        print("Volunteers data:", volunteers)

        # Serialize the list of volunteers
        serializer = ResponseVolunteerSerializer(volunteers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # GET Volunteer
    @action(detail=False, methods=["get"], url_path="volunteer")
    def handle_volunteer_request(self, request):
        volunteer_id = self.request.query_params.get("id")

        volunteer_obj, error_response = self.get_volunteer_object(volunteer_id)
        if error_response:
            return error_response

        serializer = ResponseVolunteerSerializer(volunteer_obj)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Update a Volunteer by ID
    @action(detail=True, methods=["put"], url_path="update")
    def update_volunteer(self, request, pk=None):

        # Use the helper method to fetch the volunteer
        volunteer_obj = volunteer_services.get_volunteer(id=pk)
        if not volunteer_obj:
            return Response(
                {"error": "Volunteer not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = ResponseVolunteerSerializer(
            volunteer_obj, data=request.data, partial=False
        )
        if serializer.is_valid():

            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE Volunteer
    @action(detail=False, methods=["delete"], url_path="volunteer")
    def handle_volunteer_delete(self, request):
        volunteer_id = self.request.query_params.get("id")

        if not volunteer_id:
            raise ValidationError("The 'id' query parameter is required.")

        volunteer_obj = volunteer_services.get_volunteer(id=volunteer_id)
        if not volunteer_obj:
            return Response(
                {"error": "Volunteer not found"}, status=status.HTTP_404_NOT_FOUND
            )

        volunteer_services.delete_volunteer(id=volunteer_id)
        return Response(
            {"message": "Volunteer deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


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
