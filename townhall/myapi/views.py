from django.shortcuts import render
import dataclasses

# Follows layered architecture pattern of views -> services -> dao
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response

from myapi.types import UpdateOpportunityData
from .services import VolunteerServices as volunteer_services
from .services import OpportunityServices as opportunity_services
from .serializers import OpportunitySerializer, VolunteerSerializer


class VolunteerViewSet(viewsets.ModelViewSet):

    @action(detail=False, methods=['get'], url_path='volunteer')
    def handle_volunteer_request(self, request):
        volunteer_id = self.request.query_params.get('id')

        volunteer_obj = volunteer_services.get_volunteer(id=volunteer_id)
        if not volunteer_obj:
            return Response({"error": "Volunteer not found"}, status=status.HTTP_404_NOT_FOUND) 
        
        serializer = VolunteerSerializer(volunteer_obj)
        return Response(serializer.data, status=status.HTTP_200_OK)

class OpportunityViewSet(viewsets.ModelViewSet):
    
    # GET Opportunity
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
    
    # DELETE Opportunity
    @action(detail=False, methods=['delete'], url_path='opportunity')
    def handle_opportunity_delete(self, request):
        opportunity_id = self.request.query_params.get('id')
        
        opportunity_services.delete_opportunity(id=opportunity_id)
        return Response({"message": "Opportunity deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    
    # UPDATE Opportunity
    @action(detail=False, methods=['put'], url_path='opportunity')
    def handle_opportunity_update(self, request):
        opportunity_id = self.request.query_params.get('id')
        if not opportunity_id:
            return Response({"error": "ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = OpportunitySerializer(data=request.data)
        if serializer.is_valid():
            update_data = UpdateOpportunityData(
                id=int(opportunity_id),
                name=serializer.validated_data['name'],
                time=serializer.validated_data['time'],
                description=serializer.validated_data['description'],
                location=serializer.validated_data['location']
            )

            opportunity_services.update_opportunity(id=int(opportunity_id), update_opportunity_data=update_data)
            return Response({"message": "Opportunity updated successfully"}, status=status.HTTP_200_OK)