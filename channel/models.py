from django.db import models
from django.conf import settings
from django.urls import reverse

# Create your models here.

class Channel(models.Model):
    name = models.CharField(max_length=50, unique=True)
    handle = models.CharField(max_length=20, unique=True)
    icon = models.ImageField(upload_to="images/icon", default='images/icon/default-icon.jpg')
    banner = models.ImageField(upload_to="images/banner", default='images/banner/default-banner.jpg')
    description = models.TextField(max_length=1000, blank=True)
    links = models.CharField(max_length=200, blank=True)
    contact = models.CharField(max_length=20, blank=True)
    creationdate = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    subscribers = models.IntegerField(default=0)

    def subscriber_count(self):
        return self.subscription_set.count()

    def is_subscribed(self, user):
        return self.subscription_set.filter(user=user).exists()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('channel-detail', kwargs={'handle': self.handle,})


class Video(models.Model):

    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name="videos")
    thumbnail = models.ImageField(upload_to="images/")
    video = models.CharField(max_length=200)
    video_title = models.CharField(max_length=200)
    video_description = models.TextField(max_length=1000, blank=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    upload_date = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)

    media_types = {
        "VIDEO": "Video",
        "SHORTS": "Shorts",
        "LIVE": "Livestream"
    }
    vtype = models.CharField(max_length=20, choices=media_types.items())

    def __str__(self):
        return self.video_title
    
    def get_absolute_url(self):
        return reverse("video-detail", kwargs={"channel": self.channel.handle, "video_id": self.video_id})

class Comment(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    comment = models.CharField(max_length=500)
    post_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return self.comment

class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    channel = models.ForeignKey("Channel", on_delete=models.CASCADE)
    subscribe_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "channel")

    def __str__(self):
        return f"{self.user.username} → {self.channel.name}"

