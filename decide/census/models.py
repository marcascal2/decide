from django.db import models

from voting.models import Voting
from datetime import date
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError, ObjectDoesNotExist
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

    def clean(self):
        try:
            voting = Voting.objects.get(id=self.voting_id)
            user = User.objects.get(id=self.voter_id)
            if user.userdata is not None:
                age = user.userdata.age
                location = user.userdata.location
                if voting.min_age is not None and age < voting.min_age:
                        raise ValidationError('El usuario no cumple con la edad mínima')
                if voting.max_age is not None and age > voting.max_age:
                        raise ValidationError('El usuario no cumple con la edad máxima')
                if voting.location is not '' and location != voting.location:
                        raise ValidationError('La localización del usuario no cumple los requisitos')
        except User.userdata.RelatedObjectDoesNotExist:
            raise ValidationError('El usuario a agregar no tiene informacion registrada')
        except ObjectDoesNotExist:
            raise ValidationError('No existe el voting o el user elegido')

class UserData(models.Model):
    age = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(125)])
    location = models.CharField(max_length=200, blank=True, null=True)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    def __str__(self):
        return 'Datos del usuario : ' + self.user.username
