from rest_framework import serializers
from .models import Opportunity
from .models import Volunteer
from .models import Organization
from .models import Task


class OpportunitySerializer(serializers.ModelSerializer):

    class Meta:
        model = Opportunity
        fields = "__all__"


class VolunteerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Volunteer
        fields = [
            "first_name",
            "last_name",
            "email",
            "gender",
            "is_active",
        ]


class CreateVolunteerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Volunteer
        fields = [
            "first_name",
            "last_name",
            "email",
            "password",
            "gender",
        ]


class UpdateVolunteerSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    gender = serializers.ChoiceField(
        choices=[("M", "Male"), ("F", "Female")], required=False
    )
    is_active = serializers.BooleanField(required=False)

    # Make sure atleast 1 field has a Value
    def validate(self, data):
        if not any(data.values()):
            raise serializers.ValidationError("Atleast 1 field must have a Value")
        return data


class OrganizationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Organization
        fields = "__all__"


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = "__all__"


class ValidIDSerializer(serializers.Serializer):
    opportunity_id = serializers.IntegerField(required=True)
