import pytest
from tests.conftest import * # noqa: F403
import datetime
from django.db import IntegrityError


@pytest.mark.django_db
def test_publishing_blog_auto_assign_published_at(blog_factory: BlogFactory):
    """
    Ensure the 'published_at' timestamp is automatically set when a blog is published.

    Given: A blog post created with 'published=False' and no publish timestamp.
    When: The 'published' status is updated to True and the model is saved.
    Then: The 'published_at' field should automatically contain a valid datetime object.
    """
    # Given
    blog = blog_factory.create(published=False)
    # When
    blog.published = True
    blog.save()
    # Then
    assert isinstance(blog.published_at, datetime.datetime)


@pytest.mark.django_db
def test_republishing_blog_should_not_change_old_published_at_value(
    blog_factory: BlogFactory,
):
    """
    Verify that unpublishing and republishing a blog preserves its original 'published_at' timestamp.

    Given: An already published blog post with an existing 'published_at' value.
    When: The blog is unpublished (published=False), saved, and then republished (published=True) and saved again.
    Then: The 'published_at' timestamp must remain identical to the original value without being overwritten.
    """
    # Given
    blog = blog_factory.create(published_blog=True)
    published_at = blog.published_at
    # When
    blog.published = False
    blog.save()
    blog.published = True
    blog.save()
    # Then
    assert blog.published_at == published_at


@pytest.mark.django_db
def test_blog_slug_is_auto_generated(blog_factory: BlogFactory, user):
    """
    Confirm that a unique URL slug is automatically generated upon the first database save.

    Given: A new blog instance built in memory (not yet saved) with an empty slug field.
    When: An author is assigned and the blog instance is saved to the database.
    Then: The 'slug' field should be populated automatically (typically generated from the title).
    """
    # Given
    blog = blog_factory.build()
    assert not blog.slug
    blog.author = user
    # When
    blog.save()
    # Then
    assert blog.slug


@pytest.mark.django_db
def test_no_blog_slug_duplicate(blog_factory: BlogFactory):
    """
    Ensure that blog slugs must remain unique and cannot be duplicated via case-insensitive titles.

    Given: A blog post is created with a specific title.
    When: Another blog is created using the same title (in a different case),
    Then: The system should raise an IntegrityError due to the unique constraint on the slug field,
    preventing duplicate blog slugs from being inserted into the database.
    """
    # Given
    title = "Sample Title"
    blog_factory.create(title=title)
    title = title.lower()
    # Then
    with pytest.raises(IntegrityError):
        # When
        blog_factory.create(title=title)
