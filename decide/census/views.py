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
from datetime import date


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
        return Response({'voters': voters})

class CensusDetail(generics.RetrieveDestroyAPIView):

    def destroy(self, request, voting_id, *args, **kwargs):
        voters = request.data.get('voters')
        try:
            for voter in voters:
                census = Census.objects.filter(voting_id=voting_id, voter_id=voter)
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

def all_census(request):
    if not request.user.is_authenticated:
        return render(request, 'login_error.html')

    census = Census.objects.all()
    votings = []
    voters = []
    adscripciones = []
    dates = [] 
    questions = []

    for c in census:
        v = Voting.objects.get(id = c.voting_id)  
        if v not in votings:
            votings.append(v)

        u = User.objects.get(id = c.voter_id)  
        if u not in voters:
            voters.append(u)

        a = c.adscripcion
        if a not in adscripciones:
            adscripciones.append(a)

        d = c.date
        if d not in dates:
            dates.append(d)
        
        q = c.voting_question
        if q not in questions:
            questions.append(q)
    
    return render(request,'all_census.html', {'census':census, 'votings':votings, 'voters':voters, 'adscripciones':adscripciones, 'dates': dates, 'questions': questions})

def group_by_adscripcion(request, adscripcion):
    if not request.user.is_authenticated:
        return render(request, 'login_error.html')

    census = Census.objects.filter(adscripcion = adscripcion)

    all_votings = Voting.objects.all()
    votings = []
    for v in all_votings:
        c = Census.objects.filter(voting_id = v.id)
        if len(c) != 0:
            votings.append(v)

    all_voters = User.objects.all()
    voters = []
    for v in all_voters:
        c = Census.objects.filter(voter_id = v.id)
        if len(c) != 0:
            voters.append(v)

    adscripciones = []
    dates = []
    questions = []
    
    for c in Census.objects.all():
        a = c.adscripcion
        d = c.date
        q = c.voting_question

        if a not in adscripciones:
            adscripciones.append(a)

        if d not in dates:
            dates.append(d)
        
        if q not in questions:
            questions.append(q)
    
    return render(request,'all_census.html', {'census':census, 'voters':voters, 'votings':votings, 'adscripciones':adscripciones, 'dates':dates, 'questions':questions})

def group_by_voting(request, voting_id):
    if not request.user.is_authenticated:
        return render(request, 'login_error.html')

    census = Census.objects.filter(voting_id = voting_id)
    
    all_voters = User.objects.all()
    voters = []
    for v in all_voters:
        c = Census.objects.filter(voter_id = v.id)
        if len(c) != 0:
            voters.append(v)

    all_votings = Voting.objects.all()
    votings = []
    for v in all_votings:
        c = Census.objects.filter(voting_id = v.id)
        if len(c) != 0:
            votings.append(v)
    
    dates = []
    adscripciones = []
    questions = []
    
    for c in Census.objects.all():
        d = c.date
        q = c.voting_question
        a = c.adscripcion 
    
        if d not in dates:
            dates.append(d)
    
        if a not in adscripciones:
            adscripciones.append(a)

        if q not in questions:
            questions.append(q)
    
    return render(request,'all_census.html', {'census':census, 'voters':voters, 'votings':votings, 'dates': dates, 'adscripciones':adscripciones, 'questions': questions})

def group_by_voter(request, voter_id):
    if not request.user.is_authenticated:
        return render(request, 'login_error.html')

    census = Census.objects.filter(voter_id = voter_id)

    all_votings = Voting.objects.all()
    votings = []
    for v in all_votings:
        c = Census.objects.filter(voting_id = v.id)
        if len(c) != 0:
            votings.append(v)

    all_voters = User.objects.all()
    voters = []
    for v in all_voters:
        c = Census.objects.filter(voter_id = v.id)
        if len(c) != 0:
            voters.append(v)
    
    dates = []
    adscripciones = []
    questions = []
    
    for c in Census.objects.all():
        d = c.date
        q = c.voting_question
        a = c.adscripcion
    
        if d not in dates:
            dates.append(d)
    
        if a not in adscripciones:
            adscripciones.append(a)

        if q not in questions:
            questions.append(q)
    
    
    return render(request,'all_census.html', {'census':census, 'voters':voters, 'votings':votings, 'dates': dates, 'adscripciones':adscripciones, 'questions': questions})

def group_by_date(request, date):
    if not request.user.is_authenticated:
        return render(request, 'login_error.html')

    census = Census.objects.filter(date=date)
    
    all_voters = User.objects.all()
    voters = []
    for v in all_voters:
        c = Census.objects.filter(voter_id = v.id)
        if len(c) != 0:
            voters.append(v)

    all_votings = Voting.objects.all()
    votings = []
    for v in all_votings:
        c = Census.objects.filter(voting_id = v.id)
        if len(c) != 0:
            votings.append(v)

    dates = []
    adscripciones = []
    questions = []
    
    for c in Census.objects.all():
        d = c.date
        q = c.voting_question
        a = c.adscripcion

        if d not in dates:
            dates.append(d)
    
        if a not in adscripciones:
            adscripciones.append(a)
        
        if q not in questions:
            questions.append(q)
    
    return render(request,'all_census.html', {'census':census, 'dates':dates, 'voters':voters, 'votings':votings, 'adscripciones':adscripciones, 'questions':questions})

def group_by_question(request, question):
    if not request.user.is_authenticated:
        return render(request, 'login_error.html')

    votings_q = Voting.objects.filter(question__desc=question)
    census = Census.objects.filter(voting_id__in=votings_q)

    all_voters = User.objects.all()
    voters = []
    for v in all_voters:
        c = Census.objects.filter(voter_id = v.id)
        if len(c) != 0:
            voters.append(v)

    all_votings = Voting.objects.all()
    votings = []
    for v in all_votings:
        c = Census.objects.filter(voting_id = v.id)
        if len(c) != 0:
            votings.append(v)

    dates = []
    adscripciones = []
    questions = []
    
    for c in Census.objects.all():
        d = c.date
        q = c.voting_question
        a = c.adscripcion

        if d not in dates:
            dates.append(d)
        
        if a not in adscripciones:
            adscripciones.append(a)
        
        if q not in questions:
            questions.append(q)
    
    return render(request,'all_census.html', {'census':census, 'dates':dates, 'voters':voters, 'votings':votings, 'adscripciones':adscripciones, 'questions':questions})