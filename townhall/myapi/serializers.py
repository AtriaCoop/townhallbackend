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


class FilterVolunteerSerializer(serializers.Serializer):
    should_filter = serializers.BooleanField(required=True)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    gender = serializers.ChoiceField(
        choices=[("M", "Male"), ("F", "Female")], required=False
    )
    is_active = serializers.BooleanField(required=False, allow_null=True)

    def validate(self, data):
        if data.get("should_filter"):
            if all(
                data.get(field) is None
                for field in ["first_name", "last_name", "email", "gender", "is_active"]
            ):
                raise serializers.ValidationError(
                    {"should_filter": "This field is required."}
                )
        return data


class ChangePasswordVolunteerSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    curr_password = serializers.CharField(max_length=128, required=True)
    new_password = serializers.CharField(max_length=128, required=True)


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
