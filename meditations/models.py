from django.db import models

# Create your models here.


class Meditation(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    audio = models.CharField(max_length=600)
    category = models.CharField(max_length=100)
    minutes = models.SmallIntegerField()
    sessions = models.SmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Meditation " + self.name
