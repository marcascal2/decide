from django.db.utils import IntegrityError
from django.db.models.base import Model 
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics
from django.shortcuts import render
from django.shortcuts import redirect
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
from django.contrib.auth.models import User


class CensusCreate(generics.ListCreateAPIView):
    permission_classes = (UserIsStaff,)

    def create(self, request, *args, **kwargs):
        voting_id = request.data.get('voting_id')
        voters = request.data.get('voters')
        adscripcion = request.data.get('adscripcion')
        try:
            for voter in voters:
                census = Census(voting_id=voting_id, voter_id=voter, adscripcion=adscripcion)
                census.save()
        except IntegrityError:
            return Response('Error try to create census', status=ST_409)
        return Response('Census created', status=ST_201)

    def list(self, request, *args, **kwargs):
        voting_id = request.GET.get('voting_id')
        voters = Census.objects.filter(voting_id=voting_id).values_list('voter_id', flat=True)
        # adscripcion = Census.objects.filter(voting_id=voting_id).values_list('adscripcion', flat=True)
        # date = Census.objects.filter(voting_id=voting_id).values_list('date', flat=True)
        return Response({'voters': voters})

class CensusDetail(generics.RetrieveDestroyAPIView):

    def destroy(self, request, voting_id, *args, **kwargs):
        voters = request.data.get('voters')
        adscripcion = request.data.get('adscripcion')
        date = request.data.get('date')
        try:
            for voter in voters:
                census = Census.objects.filter(voting_id=voting_id, voter_id=voter,adscripcion=adscripcion, date=date)
                census.delete()
        except IntegrityError:
            return Response('Error try to delete census', status=ST_409)
        return Response('Voters deleted from census', status=ST_204)

    def retrieve(self, request, voting_id, *args, **kwargs):
        voter = request.GET.get('voter_id')
        try:
            Census.objects.get(voting_id=voting_id, voter_id=voter)
        except ObjectDoesNotExist:
            return Response('Invalid voter', status=ST_401)
        return Response('Valid voter')

def group_by_voter(request):
    if not request.user.is_authenticated:
        return render(request, 'login_error.html')
    voters = User.objects.all()
    voters_with_census = []
    for voter in voters:
        census = Census.objects.filter(voter_id=voter.id)
        if len(census) != 0:
            voters_with_census.append(voter)

    return render(request, 'manage_grouping_voter.html', { 'voters': voters_with_census})

def voter_census(request, voter_id):
    if not request.user.is_authenticated:
        return render(request, 'login_error.html')
    voter = User.objects.get(id = voter_id)
    census = Census.objects.filter(voter_id = voter_id)
    votings = []
    for c in census:
        votings.append(Voting.objects.get(id = c.voting_id))
    
    return render(request, 'voter_census.html', {'census': census, 'voter': voter, 'votings': votings})

def group_by_voting(request):
    if not request.user.is_authenticated:
        return render(request, 'login_error.html')
    votings = Voting.objects.all()
    votings_with_census = []
    for voting in votings:
        census = Census.objects.filter(voting_id = voting.id)
        if len(census) != 0:
            votings_with_census.append(voting)
        
    return render(request, 'manage_grouping_voting.html', { 'votings': votings_with_census})

def voting_census(request, voting_id):
    if not request.user.is_authenticated:
        return render(request, 'login_error.html')

    voting = Voting.objects.get(id = voting_id)
    census = Census.objects.filter(voting_id = voting_id)
    voters = []
    for c in census:  
        u = User.objects.get(id = c.voter_id)  
        voters.append(u)
    return render(request, 'voting_census.html', {'census': census, 'voting': voting, 'voters': voters})

    