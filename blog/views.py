from django.shortcuts import render
from django.views.generic import ListView
from . import models


# Create your views here.
class RecentBlogs(ListView):
    queryset = models.Blog.objects.recent_published
    template_name = "blog/index.html"
    context_object_name = "recent_blogs"
