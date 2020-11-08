from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinLengthValidator


class User(AbstractUser):
    follows = models.ManyToManyField('self', related_name='followers', symmetrical=False)

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "follows": [user.username for user in self.follows.all()],
        }

class Post(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="posts")
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
    edited_at = models.DateTimeField(auto_now=True, null=True)
    text = models.TextField(
        max_length=280,
        validators=[MinLengthValidator(2, "Make must be greater than 1 character")])
    likes = models.ManyToManyField(User, related_name="liked")

    def serialize(self):
        return {
            "id": self.id,
            "owner": self.owner,
            "timestamp": self.timestamp,
            "text": self.text,
            "likes": self.likes
        }

    def __string__(self):
        """String for representing the Model object."""
        return f"{self.owner}: {self.text}"

