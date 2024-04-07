from django.shortcuts import render
import dataclasses

# Follows layered architecture pattern of views -> services -> dao
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response
from .services import VolunteerServices as volunteer_services


class VolunteerViewSet(viewsets.ModelViewSet):

    # THIS IS AN EXAMPLE, NOT COMPLETE
    @action(
        detail=True,
        methods=["GET"],
        url_path="get-volunteer"
    )
    def get_volunteer(self, request):
        return Response(dataclasses.asdict(volunteer_services.get_volunteer(id=request.data)), status=status.HTTP_200_OK)