from django.db import models

from api.models import Project, Contributor, CustomUser


class Issue(models.Model):
    TAG_CHOICES = [
        ('bug', 'Bug'),
        ('task', 'Tâche'),
        ('amelioration', 'Amélioration')
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    contributor = models.ForeignKey(Contributor, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    tag = models.CharField(max_length=255, choices=TAG_CHOICES)
    priority = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)