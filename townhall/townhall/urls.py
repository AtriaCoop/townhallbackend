"""
URL configuration for townhall project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from debug_toolbar.toolbar import debug_toolbar_urls

from myapi.views import VolunteerViewSet
from myapi.views import OpportunityViewSet
from myapi.views import OrganizationViewSet
from myapi.views import TaskViewSet
from myapi.views import PostViewSet

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "auth/login/",
        VolunteerViewSet.as_view({"post": "login_volunteer"}),  # Fixed mapping
        name="login_volunteer",
    ),
    path(
        "volunteer/",
        VolunteerViewSet.as_view(
            {
                "get": "get_all_volunteers_optional_filter_request",
                "post": "create_volunteer_request",
            }
        ),
        name="volunteer",
    ),
    path(
        "volunteer/<int:vol_id>/",
        VolunteerViewSet.as_view(
            {
                "get": "get_volunteer_request",
                "delete": "delete_volunteer_request",
                "patch": "update_volunteer_request",
            }
        ),
        name="volunteer_id",
    ),
    path(
        "volunteer/<int:pk>/complete_profile/",
        VolunteerViewSet.as_view({"post": "complete_profile"}),
        name="complete_profile",
    ),
    path(
        "volunteer/<int:vol_id>/opportunity/",
        VolunteerViewSet.as_view(
            {
                "get": "get_all_filtered_opportunities_of_a_volunteer_request",
            }
        ),
        name="volunteer_id_opportunity",
    ),
    path(
        "volunteer/<int:vol_id>/opportunity/<int:opp_id>/",
        VolunteerViewSet.as_view(
            {
                "post": "add_volunteer_to_opportunity_request",
                "delete": "remove_opportunity_from_a_volunteer_request",
            }
        ),
        name="volunteer_id_opportunity_id",
    ),
    path(
        "volunteer/<int:vol_id>/change_password/",
        VolunteerViewSet.as_view(
            {
                "patch": "change_password_volunteer_request",
            }
        ),
        name="volunteer_change_password",
    ),
    path(
        "opportunity/",
        OpportunityViewSet.as_view(
            {
                "get": "handle_opportunity_request",
                "delete": "handle_opportunity_delete",
                "put": "handle_opportunity_update",
            }
        ),
    ),
    path(
        "organization/",
        OrganizationViewSet.as_view(
            {
                "get": "handle_organization_request",
                "delete": "handle_organization_delete",
                "put": "handle_organization_update",
            }
        ),
    ),
    path(
        "tasks/",
        TaskViewSet.as_view(
            {
                "get": "get_all_tasks",
                "post": "create_task",
            }
        ),
    ),
    path(
        "tasks/<int:pk>/",
        TaskViewSet.as_view(
            {
                "get": "get_task",
                "put": "update_task",
                "delete": "delete_task",
            }
        ),
    ),
    path(
        "post/",
        PostViewSet.as_view(
            {
                "get": "get_all_posts",
                "post": "create_post_endpoint",
            }
        ),
        name="post",
    ),
] + debug_toolbar_urls()

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
