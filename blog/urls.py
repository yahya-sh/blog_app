from django.urls import path
from . import views


app_name = "blog"
urlpatterns = [
    path("", views.RecentBlogs.as_view(), name="index"),
    path("blogs/", views.AllBlogs.as_view(), name="blog-list"),
    path("my/", views.UserBlogs.as_view(), name="my"),
    path('blogs/<int:blog_id>/', view=views.BlogDetail.as_view(), name='blog-id'),
    path('blogs/<slug:slug>/', view=views.BlogDetail.as_view(), name='blog-slug'),
]
