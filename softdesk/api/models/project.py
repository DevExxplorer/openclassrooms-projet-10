from django.db import models

from api.models import Contributor


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
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Contributor, on_delete=models.CASCADE, related_name='authored_project', null=True)
