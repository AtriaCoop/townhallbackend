from django.forms import ValidationError

# Follows layered architecture pattern of views -> services -> dao
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response

from .services import VolunteerServices as volunteer_services
from .services import OpportunityServices as opportunity_services
from .services import OrganizationServices as organization_services
from .services import TaskServices
from .serializers import OpportunitySerializer, VolunteerSerializer, OrganizationSerializer, TaskSerializer


class VolunteerViewSet(viewsets.ModelViewSet):
    
    # Define the get_queryset method to fetch all volunteers
    # This method returns all volunteers for use with the ModelViewSet's built-in functionality.
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
    
     # GET all volunteers
    @action(detail=False, methods=["get"], url_path="volunteers")
    def get_all_volunteers(self, request):
        volunteers = volunteer_services.get_volunteers_all()

        # If no volunteers exist, return an empty list
        if not volunteers:
            return Response([], status=status.HTTP_200_OK)
        
        print("Volunteers data:", volunteers)

        # Serialize the list of volunteers
        serializer = VolunteerSerializer(volunteers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # GET Volunteer
    @action(detail=False, methods=["get"], url_path="volunteer")
    def handle_volunteer_request(self, request):
        volunteer_id = self.request.query_params.get("id")

        volunteer_obj, error_response = self.get_volunteer_object(volunteer_id)
        if error_response:
            return error_response

        serializer = VolunteerSerializer(volunteer_obj)
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

        serializer = VolunteerSerializer(
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
            return Response({"error": "Opportunity not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = OpportunitySerializer(opportunity_obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Opportunity updated successfully"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrganizationViewSet(viewsets.ModelViewSet):

    # GET Organization
    @action(detail=False, methods=['get'], url_path='organization')
    def handle_organization_request(self, request):
            organization_id = self.request.query_params.get('id')
            if organization_id:
                # Fetching organization by ID
                organization_obj = organization_services.get_organization(id=organization_id)
                if not organization_obj:
                    return Response({"error": "Organization not found"}, status=status.HTTP_404_NOT_FOUND)
                
                serializer = OrganizationSerializer(organization_obj)
                return Response(serializer.data, status=status.HTTP_200_OK)
            
            else:
                # Fetching ALL organizations
                organization = organization_services.get_organization_all(id)
                if not organization:
                    return Response({"No organizations found"}, status=status.HTTP_404_NOT_FOUND)
                
                serializer = OrganizationSerializer(organization, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)

    # DELETE Organization
    @action(detail=False, methods=['delete'], url_path='organization')
    def handle_organization_delete(self, request):
        organization_id = self.request.query_params.get('id')

        if not organization_id:
            raise ValidationError("The 'id' query parameter is required.")

        organization_obj = organization_services.get_organization(id=organization_id)
        if not organization_obj:
            return Response({"error": "Organization not found"}, status=status.HTTP_404_NOT_FOUND)
        
        organization_services.delete_organization(id=organization_id)
        return Response({"message": "Organization deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    
    # UPDATE Organization
    @action(detail=False, methods=['put'], url_path='organization')
    def handle_organization_update(self, request):
        organization_id = self.request.query_params.get('id')
        if not organization_id:
            return Response({"error": "ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        organization_obj = organization_services.get_organization(id=int(organization_id))
        if not organization_obj:
            return Response({"error": "Organization not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = OrganizationSerializer(organization_obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Organization updated successfully"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class TaskViewSet(viewsets.ViewSet):

    @action(detail=False, methods=['get'])
    def get_all_tasks(self, request):

        tasks = TaskServices.get_all_tasks()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def get_task(self, request, pk=None):

        task = TaskServices.get_task_by_id(pk)
        if task:
            return Response(TaskSerializer(task).data)
        return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['post'])
    def create_task(self, request):

        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            task_data = serializer.validated_data
            task = TaskServices.create_task(task_data)
            return Response(TaskSerializer(task).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['put'])
    def update_task(self, request, pk=None):

        serializer = TaskSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            task_data = serializer.validated_data
            task = TaskServices.update_task(pk, task_data)
            if task:
                return Response(TaskSerializer(task).data)
            return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'])
    def delete_task(self, request, pk=None):
        
        TaskServices.delete_task(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)