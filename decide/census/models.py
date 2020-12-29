from django.db import models

from voting.models import Voting
from datetime import date

class Census(models.Model):
    voting = models.OneToOneField(Voting, on_delete=models.CASCADE)
    voter_id = models.PositiveIntegerField()
    adscripcion = models.CharField(max_length=20, blank=True, null=True)
    date = models.DateField(default=date.today)

    class Meta:
        unique_together = (('voting', 'voter_id'),)
