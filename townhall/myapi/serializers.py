from rest_framework import serializers
from .models import Opportunity
from .models import Volunteer
from .models import Organization


class OpportunitySerializer(serializers.ModelSerializer):

    class Meta:
        model = Opportunity
        fields = "__all__"


class VolunteerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Volunteer
        fields = '__all__'

class OrganizationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Organization
        fields = '__all__'
