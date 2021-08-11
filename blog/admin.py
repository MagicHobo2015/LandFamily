from django.contrib import admin
from .models import Post, Comment
from users.models import Profile


admin.site.register(Post)  # this adds posts into the admin site...
admin.site.register(Profile)    # this adds profile into the admin site
admin.site.register(Comment)    # this adds comment to the admin site
