import uuid
from django.db import models
from api.models import Contributor
from api.models.issue import Issue


class Comment(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='comments')
    description = models.TextField()
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Contributor, on_delete=models.PROTECT, related_name='authored_comment', null=True)
