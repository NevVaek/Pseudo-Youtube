
from django.contrib import admin
from .models import Channel, Video, Comment, Subscription

admin.site.register(Channel)
admin.site.register(Video)
admin.site.register(Comment)
admin.site.register(Subscription)
# Register your models here.

