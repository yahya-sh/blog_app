import factory
import random
from factory.django import DjangoModelFactory
from blog import models
from faker import Faker
from pytest_factoryboy import register
from .blog_tags import BLOG_TAGS
from django.utils import timezone
from user.tests.factories import UserFactory

fake = Faker()


@register
class TagFactory(DjangoModelFactory):
    class Meta:
        model = models.Tag
        django_get_or_create = ("name",)

    # @lazy_attribute
    # def name(self):
    #     return fake.word().title()

    # name = factory.Iterator(BLOG_TAGS, cycle=True)

    name = factory.Faker(
        "random_element",
        elements=BLOG_TAGS,
    )


@register
class BlogFactory(DjangoModelFactory):
    class Meta:
        model = models.Blog
        skip_postgeneration_save = True

    class Params:
        published_blog = factory.Trait(
            published=True,
            published_at=factory.Faker(
                "date_time_this_year",
                tzinfo=timezone.get_current_timezone(),
            ),
        )

    author = factory.SubFactory(UserFactory)

    title = factory.Faker("sentence", nb_words=5)
    content = factory.Faker("paragraph", nb_sentences=10)

    published = False
    published_at = None

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            return

        if isinstance(extracted, int):
            self.tags.add(*TagFactory.create_batch(extracted))

        elif extracted:
            self.tags.add(*extracted)

        else:
            self.tags.add(*TagFactory.create_batch(random.randint(1, 5)))
