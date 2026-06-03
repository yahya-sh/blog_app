from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.utils import timezone
# Create your models here.


class Tag(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, editable=False)

    def save(self, *args, **kwargs):
        # Generate the slug only if it doesn't exist yet (prevents breaking URLs on title updates)
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name.capitalize()

class BlogManager(models.Manager):
    def recent(self):
        return self.filter()


class Blog(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField("blog title", max_length=255)
    slug = models.SlugField(unique=True, editable=False)
    content = models.TextField("the blog content")
    tags = models.ManyToManyField(Tag, related_name="blogs")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True)

    def save(self, *args, **kwargs):
        # Generate the slug only if it doesn't exist yet (prevents breaking URLs on title updates)
        if not self.slug:
            self.slug = slugify(self.title)
        
        # Set value to published_at field if it's None & published field is enabled
        if self.published_at is None and self.published:
            self.published_at = timezone.now()

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
