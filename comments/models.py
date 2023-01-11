from django.db import models

# Create your models here.


class Comment(models.Model):
    text = models.TextField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    article = models.ForeignKey(
        "articles.Article", related_name="comments", on_delete=models.CASCADE)
    owner = models.ForeignKey(
        "jwt_auth.User", related_name="comments", on_delete=models.CASCADE)
