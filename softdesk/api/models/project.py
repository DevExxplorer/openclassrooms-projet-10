from django.db import models

from api.models import CustomUser

class Project(models.Model):
    TYPE_CHOICES = [
        ('back', 'Back-end'),
        ('front', 'Front-end'),
        ('ios', 'IOS'),
        ('android', 'Android')
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    type_project = models.CharField(max_length=10, choices=TYPE_CHOICES)
    author = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name="author_project")
    # contributors = models.ManyToManyField(CustomUser, through='Contributor', related_name="contributors_project")
    created_at = models.DateTimeField(auto_now_add=True)