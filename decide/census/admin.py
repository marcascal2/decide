from django.contrib import admin
from django.http import HttpResponse
import csv
from django import forms
from django.shortcuts import render

from .models import Census

import logging


class CensusAdmin(admin.ModelAdmin):
    list_display = ('voting_id', 'voter_id')
    list_filter = ('voting_id', )

    search_fields = ('voter_id', )

    actions = ['export_as_csv','import_from_csv']

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

    def import_from_csv(self, request, queryset):
        class UploadDocumentForm(forms.Form):
            file = forms.FileField()

        def save_import(f):
            reader = csv.DictReader(open(f))
            for row in reader:
                voting_id = row['voting_id']
                voter_id = row['voter_id']
                census = Census(voting_id=voting_id, voter_id=voter_id)
                census.save()
            f.close()

        logger = logging.getLogger("mylogger")
        form = UploadDocumentForm()
        if request.method == 'POST':
            form = UploadDocumentForm(request.POST, request.FILES)
            logger.info(form.is_valid())
            logger.info(form.errors)
            logger.info(request.FILES)
            logger.info(request.POST)
            if form.is_valid():
                save_import(request.FILES['file'])
        else:
            form = UploadAttemptForm()

        return render(request, 'upload_doc.html', {'form': form})

    export_as_csv.short_description = 'Export as CSV'
    import_from_csv.short_description = 'Import from CSV'

admin.site.register(Census, CensusAdmin)
