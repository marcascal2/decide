from django.db import models

from voting.models import Voting
from django.contrib.auth.models import User
from datetime import date

class CensusGroupByVoting(models.Model):
    voting = models.OneToOneField(Voting, on_delete=models.CASCADE)

    def census_number(self):
        census = Census.objects.filter(voting=self.voting).all()
        return len(census)
    
    def census(self):
        census = Census.objects.filter(voting=self.voting).values('voter__username').all()

        return ', '.join(str(item['voter__username']) for item in census)

    class Meta:
        unique_together = (('voting',),)

class CensusGroupByVoter(models.Model):
    voter = models.OneToOneField(User, on_delete=models.CASCADE)

    def census_number(self):
        census = Census.objects.filter(voter=self.voter).all()
        return len(census)

    def census(self):
        census = Census.objects.filter(voter=self.voter).values('voting__name').all()

        return ', '.join(str(item['voting__name']) for item in census)

    class Meta:
        unique_together = (('voter',),)

class Census(models.Model):
    voting = models.ForeignKey(Voting, on_delete=models.CASCADE)
    voter = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    adscripcion = models.CharField(max_length=20, blank=True, null=True)
    date = models.DateField(default=date.today)

    class Meta:
        unique_together = (('voting', 'voter'),)