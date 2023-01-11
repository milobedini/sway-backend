from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    email = models.CharField(max_length=50, unique=True)
    favourites = models.ManyToManyField(
        "meditations.Meditation", related_name="favourited_by", default=None)
    sessions = models.IntegerField(default=0)
    minutes = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.username}"
