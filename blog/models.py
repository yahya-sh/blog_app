from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.


class Tag(models.Model):
    slug = models.SlugField(unique=True)


class Blog(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField("blog title", max_length=255)
    content = models.TextField("the blog content")
    tags = models.ManyToManyField(Tag, related_name="blogs")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=False)
