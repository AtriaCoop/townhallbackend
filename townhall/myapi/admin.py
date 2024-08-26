from django.contrib import admin

# Register your models here.
from .models import Volunteer
from .models import Organization
from .models import Opportunity
from .models import Post


admin.site.register(Volunteer)
admin.site.register(Opportunity)
admin.site.register(Organization)
admin.site.register(Post)