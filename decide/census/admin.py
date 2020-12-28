from django.contrib import admin

from .models import Census


class CensusAdmin(admin.ModelAdmin):
    list_display = ('voting_id', 'voter_id','adscripcion','date')
    list_filter = ('voting_id', 'adscripcion','date')

    search_fields = ('voter_id', 'adscripcion')


admin.site.register(Census, CensusAdmin)
