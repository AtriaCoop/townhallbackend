from django.utils import timezone
from django.forms import ValidationError
from django.contrib.auth import login
from .models import Task, Volunteer, Post, Comment

from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Follows layered architecture pattern of views -> services -> dao
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response

from .services import VolunteerServices as volunteer_services
from .services import OpportunityServices as opportunity_services
from .services import OrganizationServices as organization_services
from .services import TaskServices
from .services import CommentServices as comment_services
from .services import PostServices as post_services

from .serializers import OpportunitySerializer, FilteredOpportunitySerializer
from .serializers import (
    VolunteerSerializer,
    CreateVolunteerSerializer,
    OptionalVolunteerSerializer,
    VolunteerProfileSerializer,
    ChangePasswordVolunteerSerializer,
    CreateCommentSerializer,
    CommentSerializer,
    PostSerializer,
)
from .serializers import OrganizationSerializer
from .serializers import TaskSerializer

from .types import (
    CreateVolunteerData,
    UpdateVolunteerData,
    FilterVolunteerData,
    ChangeVolunteerPasswordData,
    CreateCommentData,
    CreatePostData,
    UpdatePostData,
)

from .types import FilteredOpportunityData

from .types import CreateTaskData
from .types import UpdateTaskData


class VolunteerViewSet(viewsets.ModelViewSet):

    # Volunteer Login
    @csrf_exempt  # Disable CSRF (only for development)
    @action(detail=False, methods=["post"])
    def login_volunteer(self, request):
        if request.method == "POST":
            try:
                data = json.loads(request.body)
                email = data.get("email")
                password = data.get("password")

                # Check if the volunteer exists
                try:
                    volunteer = Volunteer.objects.get(email=email)
                except Volunteer.DoesNotExist:
                    return JsonResponse({"error": "User not found"}, status=404)

                # Validate Password
                if check_password(password, volunteer.password):
                    login(
                        request,
                        volunteer,
                        backend='django.contrib.auth.backends.ModelBackend'
                    )

                    return JsonResponse({
                        "message": "Login successful",
                        "user": {
                            "id": volunteer.id,
                            "first_name": volunteer.first_name,
                            "last_name": volunteer.last_name,
                            "email": volunteer.email,
                            "gender": volunteer.gender,
                        }
                    }, status=200)
                else:
                    return JsonResponse({"error": "Invalid password"}, status=400)

            except json.JSONDecodeError:
                return JsonResponse({"error": "Invalid JSON"}, status=400)

        return JsonResponse({"error": "Invalid request method"}, status=405)

    # POST (Create) Volunteer
    @action(detail=False, methods=["post"], url_path="volunteer")
    def create_volunteer_request(self, request):
        # Transforms requests JSON data into a python dictionary
        serializer = CreateVolunteerSerializer(data=request.data)

        # If the data is NOT valid return with a message serializers errors
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # If data is valid, Take out the validated data
        validated_data = serializer.validated_data

        # Convert the validated data into the CreateVolunteerData type
        create_volunteer_data = CreateVolunteerData(
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
            email=validated_data["email"],
            password=validated_data["password"],
            gender=validated_data.get("gender", ""),
        )
        try:
            # Call the service method to create the volunteer
            volunteer = volunteer_services.create_volunteer(create_volunteer_data)

            # Create the response serializer
            response_serializer = VolunteerSerializer(volunteer)

            # Return the successful response
            return Response(
                {
                    "message": "Volunteer Created Successfully",
                    "volunteer": response_serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        except ValidationError as e:
            # If services method returns an error, return an error Response
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # POST for completing user's information
    @action(detail=True, methods=["post"], url_path="complete_profile")
    def complete_profile(self, request, pk=None):
        try:
            volunteer = Volunteer.objects.get(id=pk)
        except Volunteer.DoesNotExist:
            return Response(
                {"error": "Volunteer not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Only this line needed — no "files="!
        serializer = VolunteerProfileSerializer(
            volunteer, data=request.data, partial=True
        )

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()  # saves image too if passed

        # Automatically log the user in after profile is completed (authenticated)
        login(request, volunteer, backend='django.contrib.auth.backends.ModelBackend')

        return Response(
            {"message": "Profile setup completed."},
            status=status.HTTP_201_CREATED
        )

    # POST (Create) Add volunteer to Opportunity
    @action(detail=True, methods=["post"], url_path="opportunity")
    def add_volunteer_to_opportunity_request(self, request, vol_id, opp_id):
        # Get the volunteer id from the url
        volunteer_id = vol_id

        # Get the opportunity id from the url
        opportunity_id = opp_id

        try:
            # Call the service method to add volunteer to opportunity
            volunteer_services.add_volunteer_to_opportunity(
                volunteer_id, opportunity_id
            )

            # Return the successful response
            return Response(
                {"message": "Volunteer Added to Opportunity Successfully"},
                status=status.HTTP_201_CREATED,
            )
        except ValidationError as e:
            # If services method returns an error, return an error Response
            return Response({"message": str(e)}, status=status.HTTP_404_NOT_FOUND)

    # GET One Volunteer
    @action(detail=True, methods=["get"], url_path="volunteer")
    def get_volunteer_request(self, request, vol_id):
        # Get the volunteer id from the url
        volunteer_id = vol_id

        try:
            # Call the service method to get the volunteer
            volunteer = volunteer_services.get_volunteer(volunteer_id)

            # Create the response serializer
            response_serializer = VolunteerSerializer(volunteer)

            # Return the successful response
            return Response(
                {
                    "message": "Volunteer Retreived Successfully",
                    "volunteer": response_serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        except ValidationError as e:
            # If services method returns an error, return an error Response
            return Response({"message": str(e)}, status=status.HTTP_404_NOT_FOUND)

    # GET All Volunteers (Optional Volunteer Filter)
    @action(detail=False, methods=["get"], url_path="volunteer")
    def get_all_volunteers_optional_filter_request(self, request):
        # Transforms requests JSON data into a python dictionary
        serializer = OptionalVolunteerSerializer(data=request.query_params)

        # If the data is NOT valid (when atleast one value exists) then
        # process with the filter, otherwise get all
        volunteers = None
        message = None
        if serializer.is_valid():
            validated_data = serializer.validated_data

            # Convert the validated data into the FilterVolunteerData type
            filter_volunteer_data = FilterVolunteerData(
                first_name=validated_data.get("first_name", None),
                last_name=validated_data.get("last_name", None),
                email=validated_data.get("email", None),
                gender=validated_data.get("gender", None),
                is_active=validated_data.get("is_active", None),
            )

            volunteers = volunteer_services.get_all_volunteers_optional_filter(
                filter_volunteer_data
            )

            message = "All volunteers with the given filters retreived successfully"
        else:
            volunteers = volunteer_services.get_all_volunteers_optional_filter(None)
            message = "All Volunteers retreived successfully"

        # If no volunteers exist, return an empty list
        if not volunteers:
            return Response(
                {"message": "No Volunteers were found"},
                status=status.HTTP_200_OK,
            )

        # Create the response serializer for the list of volunteers
        response_serializer = VolunteerSerializer(volunteers, many=True)
        return Response(
            {
                "message": message,
                "data": response_serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    # GET All Opportunities of a Volunteer (Optional Opportunity Filter)
    @action(detail=True, methods=["get"], url_path="opportunity")
    def get_all_filtered_opportunities_of_a_volunteer_request(self, request, vol_id):
        # Get the volunteer id from the url
        volunteer_id = vol_id

        # Transforms requests JSON data into a python dictionary
        serializer = FilteredOpportunitySerializer(data=request.query_params)

        # If the data is NOT valid return with a message serializers errors
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # If data is valid, Take out the validated data
        validated_data = serializer.validated_data

        # Convert the validated data into the FilteredOpportunityData type
        filtered_opportunity_data = FilteredOpportunityData(
            title=validated_data.get("title", None),
            starting_start_time=validated_data.get("starting_start_time", None),
            starting_end_time=validated_data.get("starting_end_time", None),
            ending_start_time=validated_data.get("ending_start_time", None),
            ending_end_time=validated_data.get("ending_end_time", None),
            location=validated_data.get("location", None),
            organization_id=validated_data.get("organization", None),
            volunteer_id=volunteer_id,
        )

        # Call the service method to get the opportunities for the volunteer
        opportunities = (
            volunteer_services.get_all_filtered_opportunities_of_a_volunteer(
                filtered_opportunity_data
            )
        )

        # If no opportunities were found, send an appropriate message
        if not opportunities:
            return Response(
                {"message": "No Opportunities were found with the specified filters"},
                status=status.HTTP_200_OK,
            )

        # Create the response serializer for the list of volunteers
        response_serializer = OpportunitySerializer(opportunities, many=True)
        return Response(
            {
                "message": "Filtered Opportunities of this "
                + "Volunteer retreived successfully",
                "data": response_serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    # DELETE A Volunteer
    @action(detail=True, methods=["delete"], url_path="volunteer")
    def delete_volunteer_request(self, request, vol_id):
        # Get the volunteer id from the url
        volunteer_id = vol_id

        try:
            # Call the service method to delete the volunteer
            volunteer_services.delete_volunteer(volunteer_id)

            # Return the successful response
            return Response(
                {"message": "Volunteer Deleted Successfully"},
                status=status.HTTP_200_OK,
            )
        except ValidationError as e:
            # If services method returns an error, return an error Response
            return Response({"message": str(e)}, status=status.HTTP_404_NOT_FOUND)

    # DELETE (Remove) An Opportunity from a Volunteer
    @action(detail=True, methods=["delete"], url_path="opportunity")
    def remove_opportunity_from_a_volunteer_request(self, request, vol_id, opp_id):
        # Get the volunteer id from the url
        volunteer_id = vol_id

        # Get the opportunity id from the url
        opportunity_id = opp_id

        try:
            # Call the service method to remove the opportunity from the volunteer
            volunteer_services.remove_volunteer_from_opportunity(
                volunteer_id, opportunity_id
            )

            # Create and return the response
            return Response(
                {"message": "Opportunity removed from Volunteer successfully"},
                status=status.HTTP_200_OK,
            )
        except ValidationError as e:
            # If services method returns an error, return an error Response
            return Response({"message": str(e)}, status=status.HTTP_404_NOT_FOUND)

    # PATCH (Update) A Volunteer by ID
    @action(detail=True, methods=["patch"], url_path="volunteer")
    def update_volunteer_request(self, request, vol_id):
        # Get the volunteer id from the url
        volunteer_id = vol_id

        # Create a serializer to check if the data is valid
        serializer = OptionalVolunteerSerializer(data=request.data)

        # If the data is NOT valid return with message serializers errors
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Take out the validated data
        validated_data = serializer.validated_data

        # Convert the validated data into the UpdateVolunteerData type
        update_volunteer_data = UpdateVolunteerData(
            id=volunteer_id,
            first_name=validated_data.get("first_name"),
            last_name=validated_data.get("last_name"),
            email=validated_data.get("email"),
            gender=validated_data.get("gender"),
            is_active=validated_data.get("is_active"),
            pronouns=validated_data.get("pronouns"),
            title=validated_data.get("title"),
            primary_organization=validated_data.get("primary_organization"),
            other_organizations=validated_data.get("other_organizations"),
            other_networks=validated_data.get("other_networks"),
            about_me=validated_data.get("about_me"),
            skills_interests=validated_data.get("skills_interests"),
            profile_image=request.FILES.get("profile_image"),
        )
        try:
            # Call the service method to update the volunteer
            volunteer_services.update_volunteer(update_volunteer_data)

            # Return the successful response
            return Response(
                {
                    "message": "Volunteer Updated Successfully",
                },
                status=status.HTTP_200_OK,
            )
        except ValidationError as e:
            # If services method returns an error, return an error Response
            return Response({"message": str(e)}, status=status.HTTP_404_NOT_FOUND)

    # PATCH (Change) A Volunteers Password by ID
    @action(detail=True, methods=["patch"], url_path="change_password")
    def change_password_volunteer_request(self, request, vol_id):
        # Get the volunteer id from the url
        volunteer_id = vol_id

        # Create a serializer to check if the data is valid
        serializer = ChangePasswordVolunteerSerializer(data=request.data)

        # If the data is NOT valid return with message serializers errors
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Take out the validated data
        validated_data = serializer.validated_data

        # Convert the validated data into the UpdateVolunteerData type
        change_volunteer_password_data = ChangeVolunteerPasswordData(
            id=volunteer_id,
            email=validated_data["email"],
            curr_password=validated_data["curr_password"],
            new_password=validated_data["new_password"],
        )

        try:
            # Call the service method to update the volunteer
            volunteer_services.change_volunteers_password(
                change_volunteer_password_data
            )

            # Return the successful response
            return Response(
                {
                    "message": "Volunteers Password Changed Successfully",
                },
                status=status.HTTP_200_OK,
            )
        except ValidationError as e:
            # If services method returns an error, return an error Response
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class OpportunityViewSet(viewsets.ModelViewSet):

    # GET Opportunity
    @action(detail=False, methods=["get"], url_path="opportunity")
    def handle_opportunity_request(self, request):
        opportunity_id = self.request.query_params.get("id")
        if opportunity_id:
            # Fetching opportunity by ID
            opportunity_obj = opportunity_services.get_opportunity(id=opportunity_id)
            if not opportunity_obj:
                return Response(
                    {"error": "Opportunity not found"}, status=status.HTTP_404_NOT_FOUND
                )

            serializer = OpportunitySerializer(opportunity_obj)
            return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            # Fetching ALL opportunities
            opportunities = opportunity_services.get_opportunity_all()
            if not opportunities:
                return Response(
                    {"No opportunities found"}, status=status.HTTP_404_NOT_FOUND
                )

            serializer = OpportunitySerializer(opportunities, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    # DELETE Opportunity
    @action(detail=False, methods=["delete"], url_path="opportunity")
    def handle_opportunity_delete(self, request):
        opportunity_id = self.request.query_params.get("id")

        if not opportunity_id:
            raise ValidationError("The 'id' query parameter is required.")

        opportunity_obj = opportunity_services.get_opportunity(id=opportunity_id)
        if not opportunity_obj:
            return Response(
                {"error": "Opportunity not found"}, status=status.HTTP_404_NOT_FOUND
            )

        opportunity_services.delete_opportunity(id=opportunity_id)
        return Response(
            {"message": "Opportunity deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )

    # UPDATE Opportunity
    @action(detail=False, methods=["put"], url_path="opportunity")
    def handle_opportunity_update(self, request):
        opportunity_id = self.request.query_params.get("id")
        if not opportunity_id:
            return Response(
                {"error": "ID is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        opportunity_obj = opportunity_services.get_opportunity(id=int(opportunity_id))
        if not opportunity_obj:
            return Response(
                {"error": "Opportunity not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = OpportunitySerializer(
            opportunity_obj, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Opportunity updated successfully"},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrganizationViewSet(viewsets.ModelViewSet):

    # GET Organization
    @action(detail=False, methods=["get"], url_path="organization")
    def handle_organization_request(self, request):
        organization_id = self.request.query_params.get("id")
        if organization_id:
            # Fetching organization by ID
            organization_obj = organization_services.get_organization(
                id=organization_id
            )
            if not organization_obj:
                return Response(
                    {"error": "Organization not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            serializer = OrganizationSerializer(organization_obj)
            return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            # Fetching ALL organizations
            organization = organization_services.get_organization_all(id)
            if not organization:
                return Response(
                    {"No organizations found"}, status=status.HTTP_404_NOT_FOUND
                )

            serializer = OrganizationSerializer(organization, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    # DELETE Organization
    @action(detail=False, methods=["delete"], url_path="organization")
    def handle_organization_delete(self, request):
        organization_id = self.request.query_params.get("id")

        if not organization_id:
            raise ValidationError("The 'id' query parameter is required.")

        organization_obj = organization_services.get_organization(id=organization_id)
        if not organization_obj:
            return Response(
                {"error": "Organization not found"}, status=status.HTTP_404_NOT_FOUND
            )

        organization_services.delete_organization(id=organization_id)
        return Response(
            {"message": "Organization deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )

    # UPDATE Organization
    @action(detail=False, methods=["put"], url_path="organization")
    def handle_organization_update(self, request):
        organization_id = self.request.query_params.get("id")
        if not organization_id:
            return Response(
                {"error": "ID is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        organization_obj = organization_services.get_organization(
            id=int(organization_id)
        )
        if not organization_obj:
            return Response(
                {"error": "Organization not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = OrganizationSerializer(
            organization_obj, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Organization updated successfully"},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskViewSet(viewsets.ViewSet):

    @action(detail=False, methods=["get"])
    def get_all_tasks(self, request):

        tasks = TaskServices.get_all_tasks()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def get_task(self, request, pk=None):

        task = TaskServices.get_task_by_id(pk)
        if task:
            return Response(TaskSerializer(task).data)
        return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=["post"])
    def create_task(self, request, *args, **kwargs):
        task_data = CreateTaskData(
            name=request.data.get("name"),
            description=request.data.get("description", None),
            deadline=request.data.get("deadline", None),
            status=request.data.get("status", Task.TaskStatus.OPEN),
            assigned_to=request.data.get("assigned_to", None),
            created_by=request.data.get("created_by"),
            organization_id=request.data.get("organization", None),
        )

        task = TaskServices.create_task(task_data)
        return Response(TaskSerializer(task).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["put"])
    def update_task(self, request, pk=None, *args, **kwargs):
        task_data = UpdateTaskData(
            id=pk,
            name=request.data.get("name"),
            description=request.data.get("description", None),
            deadline=request.data.get("deadline", None),
            status=request.data.get("status", None),
            assigned_to=request.data.get("assigned_to", None),
            organization_id=request.data.get("organization", None),
        )

        task = TaskServices.update_task(pk, task_data)
        if task:
            return Response(TaskSerializer(task).data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=["delete"])
    def delete_task(self, request, pk=None):

        TaskServices.delete_task(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        return Comment.objects.all()

    # POST (Create) Comment
    @action(detail=False, methods=["post"], url_path="comment")
    def create_comment_endpoint(self, request):
        # Transforms requests JSON data into a python dictionary
        serializer = CreateCommentSerializer(data=request.data)

        # If the data is NOT valid return with a message serializers errors
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data

        create_comment_data = CreateCommentData(
            user_id=validated_data["user"].id,
            post_id=validated_data["post"].id,
            content=validated_data["content"],
            created_at=validated_data["created_at"],
        )

        try:
            comment = comment_services.create_comment(create_comment_data)

            response_serializer = CommentSerializer(comment)

            return Response(
                {
                    "message": "Comment Created Succesfully",
                    "comment": response_serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        except ValidationError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # DELETE (only by author)
    def destroy(self, request, *args, **kwargs):
        try:
            comment = self.get_object()
        except Comment.DoesNotExist:
            return Response(
                {"error": "Comment not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Get current user from session
        user_id = request.session.get("_auth_user_id")
        if not user_id:
            return Response(
                {"error": "Not authenticated"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Allow only the author to delete
        if comment.user.id != int(user_id):
            return Response(
                {"error": "Permission denied"},
                status=status.HTTP_403_FORBIDDEN
            )

        # Authorized – delete it
        comment.delete()
        return Response(
            {"message": "Comment deleted"},
            status=status.HTTP_204_NO_CONTEN
        )


class PostViewSet(viewsets.ModelViewSet):

    # GET a Post
    @action(detail=True, methods=["get"], url_path="post")
    def get_post_request(self, request, pk=None):
        try:
            post = post_services.get_post(id=pk)
            serializer = PostSerializer(post)
            return Response({
                "message": "Post fetched successfully",
                "post": serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "error": str(e)
            }, status=status.HTTP_404_NOT_FOUND)

    # GET all Posts
    @action(detail=False, methods=["get"], url_path="post")
    def get_all_posts(self, request):
        try:
            posts = post_services.get_all_posts()
            serializer = PostSerializer(posts, many=True)
            return Response({
                "message": "Posts fetched successfully",
                "posts": serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "error": str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # POST (Create)
    @action(detail=False, methods=["post"], url_path="post")
    def create_post_endpoint(self, request):
        serializer = PostSerializer(data=request.data)

        if not serializer.is_valid():
            print("Serializer errors:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data

        create_post_data = CreatePostData(
            volunteer_id=validated_data["volunteer"].id,
            content=validated_data["content"],
            created_at=timezone.now(),
            image=validated_data.get("image", None),
        )

        try:
            post = post_services.create_post(create_post_data)
            response_serializer = PostSerializer(post)
            return Response(
                {
                    "message": "Post Created Successfully",
                    "post": response_serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        except ValidationError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # PATCH (Update) Post
    @action(detail=True, methods=["patch"], url_path="post")
    def update_post(self, request, pk=None):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response(
                {"error": "Post not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = PostSerializer(post, data=request.data, partial=True)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        update_post_data = UpdatePostData(
            content=serializer.validated_data.get("content", ""),
            image=serializer.validated_data.get("image", None),
        )

        from .services import PostServices as post_services
        post_services.update_post(pk, update_post_data)

        return Response(
            {"message": "Post Updated Successfully"},
            status=status.HTTP_200_OK
        )

    # DELETE a Post
    @action(detail=True, methods=["delete"], url_path="post")
    def delete_post(self, request, pk=None):
        try:
            post_services.delete_post(post_id=pk)
            return Response(
                {"message": "Post deleted successfully"},
                status=status.HTTP_204_NO_CONTENT
            )
        except ValidationError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_404_NOT_FOUND
            )

    # Like a Post
    @action(detail=True, methods=["patch"], url_path="like")
    def like_post(self, request, pk=None):
        try:
            post = Post.objects.get(pk=pk)

            # Here: fetch user ID from session
            user_id = request.session.get("_auth_user_id")
            if not user_id:
                return Response(
                    {"error": "Not authenticated"},
                    status=status.HTTP_401_UNAUTHORIZED
                )

            try:
                volunteer = Volunteer.objects.get(id=user_id)
            except Volunteer.DoesNotExist:
                return Response(
                    {"error": "Volunteer not found"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if volunteer in post.liked_by.all():
                post.liked_by.remove(volunteer)
                post.likes -= 1
                post.save()
                return Response(
                    {
                        "message": "Post unliked",
                        "likes": post.likes
                    },
                    status=status.HTTP_200_OK
                )
            else:
                post.liked_by.add(volunteer)
                post.likes += 1
                post.save()
                return Response(
                    {
                        "message": "Post liked",
                        "likes": post.likes
                    },
                    status=status.HTTP_200_OK
                )

        except Post.DoesNotExist:
            return Response(
                {"error": "Post not found"},
                status=status.HTTP_404_NOT_FOUND
            )
