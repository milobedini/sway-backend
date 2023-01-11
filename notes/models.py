from django.db import models

# Create your models here.


class Note(models.Model):
    date = models.DateField(auto_now_add=True)
    text = models.TextField(max_length=600)
    owner = models.ForeignKey(
        "jwt_auth.User", related_name="notes", on_delete=models.CASCADE)

    def __str__(self):
        return f"Note {self.owner} {self.date}"
