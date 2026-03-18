import factory
from faker import Faker
from django.contrib.auth import get_user_model
from django.utils import timezone

from .models import Post

User = get_user_model()
FAKE = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    """
    Factory for the Django User model.
    Creates simple, unique users suitable for a basic blog app.
    """

    class Meta:
        model = User
        django_get_or_create = ("username",)

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
    # username = factory.LazyAttribute(lambda _: fake.name()) #This will create random names ratherthan User0,1....
    # email = factory.LazyAttribute(lambda _: fake.email())


class PostFactory(factory.django.DjangoModelFactory):
    """
    Factory for the Post model.
    Generates realistic titles, content, and associates each post with a user.
    """

    class Meta:
        model = Post

    title = factory.Faker("sentence", nb_words=6)
    content = factory.LazyFunction(
        lambda: "\n".join(
            FAKE.paragraph(nb_sentences=5) for _ in range(5)
        )
    )
    date_posted = factory.LazyFunction(timezone.now)
    author = factory.SubFactory(UserFactory)