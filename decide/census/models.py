from django.db import models
from django.contrib.auth.models import User

class Census(models.Model):
    voting_id = models.PositiveIntegerField()
    voter_id = models.PositiveIntegerField()

    class Meta:
        unique_together = (('voting_id', 'voter_id'),)


class UserData(models.Model):
    age = models.PositiveIntegerField()
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    def __str__(self):
        return 'Datos del usuario : ' + self.user.username