from django.db import models

from api.models import Contributor
from softdesk.api.models.issue import Issue


class Comment(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    contributor = models.ForeignKey(Contributor, on_delete=models.CASCADE)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
