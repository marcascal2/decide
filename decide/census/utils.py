from django.http import HttpResponse
import csv
from django import forms
from django.shortcuts import render

from .models import Census

def import_from_csv_by_voting():
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

def export_as_csv_by_voting(self, request, queryset):
    field = self.model._meta.get_field('voter_id')
    voter_set = Census.objects.filter(voting_id=1)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename={}.csv'.format(field)
    writer = csv.writer(response)
    writer.writerow([field.name])

    for obj in voter_set:
        row = writer.writerow([getattr(obj, field.name)])
    return response