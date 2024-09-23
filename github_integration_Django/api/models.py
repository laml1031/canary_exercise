from django.db import models


class User(models.Model):
    google_id = models.CharField(max_length=255)
    github_id = models.CharField(max_length=255)
    github_token = models.CharField(max_length=255)
    selected_repo = models.CharField(max_length=255)
