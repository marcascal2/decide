from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
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


class CensusCreate(generics.ListCreateAPIView):
    permission_classes = (UserIsStaff,)

    def create(self, request, *args, **kwargs):
        voting = request.data.get('voting')
        voters = request.data.get('voters')
        adscripcion = request.data.get('adscripcion')
        date = request.data.get('date')
        try:
            for voter in voters:
                census = Census(voting=voting, voter_id=voter, adscripcion=adscripcion, date=date)
                census.save()
        except IntegrityError:
            return Response('Error try to create census', status=ST_409)
        return Response('Census created', status=ST_201)

    def list(self, request, *args, **kwargs):
        voting = request.GET.get('voting')
        voters = Census.objects.filter(voting=voting).values_list('voter_id', flat=True)
        adscripcion = Census.objects.filter(voting=voting).values_list('adscripcion', flat=True)
        date = Census.objects.filter(voting=voting).values_list('date', flat=True)
        question = Voting.objects.filter(voting=voting).values_list('question', flat=True)
        return Response({'voters': voters, 'adscripcion': adscripcion, 'date': date})


class CensusDetail(generics.RetrieveDestroyAPIView):

    def destroy(self, request, voting_id, *args, **kwargs):
        voters = request.data.get('voters')
        adscripcion = request.data.get('adscripcion')
        date = request.data.get('date')
        census = Census.objects.filter(voting=voting, voter_id__in=voters,adscripcion=adscripcion, date=date)
        census.delete()
        return Response('Voters deleted from census', status=ST_204)

    def retrieve(self, request, voting_id, *args, **kwargs):
        voter = request.GET.get('voter_id')
        adscripcion = request.GET.get('adscripcion')
        date = request.GET.get('date')
        try:
            Census.objects.get(voting=voting, voter_id=voter, adscripcion=adscripcion, date=date)
        except ObjectDoesNotExist:
            return Response('Invalid voter', status=ST_401)
        return Response('Valid voter')
