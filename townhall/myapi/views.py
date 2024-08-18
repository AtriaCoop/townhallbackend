from django.shortcuts import render
import dataclasses

# Follows layered architecture pattern of views -> services -> dao
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response
from .services import VolunteerServices as volunteer_services
from .services import OpportunityServices as opportunity_services
from .serializers import OpportunitySerializer, VolunteerSerializer
from .types import UpdateVolunteerData


class VolunteerViewSet(viewsets.ModelViewSet):

    # Helper method to fetch a volunteer by ID and handle the case where the volunteer is not found
    def get_volunteer_object(self, pk):

        volunteer = volunteer_services.get_volunteer(id=pk)
        if not volunteer:
            return None, Response({"error": "Volunteer not found"}, status=status.HTTP_404_NOT_FOUND)
        return volunteer, None

    @action(detail=False, methods=['get'], url_path='volunteer')
    def handle_volunteer_request(self, request):
        volunteer_id = self.request.query_params.get('id')

        volunteer_obj, error_response = self.get_volunteer_object(volunteer_id)
        if error_response:
            return error_response

        serializer = VolunteerSerializer(volunteer_obj)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # Update a Volunteer by ID
    @action(detail=True, methods=['put'], url_path='update')
    def update_volunteer(self, request, pk=None):
        
        # Use the helper method to fetch the volunteer
        volunteer_obj = volunteer_services.get_volunteer(id=pk)
        if not volunteer_obj:
            return Response({"error": "Volunteer not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = VolunteerSerializer(volunteer_obj, data=request.data, partial=False)
        if serializer.is_valid():
            
            serializer.save()
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OpportunityViewSet(viewsets.ModelViewSet):
    
    @action(detail=False, methods=['get'], url_path='opportunity')
    def handle_opportunity_request(self, request):
            opportunity_id = self.request.query_params.get('id')
            if opportunity_id:
                # Fetching opportunity by ID
                opportunity_obj = opportunity_services.get_opportunity(id=opportunity_id)
                if not opportunity_obj:
                    return Response({"error": "Opportunity not found"}, status=status.HTTP_404_NOT_FOUND)
                
                serializer = OpportunitySerializer(opportunity_obj)
                return Response(serializer.data, status=status.HTTP_200_OK)
            
            else:
                # Fetching ALL opportunities
                opportunities = opportunity_services.get_opportunity_all()
                if not opportunities:
                    return Response({"No opportunities found"}, status=status.HTTP_404_NOT_FOUND)
                
                serializer = OpportunitySerializer(opportunities, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['delete'], url_path='opportunity')
    def handle_opportunity_delete(self, request):
        opportunity_id = self.request.query_params.get('id')
        
        opportunity_services.delete_opportunity(id=opportunity_id)
        return Response({"message": "Opportunity deleted successfully"}, status=status.HTTP_204_NO_CONTENT)