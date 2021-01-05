from django.contrib import admin
from django.http import HttpResponse
import csv
from django import forms
from django.shortcuts import render
from django.urls import path

from .models import Census
from .views import *


class CensusAdmin(admin.ModelAdmin):
    change_list_template = "import.html"
    list_display = ('voting_id', 'voter_id')
    list_filter = ('voting_id', 'voter_id')

    search_fields = ('voter_id', )

    actions = ['export_as_csv']

    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)
        writer.writerow(field_names)

        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])
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

        def save_import(f):
            for row in f:
                if not row.startswith(b'id'):
                    cadena = row.decode('utf-8')
                    ids = cadena.split(',')
                    voting_id = ids[1]
                    voter_id = ids[2]
                    census = Census(voting_id=voting_id, voter_id=voter_id)
                    census.save()
            f.close()

        form = UploadDocumentForm()
        if request.method == 'POST':
            form = UploadDocumentForm(request.POST, request.FILES)
            if form.is_valid():
                save_import(request.FILES['file'])
                return render(request, 'succes.html', locals())
        else:
            form = UploadDocumentForm()

        return render(request, 'upload.html', {'form': form})

admin.site.register(Census, CensusAdmin)
