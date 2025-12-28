from django.shortcuts import render
from django.views.generic import TemplateView
from channel.models import Channel
from django.shortcuts import render
class HomePageView(TemplateView):
    model = Channel
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        # Get context from TemplateView
        context = super().get_context_data(**kwargs)

        # Add custom context for the list
        context['channel_list'] = Channel.objects.all()

        return context

