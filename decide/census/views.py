from django.db.utils import IntegrityError
from django.db.models.base import Model 
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
import csv
from django import forms
from django.shortcuts import render
from django.shortcuts import redirect

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
from datetime import date, datetime
from .forms import CensusAddUserForm

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
    
    return render(request,'admin.html', {'census':census, 'votings':votings, 'voters':voters, 'adscripciones':adscripciones, 'dates': dates, 'questions': questions})

def group_by_adscripcion(request, adscripcion):
    if not request.user.is_authenticated:
        return render(request, 'login_error.html')

    if adscripcion=='None':
        census = Census.objects.filter(adscripcion= None)
    else:
        census = Census.objects.filter(adscripcion= adscripcion)

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
    
    return render(request,'admin.html', {'census':census, 'voters':voters, 'votings':votings, 'adscripciones':adscripciones, 'dates':dates, 'questions':questions})

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
    
    return render(request,'admin.html', {'census':census, 'voters':voters, 'votings':votings, 'dates': dates, 'adscripciones':adscripciones, 'questions': questions})

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
    
    
    return render(request,'admin.html', {'census':census, 'voters':voters, 'votings':votings, 'dates': dates, 'adscripciones':adscripciones, 'questions': questions})

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
    
    return render(request,'admin.html', {'census':census, 'dates':dates, 'voters':voters, 'votings':votings, 'adscripciones':adscripciones, 'questions':questions})

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
    
    return render(request,'admin.html', {'census':census, 'dates':dates, 'voters':voters, 'votings':votings, 'adscripciones':adscripciones, 'questions':questions})

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
        if c.adscripcion != None:
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

    for c in census:

        d = c.date
        q = c.voting_question
        
        if d not in dates:
            dates.append(d)
    
        if c.adscripcion not in adscripciones:
            adscripciones.append(c.adscripcion)

        if q not in questions:
            questions.append(q)

    return render(request,'admin.html', {'census':res, 'dates':dates, 'voters':voters, 'votings':votings, 'adscripciones':adscripciones, 'questions':questions})

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

#TODO: Frontend
def import_by_voting(request):
    if not request.user.is_authenticated:
        return render(request, 'login_error.html')

    class UploadDocumentForm(forms.Form):
        file = forms.FileField()
        voting_id = forms.CharField()

    def save_import(f, voting_id):
        for row in f:
            if not row.startswith(b'voter_id'):
                cadena = row.decode('utf-8')
                ids = cadena.split(',')
                voter_id = ids[0]
                adscripcion = ids[1]
                if adscripcion == '': adscripcion=None
                dat = ids[2]
                objDate = datetime.strptime(dat, '%Y-%m-%d')
                census = Census(voting_id=voting_id, voter_id=voter_id, adscripcion=adscripcion, date=objDate)
                census.save()
        f.close()

    form = UploadDocumentForm()
    if request.method == 'POST':
        form = UploadDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            save_import(request.FILES['file'], request.POST.get('voting_id', ''))
            return render(request, 'succes.html', locals())
    else:
        form = UploadDocumentForm()
    
    return render(request, 'upload.html', {'form': form})

#TODO: Frontend
def export_by_voting(request, voting_id):
    meta = Census._meta
    field_names = [field.name for field in meta.fields]
    field_names.remove('id')
    field_names.remove('voting_id')
    voter_set = Census.objects.filter(voting_id=voting_id)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
    writer = csv.writer(response)
    writer.writerow(field_names)

    for obj in voter_set:
        row = writer.writerow([getattr(obj, field) for field in field_names] + [''])
    return response


#TODO: Unir a las vistas existentes
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
