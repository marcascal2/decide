from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.CensusCreate.as_view(), name='census_create'),
    path('<int:voting_id>/', views.CensusDetail.as_view(), name='census_detail'),
    path('import_by_voting/<int:voting_id>', views.import_by_voting, name="import_by_voting"),
    path('export_by_voting/<int:voting_id>', views.export_by_voting, name="export_by_voting"),
]
