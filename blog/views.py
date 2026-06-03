from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from . import models


# Create your views here.
class RecentBlogs(ListView):
    queryset = models.Blog.objects.recent_published
    template_name = "blog/index.html"
    context_object_name = "recent_blogs"

class AllBlogs(ListView):
    model = models.Blog
    template_name = "blog/all_blogs.html"
    context_object_name = "blogs"

class UserBlogs(LoginRequiredMixin, ListView):
    template_name = "blog/all_blogs.html"
    context_object_name = "blogs"
    def get_queryset(self):
        user = self.request.user
        return models.Blog.objects.user_blogs(user)
    
