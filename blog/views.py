from django.shortcuts import render
from django.views.generic import ListView, DetailView
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
    
class BlogDetail(DetailView):
    model = models.Blog
    pk_url_kwarg = "blog_id"
    slug_url_kwarg = 'slug'
    query_pk_and_slug = True
    template_name = 'blog/detail.html'
