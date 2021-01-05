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
from django.db.models import Q

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
    dates = [] 
    adscripciones = []
    questions = []

    for c in census:
        u = User.objects.get(id = c.voter_id)  
        if u not in voters:
            voters.append(u)
        
        v = Voting.objects.get(id = c.voting_id)  
        if v not in votings:
            votings.append(v)

        d = c.date
        if d not in dates:
            dates.append(d)
        
        if c.adscripcion not in adscripciones:
            adscripciones.append(c.adscripcion)
        
        q = c.voting_question
        if q not in questions:
            questions.append(q)
    
    return render(request,'all_census.html', {'census':census, 'votings':votings, 'voters':voters, 'dates': dates, 'adscripciones':adscripciones, 'questions': questions})

def group_by_adscripcion(request, adscripcion):
    if not request.user.is_authenticated:
        return render(request, 'login_error.html')

    census = Census.objects.filter(adscripcion= adscripcion)
    users_in_census = []
    
    for censu in census:
        users_in_census.append(censu.voter_id)

    voters = User.objects.filter(id__in=users_in_census)
    votings = Voting.objects.all()
    votings_with_census = []
    
    for v in votings:
        c = Census.objects.filter(voting_id = v.id)
        
        if len(c) != 0:
            votings_with_census.append(v)

    dates = []
    adscripciones = []
    questions = []
    
    for c in Census.objects.all():
        d = c.date
        q = c.voting_question

        if d not in dates:
            dates.append(d)
        
        if c.adscripcion not in adscripciones:
            adscripciones.append(c.adscripcion)
        
        if q not in questions:
            questions.append(q)
    
    return render(request,'all_census.html', {'census':census, 'voters':voters, 'votings':votings_with_census, 'adscripciones':adscripciones, 'dates':dates, 'questions':questions})

def group_by_voting(request, voting_id):
    if not request.user.is_authenticated:
        return render(request, 'login_error.html')

    census = Census.objects.filter(voting_id = voting_id)
    users_in_census = []
    
    for censu in census:
        users_in_census.append(censu.voter_id)
    
    voters = User.objects.filter(id__in=users_in_census)
    votings = Voting.objects.all()
    votings_with_census = []
    
    for v in votings:
        c = Census.objects.filter(voting_id = v.id)
        
        if len(c) != 0:
            votings_with_census.append(v)
    
    dates = []
    adscripciones = []
    questions = []
    
    for c in Census.objects.all():
        d = c.date
        q = c.voting_question
    
        if d not in dates:
            dates.append(d)
    
        if c.adscripcion not in adscripciones:
            adscripciones.append(c.adscripcion)

        if q not in questions:
            questions.append(q)
    
    return render(request,'all_census.html', {'census':census, 'voters':voters, 'votings':votings_with_census, 'dates': dates, 'adscripciones':adscripciones, 'questions': questions})

def group_by_voter(request, voter_id):
    if not request.user.is_authenticated:
        return render(request, 'login_error.html')

    census = Census.objects.filter(voter_id = voter_id)
    votings_in_census = []
    
    for censu in census:
        votings_in_census.append(censu.voting_id)
    
    votings = Voting.objects.filter(id__in=votings_in_census)
    voters = User.objects.all()
    voters_with_census = []
    
    for v in voters:
        c = Census.objects.filter(voter_id = v.id)
    
        if len(c) != 0:
            voters_with_census.append(v)
    
    dates = []
    adscripciones = []
    questions = []
    
    for c in Census.objects.all():
        d = c.date
        q = c.voting_question
    
        if d not in dates:
            dates.append(d)
    
        if c.adscripcion not in adscripciones:
            adscripciones.append(c.adscripcion)

        if q not in questions:
            questions.append(q)
    
    
    return render(request,'all_census.html', {'census':census, 'voters':voters_with_census, 'votings':votings, 'dates': dates, 'adscripciones':adscripciones, 'questions': questions})

def group_by_date(request, date):
    if not request.user.is_authenticated:
        return render(request, 'login_error.html')

    census = Census.objects.filter(date=date)
    votings_in_census = []
    
    for censu in census:
        votings_in_census.append(censu.voting_id)
    
    votings = Voting.objects.filter(id__in=votings_in_census)
    dates = []
    adscripciones = []
    questions = []
    
    for c in Census.objects.all():
        d = c.date
        q = c.voting_question

        if d not in dates:
            dates.append(d)
    
        if c.adscripcion not in adscripciones:
            adscripciones.append(c.adscripcion)
        
        if q not in questions:
            questions.append(q)
    
    voters = User.objects.all()
    voters_with_census = []
    
    for v in voters:
        c = Census.objects.filter(voter_id = v.id)
    
        if len(c) != 0:
            voters_with_census.append(v)
    
    return render(request,'all_census.html', {'census':census, 'dates':dates, 'voters':voters_with_census, 'votings':votings, 'adscripciones':adscripciones, 'questions':questions})

def group_by_question(request, question):
    if not request.user.is_authenticated:
        return render(request, 'login_error.html')

    votings_in_census = []
    
    census = Census.objects.all()  

    for censu in census:
        votings_in_census.append(censu.voting_id)
    
    votings = Voting.objects.filter(id__in=votings_in_census)
    dates = []
    adscripciones = []
    questions = []

    for c in census:

        votings_in_census.append(c.voting_id)

        d = c.date
        q = c.voting_question
        
        if d not in dates:
            dates.append(d)
    
        if c.adscripcion not in adscripciones:
            adscripciones.append(c.adscripcion)

        if q not in questions:
            questions.append(q)
    
    voters = User.objects.all()
    voters_with_census = []
    
    for v in voters:
        c = Census.objects.filter(voter_id = v.id)
    
        if len(c) != 0:
            voters_with_census.append(v)   

    return render(request,'all_census.html', {'census':census, 'dates':dates, 'voters':voters_with_census, 'votings':votings, 'adscripciones':adscripciones, 'questions':questions})

def filter_by(request):
    if not request.user.is_authenticated:
        return render(request, 'login_error.html')

    q = request.POST.get('q', '')
    q = q.lower()

    census = Census.objects.all()
    votaciones = Voting.objects.all()
    users = User.objects.all()

    res = []

    for c in census:
        if q in c.adscripcion.lower():
            res.append(c)

        if q in str(c.date) and c not in res:
            res.append(c)

    for v in votaciones:
        if q in v.name.lower():
            cs = Census.objects.filter(voting_id=v.id)
            for c in cs:
                if c not in res:
                    res.append(c)

    for u in users:
        if q in u.username.lower():
            cs = Census.objects.filter(voter_id=u.id)
            for c in cs:
                if c not in res:
                    res.append(c)
    
    votings_in_census = []

    for censu in census:
        votings_in_census.append(censu.voting_id)
    
    votings = Voting.objects.filter(id__in=votings_in_census)
    dates = []
    adscripciones = []
    questions = []

    for c in census:

        votings_in_census.append(c.voting_id)

        d = c.date
        q = c.voting_question
        
        if d not in dates:
            dates.append(d)
    
        if c.adscripcion not in adscripciones:
            adscripciones.append(c.adscripcion)

        if q not in questions:
            questions.append(q)
    
    voters = User.objects.all()
    voters_with_census = []
    
    for v in voters:
        c = Census.objects.filter(voter_id = v.id)
    
        if len(c) != 0:
            voters_with_census.append(v)

    return render(request,'all_census.html', {'census':res, 'dates':dates, 'voters':voters_with_census, 'votings':votings, 'adscripciones':adscripciones, 'questions':questions})