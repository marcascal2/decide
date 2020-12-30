from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.models import User

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.status import (
        HTTP_201_CREATED as ST_201,
        HTTP_204_NO_CONTENT as ST_204,
        HTTP_400_BAD_REQUEST as ST_400,
        HTTP_401_UNAUTHORIZED as ST_401,
        HTTP_409_CONFLICT as ST_409
)

from base.perms import UserIsStaff
from .models import Census
from voting.models import Voting
from .forms import CensusAddUserForm


class CensusCreate(generics.ListCreateAPIView):
    permission_classes = (UserIsStaff,)

    def create(self, request, *args, **kwargs):
        voting_id = request.data.get('voting_id')
        voters = request.data.get('voters')
        try:
            for voter in voters:
                census = Census(voting_id=voting_id, voter_id=voter)
                census.save()
        except IntegrityError:
            return Response('Error try to create census', status=ST_409)
        return Response('Census created', status=ST_201)

    def list(self, request, *args, **kwargs):
        voting_id = request.GET.get('voting_id')
        voters = Census.objects.filter(voting_id=voting_id).values_list('voter_id', flat=True)
        return Response({'voters': voters})


class CensusDetail(generics.RetrieveDestroyAPIView):

    def destroy(self, request, voting_id, *args, **kwargs):
        voters = request.data.get('voters')
        census = Census.objects.filter(voting_id=voting_id, voter_id__in=voters)
        census.delete()
        return Response('Voters deleted from census', status=ST_204)

    def retrieve(self, request, voting_id, *args, **kwargs):
        voter = request.GET.get('voter_id')
        try:
            Census.objects.get(voting_id=voting_id, voter_id=voter)
        except ObjectDoesNotExist:
            return Response('Invalid voter', status=ST_401)
        return Response('Valid voter')

def render_panel_administracion(request):
    if not request.user.is_authenticated:
        return render(request, 'login_error.html')
    votings = Voting.objects.all()
    return render(request, 'manage_census.html', { 'votings': votings})

def voting_census(request, voting_id):
    if not request.user.is_authenticated:
        return render(request, 'login_error.html')
    
    if request.method == 'POST':
        form = CensusAddUserForm(voting_id, request.POST)
        if form.is_valid():
            user_to_add = form.cleaned_data['user_to_add']
            add_user_to_voting(user_to_add, voting_id)
            return redirect('voting_census', voting_id = voting_id)

    else:
        form = CensusAddUserForm(voting_id)

    voting = Voting.objects.get(id = voting_id)
    census = Census.objects.filter(voting_id = voting_id)
    users_in_census = []
    for censu in census:
        users_in_census.append(censu.voter_id)
    users = User.objects.filter(id__in=users_in_census)
    return render(request, 'voting_census.html', {'voting': voting, 'users': users, 'form': form})


#Funciones auxiliares
def add_user_to_voting(user_id, voting_id):
    Census.objects.create(voter_id = user_id, voting_id = voting_id)