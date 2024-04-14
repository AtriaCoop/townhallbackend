from django.shortcuts import render
import dataclasses

# Follows layered architecture pattern of views -> services -> dao
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response
from .services import VolunteerServices as volunteer_services


class VolunteerViewSet(viewsets.ModelViewSet):

    def get_volunteer(self, request):
        volunteer_id = self.request.query_params.get('id')

        volunteer_obj = volunteer_services.get_volunteer(id=volunteer_id)
        if not volunteer_obj:
            return Response({"error": "Volunteer not found"}, status=status.HTTP_404_NOT_FOUND) 
        return Response(dataclasses.asdict(volunteer_obj), status=status.HTTP_200_OK)