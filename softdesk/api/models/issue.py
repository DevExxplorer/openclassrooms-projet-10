from django.db import models

from api.models import Project, Contributor
from api.models.user import CustomUser


class Issue(models.Model):
    TYPE_CHOICES = [
        ('bug', 'Bug'),
        ('task', 'Tâche'),
        ('amelioration', 'Amélioration')
    ]

    PRIORITY_CHOICES = [
        ('low', 'Faible'),
        ('medium', 'Moyen'),
        ('hight', 'Elevé')
    ]

    STATUS_CHOICES = [
        ('todo', 'A faire'),
        ('inprogress', 'En cours'),
        ('finished', 'Terminé')
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default='todo')
    priority = models.CharField(max_length=255, choices=PRIORITY_CHOICES)
    author = models.ForeignKey(Contributor, on_delete=models.PROTECT, related_name='authored_issue', null=True)
    type_issue = models.CharField(max_length=255, choices=TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="issues")
