from django import forms
from .models import Channel, Video, Comment


class ChannelForm(forms.ModelForm):
    class Meta:
        model = Channel
        fields = ["banner", "icon", "name", "handle", "description", "links", "contact"]
        widgets = {
            "banner": forms.FileInput(attrs={"accept": 'image/*'}),
            "icon": forms.FileInput(attrs={"accept": 'image/*'}),
        }
        help_texts = {
            "banner": "This image will appear across the top of your channel<br>For the best results on all devices, use an image that’s at least 2048 x 1152 pixels and 6MB or less.",
            "icon": "Your profile picture will appear where your channel is presented on YouTube, like next to your videos and comments<br>It’s recommended to use a picture that’s at least 98 x 98 pixels and 4MB or less. Use a PNG or GIF (no animations) file. Make sure your picture follows the YouTube Community Guidelines.",
            "name": "Choose a channel name that represents you and your content. Changes made to your name and picture are visible only on YouTube and not other Google services. You can change your name twice in 14 days.",
            "handle": "Choose your unique handle by adding letters and numbers. You can change your handle back within 14 days. Handles can be changed twice every 14 days.",
            "links": "Share external links with your viewers. They'll be visible on your channel profile and about page.",
            "contact": "Let people know how to contact you with business inquiries. The email address you enter may appear in the About section of your channel and be visible to viewers."
        }

class VideoForm(forms.ModelForm):
    file_browser = forms.FileField(label="Select video")

    class Meta:
        model = Video
        fields = ["file_browser", "thumbnail", "video_title", "vtype", "video_description"]

class VideoEditForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ["thumbnail", "video_title", "vtype", "video_description"]

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("comment",)

        widgets = {
            "comment": forms.TextInput(attrs={'placeholder': 'Add a comment...'})
        }

