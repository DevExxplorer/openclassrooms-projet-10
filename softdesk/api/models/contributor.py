from django.db import models

class Contributor(models.Model):
    user = models.ForeignKey('api.CustomUser', on_delete=models.CASCADE)
    project = models.ForeignKey('api.Project', on_delete=models.CASCADE, related_name='contributors_project')

    class Meta:
        # Pour éviter qu'un utilisateur soit plusieurs fois contributeur sur le même projet
        unique_together = ('user', 'project')

