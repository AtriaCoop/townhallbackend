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


class VolunteerViewSet(viewsets.ModelViewSet):

    @action(detail=False, methods=['get'], url_path='get_volunteer')
    def get_volunteer(self, request):
        volunteer_id = self.request.query_params.get('id')

        volunteer_obj = volunteer_services.get_volunteer(id=volunteer_id)
        if not volunteer_obj:
            return Response({"error": "Volunteer not found"}, status=status.HTTP_404_NOT_FOUND) 
        
        serializer = VolunteerSerializer(volunteer_obj)
        return Response(serializer.data, status=status.HTTP_200_OK)

class OpportunityViewSet(viewsets.ModelViewSet):
    
    @action(detail=False, methods=['get'], url_path='get_opportunity')
    def get_opportunity(self, request):
        opportunity_id = self.request.query_params.get('id')

        opportunity_obj = opportunity_services.get_opportunity(id=opportunity_id)
        if not opportunity_obj:
            return Response({"error": "Opportunity not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = OpportunitySerializer(opportunity_obj)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'], url_path='get_opportunity_all')
    def get_opportunity_all(self,request):
        opportunities = opportunity_services.get_opportunity_all()
        if not opportunities:
            return Response({"error": "Opportunities not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = OpportunitySerializer(opportunities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['delete'], url_path='delete_opportunity')
    def delete_opportunity(self, request):
        opportunity_id = self.request.query_params.get('id')
        
        opportunity_services.delete_opportunity(id=opportunity_id)
        return Response({"message": "Opportunity deleted successfully"}, status=status.HTTP_204_NO_CONTENT)