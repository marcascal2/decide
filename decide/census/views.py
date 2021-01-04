from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
import csv
from django import forms
from django.shortcuts import render
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

def import_by_voting(request, voting_id):
    if not request.user.is_authenticated:
        return render(request, 'login_error.html')

    class UploadDocumentForm(forms.Form):
        file = forms.FileField()

    def save_import(f):
        for row in f:
            if not row.startswith(b'voter_id'):
                cadena = row.decode('utf-8')
                ids = cadena.split(',')
                voter_id = ids[0]
                census = Census(voting_id=voting_id, voter_id=voter_id)
                census.save()
        f.close()

    form = UploadDocumentForm()
    if request.method == 'POST':
        form = UploadDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            save_import(request.FILES['file'])
    else:
        form = UploadDocumentForm()

    return render(request, 'upload.html', {'form': form})

def export_by_voting(request, voting_id):
    field = Census._meta.get_field('voter_id')
    voter_set = Census.objects.filter(voting_id=voting_id)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename={}.csv'.format(field)
    writer = csv.writer(response)
    writer.writerow([field.name])

    for obj in voter_set:
        row = writer.writerow([getattr(obj, field.name)])
    return response