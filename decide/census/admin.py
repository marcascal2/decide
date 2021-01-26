from django.contrib import admin
from django.http import HttpResponse
import csv
from django import forms
from django.shortcuts import render
from django.urls import path

from voting.models import Voting
from datetime import datetime
from .models import Census, UserData
from django.contrib.auth.models import User


class CensusAdmin(admin.ModelAdmin):

    change_list_template = "import.html"

    list_display = ('voting_name', 'voter_username','adscripcion','date')
    list_filter = ('voting_id', 'voter_id','adscripcion','date')

    search_fields = ('voter', 'adscripcion')

    actions = ['export_as_csv']

    def export_as_csv(self, request, queryset):
        meta = Census._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)
        writer.writerow(field_names)

        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names]+[''])
        return response

    export_as_csv.short_description = 'Export as CSV'

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('import/', self.import_from_csv),
        ]
        return my_urls + urls

    def import_from_csv(self, request):
        class UploadDocumentForm(forms.Form):
            file = forms.FileField()

        def save_import(f, voting_id):
            voting = Voting.objects.get(id=voting_id)
            census_list = []

            for row in f:
                if not row.startswith(b'voter_id'):
                    cadena = row.decode('utf-8')
                    ids = cadena.split(',')
                    voter_id = ids[0]
                    user = User.objects.get(id=voter_id)
                    if user.userdata is not None:
                        edad = user.userdata.age
                        location = user.userdata.location
                        if location != voting.location:
                            for census in census_list:
                                census.delete()
                            return render(request, 'age_error.html', locals())
                        if edad < voting.min_age or edad > voting.max_age:
                            for census in census_list:
                                census.delete()
                            return render(request, 'age_error.html', locals())
                    adscripcion = ids[1]
                    if adscripcion == '': adscripcion=None
                    dat = ids[2]
                    objDate = datetime.strptime(dat, '%Y-%m-%d')
                    census = Census(voting_id=voting_id, voter_id=voter_id, adscripcion=adscripcion, date=objDate)
                    census_list.append(census)
                    census.save()

admin.site.register(Census, CensusAdmin)
admin.site.register(UserData)
