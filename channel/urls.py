from django.urls import path
from .views import (ChannelDetailView, ChannelUpdateView, ChannelUpdateListView, ChannelDeleteView,
                    ChannelCreateView, VideoCreateView, VideoDetailView, FunctionLibrary, VideoListView,
                    VideoUpdateView, VideoEditList, VideoDeleteView)

urlpatterns = [
    path("@<str:handle>/", ChannelDetailView.as_view(), name="channel-detail"),
    path("studio/@<str:handle>/", ChannelUpdateView.as_view(), name="channel-edit"),

    path("studio/@<str:handle>/delete/", ChannelDeleteView.as_view(), name="channel-delete"),
    path("studio/", ChannelUpdateListView.as_view(), name="update-list"),
    path("studio/new/", ChannelCreateView.as_view(), name="new-channel"),
    path("studio/@<str:handle>/upload/", VideoCreateView.as_view(), name="upload"),
    path("studio/@<str:handle>/contents/", VideoEditList.as_view(), name="video-edit-list"),
    path("studio/@<str:handle>/<int:video_id>/edit", VideoUpdateView.as_view(), name="video-update"),
    path("studio/@<str:handle>/<int:video_id>/delete/", VideoDeleteView.as_view(), name="video-delete"),
    path("videos/<int:video_id>/", FunctionLibrary.serve_video, name="serve-video"),
    path("@<str:handle>/videos/<int:video_id>/", VideoDetailView.as_view(), name="video-detail"),
    path("@<str:handle>/<str:vtype>/", VideoListView.as_view(), name="live-list"),
    path("@<str:handle>/video/<int:video_id>/like/", FunctionLibrary.like_video, name="like-video"),
    path("@<str:handle>/video/<int:video_id>/comment/<comment_id>/like/", FunctionLibrary.like_comment, name="like-comment"),
    path("@<str:handle>/subscribe/<int:video_id>/", FunctionLibrary.subscribe, name="subscribe"),
    path("@<str:handle>/unsubscribe/<int:video_id>/", FunctionLibrary.unsubscribe, name="unsubscribe"),
    path("@LofiGirl/stream", FunctionLibrary.lofi_radio, name="lofi-radio"),
]