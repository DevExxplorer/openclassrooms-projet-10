from django.db import models

from api.models import CustomUser
from softdesk.api.models.project import Project


class Contributor(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    class Meta:
        # Pour éviter qu'un utilisateur soit plusieurs fois contributeur sur le même projet
        unique_together = ('user', 'project')

    def __str__(self):
        return f"{self.user.username} - {self.project.name} ({self.get_role_display()})"
