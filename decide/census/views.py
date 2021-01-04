from django.db.utils import IntegrityError
from django.db.models.base import Model 
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics
from django.shortcuts import render, redirect
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

#Auth
from django.contrib.auth import logout as do_logout
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as do_login


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

def logout(request):
    # Finalizamos la sesión
    do_logout(request)
    # Redireccionamos a la portada
    return redirect('/census/admin/')
    
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

def group_by_adscripcion(request):
    if not request.user.is_authenticated:
        return render(request, 'login_error.html')
    
    census = Census.objects.all()
    adscripciones = []

    for c in census:
        if c.adscripcion not in adscripciones:
            adscripciones.append(c.adscripcion)

    return render(request, 'manage_grouping_adscripcion.html', { 'adscripciones': adscripciones})

def adscripcion_census(request, adscripcion):
    if not request.user.is_authenticated:
        return render(request, 'login_error.html')

    census = Census.objects.filter(adscripcion=adscripcion)

    return render(request, 'adscripcion_census.html', {'adscripcion':adscripcion, 'census':census})

def filter_by_adscripcion(request, adscripcion):
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
    
    return render(request,'admin.html', {'census':census, 'voters':voters, 'votings':votings_with_census, 'adscripciones':adscripciones, 'dates':dates, 'questions':questions})

def filter_by_voting(request, voting_id):
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
    
    return render(request,'admin.html', {'census':census, 'voters':voters, 'votings':votings_with_census, 'dates': dates, 'adscripciones':adscripciones, 'questions': questions})

def filter_by_voter(request, voter_id):
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
    
    
    return render(request,'admin.html', {'census':census, 'voters':voters_with_census, 'votings':votings, 'dates': dates, 'adscripciones':adscripciones, 'questions': questions})

def filter_by_date(request, date):
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
    
    return render(request,'admin.html', {'census':census, 'dates':dates, 'voters':voters_with_census, 'votings':votings, 'adscripciones':adscripciones, 'questions':questions})

def filter_by_question(request, question):
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

    return render(request,'admin.html', {'census':census, 'dates':dates, 'voters':voters_with_census, 'votings':votings, 'adscripciones':adscripciones, 'questions':questions})

def adminView(request):
    if not request.user.is_authenticated:
        return redirect('login')

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
    
    return render(request, 'admin.html', {'census':census, 'votings':votings, 'voters':voters, 'dates': dates, 'adscripciones':adscripciones, 'questions': questions})

def login(request):
    form = AuthenticationForm()
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        # Verificamos las credenciales del usuario
        user = authenticate(request,username=username, password=password)
        
        # Si existe un usuario con ese nombre y contraseña logueamos
        if user is not None:
            do_login(request, user)
            return redirect('/census/admin')

    return render(request, "login.html", {'form': form})
