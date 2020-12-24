from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin

from .models import Census


class CensusAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = ('voting_id', 'voter_id')
    list_filter = ('voting_id', )

    search_fields = ('voter_id', )


admin.site.register(Census, CensusAdmin)
