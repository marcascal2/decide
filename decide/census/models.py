from django.db import models

from voting.models import Voting
from django.contrib.auth.models import User
from datetime import date

class Census(models.Model):
    voting_id = models.PositiveIntegerField()
    voter_id = models.PositiveIntegerField()
    adscripcion = models.CharField(max_length=20, blank=True, null=True)
    date = models.DateField(default=date.today)

    def voting_name(self):
        return Voting.objects.get(id = self.voting_id).name
    
    def voter_username(self):
        return User.objects.get(id = self.voter_id).username

    def voting_question(self):
        return Voting.objects.get(id = self.voting_id).question.desc

    class Meta:
        unique_together = (('voting_id', 'voter_id'),)