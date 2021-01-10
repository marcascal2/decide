from django.db import models

from voting.models import Voting
from datetime import date
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Census(models.Model):
    voting_id = models.PositiveIntegerField()
    voter_id = models.PositiveIntegerField()
    adscripcion = models.CharField(max_length=20, blank=True, null=True)
    date = models.DateField(default=date.today)

    @property
    def voting_name(self):
        name = Voting.objects.get(id = self.voting_id).name
        return name
    
    @property
    def voter_username(self):
        username = User.objects.get(id = self.voter_id).username
        return username

    @property
    def voting_question(self):
        desc = Voting.objects.get(id = self.voting_id).question.desc
        return desc

    class Meta:
        unique_together = (('voting_id', 'voter_id'),)

    def __str__(self):
        return str(self.voting_id)

class UserData(models.Model):
    age = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(125)])
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    def __str__(self):
        return 'Datos del usuario : ' + self.user.username
