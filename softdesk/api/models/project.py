from django.db import models


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