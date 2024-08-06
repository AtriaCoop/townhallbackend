from rest_framework import serializers
from .models import Opportunity
from .models import Volunteer

class OpportunitySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Opportunity
        fields = '__all__'

class VolunteerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Volunteer
        fields = '__all__'
