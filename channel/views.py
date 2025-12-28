from pathlib import Path

from django.shortcuts import render

# Create your views here.

from django.views import View
from django.views.generic import DetailView, UpdateView, ListView, DeleteView, CreateView, FormView
from django.views.generic.detail import SingleObjectMixin

from .models import Channel, Video, Comment, Subscription
from django.urls import reverse_lazy, reverse
from .forms import ChannelForm, VideoForm, CommentForm, VideoEditForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.shortcuts import get_object_or_404, redirect
import os, datetime, subprocess, random
from django.http import Http404, StreamingHttpResponse, FileResponse
from .radio import HLSRadio



class ChannelDetailView(DetailView): # new
    model = Channel
    template_name = "base_channel_details.html"
    context_object_name = "channel"
    slug_field = "handle"  # 👈 tells Django which field to look up
    slug_url_kwarg = "handle"     # "slug" for string values, "pk" for primary keys

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add your extra variable here
        context["extra_css"] = "css/channel-details.css"

        if self.request.user.is_authenticated:
            channel = get_object_or_404(Channel, handle=self.kwargs["handle"])
            context["subscribed"] = channel.is_subscribed(user=self.request.user)

        return context

class ChannelUpdateView(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    model = Channel
    slug_field = "handle"  # 👈 tells Django which field to look up
    slug_url_kwarg = "handle"  # "slug" for string values, "pk" for primary keys
    template_name = "channel_edit.html"
    form_class = ChannelForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add your extra variable here
        context["extra_css2"] = "css/channel-edit.css"
        return context

    def test_func(self):  # new
        obj = self.get_object()
        print(obj.author)
        return obj.author == self.request.user

class ChannelUpdateListView(LoginRequiredMixin, ListView):
    model = Channel
    template_name = "channel_edit_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["extra_css"] = "css/channel_edit_list.css"
        return context

class ChannelDeleteView(LoginRequiredMixin,UserPassesTestMixin, DeleteView):
    model = Channel
    template_name = "channel_delete.html"
    success_url = reverse_lazy("update-list")

    slug_field = "handle"  # 👈 tells Django which field to look up
    slug_url_kwarg = "handle"  # "slug" for string values, "pk" for primary keys

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add your extra variable here
        context["extra_css3"] = "css/channel-delete.css"
        return context

    def test_func(self):  # new
        obj = self.get_object()
        return obj.author == self.request.user

class ChannelCreateView(LoginRequiredMixin, CreateView):
    model = Channel
    template_name = "channel_new.html"
    form_class = ChannelForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add your extra variable here
        context["extra_css4"] = "css/channel-new.css"
        return context

    def form_valid(self, form):  # new
        form.instance.author = self.request.user
        self.request.user.channels_created += 1
        return super().form_valid(form)

class VideoCreateView(LoginRequiredMixin, CreateView):
    model = Video
    template_name = "channel_video_up.html"
    form_class = VideoForm

    slug_field = "handle"  # 👈 tells Django which field to look up
    slug_url_kwarg = "handle"  # "slug" for string values, "pk" for primary keys

    FULL_VIDEO_DIR = "G:/videoo/YoutubeArchive"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["extra_css5"] = "css/video-upload.css"

        return context



    def form_valid(self, form):  # new
        channel = get_object_or_404(Channel, handle=self.kwargs["handle"])
        form.instance.channel = channel
        form.instance.creator = self.request.user
        file_name = self.request.POST.get("video")
        form.instance.video = os.path.join(self.FULL_VIDEO_DIR, channel.handle, file_name)
        return super().form_valid(form)

    def get_success_url(self):
        video = self.object
        return reverse("update-list")

class VideoEditList(LoginRequiredMixin, ListView):
    model = Channel
    template_name = "channel_video_edit_list.html"

    slug_field = "handle"
    slug_url_kwarg = "handle"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["extra_css6"] = "css/video-upload.css"

        channel = get_object_or_404(Channel, handle=self.kwargs["handle"])
        context["videos"] = Video.objects.filter(channel=channel, vtype="VIDEO")
        context["shorts"] = Video.objects.filter(channel=channel, vtype="SHORT")
        context["live"] = Video.objects.filter(channel=channel, vtype="LIVE")

        return context

class VideoUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Video

    template_name = "channel_video_edit.html"
    form_class = VideoEditForm

    def test_func(self):
        obj = self.get_object()
        return obj.creator == self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["extra_css5"] = "css/video-upload.css"
        return context

    def get_object(self, queryset=None):
        # Fetch the Channel instance using the handle
        channel = Channel.objects.get(handle=self.kwargs['handle'])
        # Now get the Video object from that Channel, using the video_id
        video = Video.objects.get(id=self.kwargs['video_id'], channel=channel)
        return video

    def get_success_url(self):
        video = self.object
        return reverse("video-edit-list", kwargs={"handle": video.channel.handle})

class VideoDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Video
    template_name = "video_delete.html"

    def test_func(self):
        obj = self.get_object()
        return obj.creator == self.request.user

    def get_object(self, queryset=None):
        # Fetch the Channel instance using the handle
        channel = Channel.objects.get(handle=self.kwargs['handle'])
        # Now get the Video object from that Channel, using the video_id
        video = Video.objects.get(id=self.kwargs['video_id'], channel=channel)
        return video

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add your extra variable here
        context["extra_css3"] = "css/channel-delete.css"
        return context

    def get_success_url(self):
        video = self.object
        return reverse("video-edit-list", kwargs={"handle": video.channel.handle})


class FunctionLibrary:

    def serve_video(request, video_id):
        video = get_object_or_404(Video, pk=video_id)
        video_path = video.video

        if not os.path.exists(video_path):
            raise Http404("video not found.")

        file_size = os.path.getsize(video_path)
        range_header = request.headers.get("Range", "").strip()
        start, end = 0, file_size - 1

        if range_header:
            range_match = range_header.replace("bytes=", "").split("-")
            start = int(range_match[0])
            if range_match[1]:
                end = int(range_match[1])

        length = end - start + 1

        def file_iterator(path, offset=start, length=length, chunk_size=8192):
            with open(path, "rb") as f:
                f.seek(offset)
                remaining = length
                while remaining > 0:
                    chunk = f.read(min(chunk_size, remaining))
                    if not chunk:
                        break
                    yield chunk
                    remaining -= len(chunk)

        response = StreamingHttpResponse(file_iterator(video_path), status=206 if range_header else 200,
                                         content_type='video/mp4')
        response['Content-Length'] = str(length)
        response['Accept-Ranges'] = "bytes"
        if range_header:
            response['Content-Range'] = f'bytes {start}-{end}/{file_size}'
        return response

    def get_time(datetimeobj):
        current = datetime.datetime.now()

        num = current.year - datetimeobj.year
        if num > 0:
            return (num, "year(s)")

        num = current.month - datetimeobj.month
        if num != 0:
            if num < 0:
                num = 12 + num
            return (num, "month(s)")

        num = current.day - datetimeobj.day
        if num != 0:
            if num < 0:
                num = 30 + num
            return (num, "day(s)")

        num = current.hour - datetimeobj.hour
        if num != 0:
            if num < 0:
                num = 24 + num
            return (num, "hour(s)")

        num = current.minute - datetimeobj.minute
        if num != 0:
            if num < 0:
                num = 60 + num
            return (num, "minute(s)")

        num = current.second - datetimeobj.second
        if num != 0:
            if num < 0:
                num = 60 + num
            return (num, "second(s)")
        return None

    def like_video(request, handle, video_id):
        if not request.user.is_authenticated:
            return redirect('login')
        video = get_object_or_404(Video, pk=video_id)
        video.likes += 1
        video.save()
        return redirect('video-detail', handle=handle, video_id=video_id)

    def like_comment(request, handle, video_id, comment_id):
        if not request.user.is_authenticated:
            return redirect('login')
        comment = get_object_or_404(Comment, pk=comment_id)
        comment.likes += 1
        comment.save()
        return redirect('video-detail', handle=handle, video_id=video_id)

    def subscribe(request, handle, video_id):
        if not request.user.is_authenticated:
            return redirect('login')
        channel = get_object_or_404(Channel, handle=handle)
        Subscription.objects.get_or_create(user=request.user, channel=channel)
        channel.subscribers += 1
        channel.save()
        referer_url = request.META.get('HTTP_REFERER', None)
        if video_id != 0:
            video = get_object_or_404(Video, pk=video_id)
            return redirect(referer_url, handle=channel.handle, video_id=video.pk)
        else:
            return redirect(referer_url, handle=handle)

    def unsubscribe(request, handle, video_id):
        channel = get_object_or_404(Channel, handle=handle)
        Subscription.objects.filter(user=request.user, channel=channel).delete()
        channel.subscribers -= 1
        channel.save()
        referer_url = request.META.get('HTTP_REFERER', None)
        if video_id != 0:
            video = get_object_or_404(Video, pk=video_id)
            return redirect(referer_url, handle=channel.handle, video_id=video.pk)
        else:
            return redirect(referer_url, handle=handle)

    def lofi_radio(request):
        MEDIA_ROOT = r"C:/Users/NevVaek/Documents/Django/code/youtube/media/audio"
        loop_path = os.path.join(MEDIA_ROOT, "LofiSingle/radio/Timeline-1.mp4")
        audio_dir = os.path.join(MEDIA_ROOT, "LofiSingle")
        playlist_path = os.path.join(audio_dir, "playlist/playlist.txt")

        tracks = [f for f in os.listdir(audio_dir) if f.endswith(".m4a")]

        if not tracks:
            raise RuntimeError("No .mp3 files found in /audio folder!")

        random.shuffle(tracks)

        with open(playlist_path, "w", encoding="utf-8") as f:
            for t in tracks:
                f.write(f"file '{os.path.join(audio_dir, t).replace("'", "'\\''")}'\n")

        # Pick a random audio track

        # ffmpeg command:
        # -stream_loop -1 → loop the video forever
        # -i loop.mp4 → video input
        # -i track.mp3 → audio input
        # -shortest → stop when audio ends
        # -f mp4 → output format
        # -movflags frag_keyframe+empty_moov → streamable MP4

        cmd = [
            "ffmpeg",
            "-stream_loop", "-1",
            "-i", loop_path,
            "-f", "concat", "-safe", "0", "-i", playlist_path,
            "-map", "0:v:0",  # take video from first input
            "-map", "1:a:0",  # take audio from second input
            "-c:v", "h264_nvenc",   #Replacement for "libx264" which uses CPU. The current one uses GPU
            "-c:a", "copy",
            "-shortest",
            "-f", "mp4",
            "-movflags", "frag_keyframe+empty_moov",
            "pipe:1",
        ]

        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        def stream():
            try:
                for chunk in iter(lambda: process.stdout.read(4096), b""):
                    yield chunk
            finally:
                process.kill()

        return StreamingHttpResponse(
            stream(), content_type="video/mp4"
        )

class VideoListView(ListView):
    model = Channel
    slug_field = "handle"
    slug_url_kwarg = "handle"
    template_name = "channel_video_list_live.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["extra_css"] = "css/channel-details.css"
        context["extra_css2"] = "css/channel-video-list-live.css"
        context["channel"] = get_object_or_404(Channel, handle=self.kwargs["handle"])

        if self.request.user.is_authenticated:
            channel = get_object_or_404(Channel, handle=self.kwargs["handle"])
            context["subscribed"] = channel.is_subscribed(user=self.request.user)

        vidtype = self.kwargs["vtype"]

        if vidtype == "videos":
            context["type"] = "VIDEO"
        elif vidtype == "shorts":
            context["type"] = "SHORTS"
        elif vidtype == "streams":
            context["type"] = "LIVE"

        return context

class VideoDetailViewGet(DetailView):
    model = Channel
    slug_field = "handle"
    slug_url_kwarg = "handle"
    template_name = "video-detail.html"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        video = get_object_or_404(Video, pk=self.kwargs["video_id"])
        video.views += 1
        video.save()
        context["video"] = video

        timetuple = FunctionLibrary.get_time(video.upload_date)
        timestring = f"{timetuple[0]} {timetuple[1]} ago"
        context["time_after_upload"] = timestring
        context["extra_css3"] = "css/video-detail.css"

        total_count = Video.objects.count()
        if total_count < 15:
            suggestions = Video.objects.exclude(pk=video.pk).order_by("?")[:20]
        else:
            suggestions = Video.objects.exclude(pk=self.kwargs["video_id"]).order_by("?")[:total_count - 1]
        context["suggestions"] = suggestions

        context["form"] = CommentForm()

        if self.request.user.is_authenticated:
            channel = get_object_or_404(Channel, handle=self.kwargs["handle"])
            context["subscribed"] = channel.is_subscribed(user=self.request.user)

        return context

class VideoDetailViewPost(SingleObjectMixin, FormView):
    model = Channel
    form_class = CommentForm
    slug_field = "handle"
    slug_url_kwarg = "handle"
    template_name = "video-detail.html"

    def post(self, request, *args, **kwargs):
        self.object = get_object_or_404(Video, pk=self.kwargs["video_id"])
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.video = self.object
        comment.author = self.request.user
        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        video = self.object
        return reverse("video-detail", kwargs={"handle": video.channel.handle, "video_id": video.pk})

class VideoDetailView(View):
    def get(self, request, *args, **kwargs):
        view = VideoDetailViewGet.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = VideoDetailViewPost.as_view()
        return view(request, *args, **kwargs)