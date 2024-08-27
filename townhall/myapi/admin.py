from django.contrib import admin

# Register your models here.
from .models import Volunteer
from .models import Organization
from .models import Opportunity
from .models import Post, Comment

# Displays the comments under the post in tabular form (neat table).
class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1  # Number of extra blank comment fields

# When viewing a post, you can see the associated comments
class PostAdmin(admin.ModelAdmin):
    inlines = [CommentInline]


admin.site.register(Volunteer)
admin.site.register(Opportunity)
admin.site.register(Organization)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)