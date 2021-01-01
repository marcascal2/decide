from django.db.utils import IntegrityError
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
from .models import Census, CensusGroupByVoting, CensusGroupByVoter
from voting.models import Voting
from django.contrib.auth.models import User


class CensusCreate(generics.ListCreateAPIView):
    permission_classes = (UserIsStaff,)

    def create(self, request, *args, **kwargs):
        voting = request.data.get('voting_id')
        voters = request.data.get('voters')
        adscripcion = request.data.get('adscripcion')
        try:
            for voter in voters:
                voting_object = Voting.objects.get(id=voting)
                voter_object = User.objects.get(id=voter)
                census = Census(voting=voting_object, voter=voter_object, adscripcion=adscripcion)
                census.save()
        except IntegrityError:
            return Response('Error try to create census', status=ST_409)
        return Response('Census created', status=ST_201)

    def list(self, request, *args, **kwargs):
        voting = request.GET.get('voting')
        voters = Census.objects.filter(voting=voting).values_list('voter', flat=True)
        adscripcion = Census.objects.filter(voting=voting).values_list('adscripcion', flat=True)
        date = Census.objects.filter(voting=voting).values_list('date', flat=True)
        return Response({'voter': voters, 'adscripcion': adscripcion, 'date': date})

class CensusDetail(generics.RetrieveDestroyAPIView):

    def destroy(self, request, voting, *args, **kwargs):
        voters = request.data.get('voters')
        adscripcion = request.data.get('adscripcion')
        date = request.data.get('date')
        census = Census.objects.filter(voting=voting, voter=voters,adscripcion=adscripcion, date=date)
        census.delete()
        return Response('Voters deleted from census', status=ST_204)

    def retrieve(self, request, voting, *args, **kwargs):
        voter = request.GET.get('voter')
        adscripcion = request.GET.get('adscripcion')
        date = request.GET.get('date')
        try:
            Census.objects.get(voting=voting, voter=voter, adscripcion=adscripcion, date=date)
        except ObjectDoesNotExist:
            return Response('Invalid voter', status=ST_401)
        return Response('Valid voter')

def group_by_voter(request):
    if not request.user.is_authenticated:
        return render(request, 'login_error.html')
    voter_id = request.get('voter_id') 
    voter = User.objects.get(id = voter_id)
    census = Census.objects.filter(voter=voter)
    return render(request, 'manage_census.html', { 'census': census})

