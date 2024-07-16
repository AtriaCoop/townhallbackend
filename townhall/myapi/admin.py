from django.contrib import admin

# Register your models here.
from .models import Volunteer

from .models import Opportunity


admin.site.register(Volunteer, Opportunity)