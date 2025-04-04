from rest_framework import serializers
from .models import Opportunity
from .models import Volunteer
from .models import Organization
from .models import Task
from .models import Comment
from .models import Post


class OpportunitySerializer(serializers.ModelSerializer):

    class Meta:
        model = Opportunity
        fields = "__all__"


class FilteredOpportunitySerializer(serializers.Serializer):
    title = serializers.CharField(required=False)
    starting_start_time = serializers.DateTimeField(required=False)
    starting_end_time = serializers.DateTimeField(required=False)
    ending_start_time = serializers.DateTimeField(required=False)
    ending_end_time = serializers.DateTimeField(required=False)
    location = serializers.CharField(required=False)
    organization_id = serializers.IntegerField(required=False)


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


class OptionalVolunteerSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    gender = serializers.ChoiceField(
        choices=[("M", "Male"), ("F", "Female")], required=False
    )
    is_active = serializers.BooleanField(required=False, allow_null=True)

    # Make sure atleast 1 field has a Value
    def validate(self, data):
        if all(data.get(field) is None for field in data):
            raise serializers.ValidationError("Atleast 1 field must have a Value")
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


class CreateCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ["id", "user", "post", "content", "created_at"]


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ["id", "user", "post", "content", "created_at"]


class PostSerializer(serializers.ModelSerializer):
    volunteer = serializers.PrimaryKeyRelatedField(queryset=Volunteer.objects.all())

    class Meta:
        model = Post
        fields = ["id", "volunteer", "content", "created_at", "image"]
        read_only_fields = ["id", "created_at"]
