from django import forms
from django.contrib.auth.models import User
from .models import Census
from voting.models import Voting

class CensusAddUserForm(forms.Form):

    def __init__(self,voting_id,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.voting_id=voting_id 
        census = Census.objects.filter(voting_id = voting_id)
        users = User.objects.all()
        census_users = []

        pending_users = []

        for censu in census:
            census_users.append(censu.voter_id)

        for user in users:
            if user.id not in census_users:
                pending_users.append([user.id, user.username])


        self.fields['user_to_add'] = forms.ChoiceField(label="Añadir usuario", choices=pending_users)
        

    user_to_add = forms.ChoiceField(choices=[])

    def clean(self):
        try:
            cleaned_data = super().clean()
            user_to_add = cleaned_data.get("user_to_add")
            if user_to_add is not None:
                voting = Voting.objects.get(id=self.voting_id)
                user = User.objects.get(id=user_to_add)
                if user.userdata is not None:
                    age = user.userdata.age
                    if voting.min_age is not None and age < voting.min_age:
                            self.add_error('user_to_add', 'El usuario no cumple con la edad mínima')
                    if voting.max_age is not None and age > voting.max_age:
                            self.add_error('user_to_add', 'El usuario no cumple con la edad máxima')
        except User.userdata.RelatedObjectDoesNotExist:
            self.add_error('user_to_add', 'El usuario a agregar no tiene edad registrada')
