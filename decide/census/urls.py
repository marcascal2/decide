from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.CensusCreate.as_view(), name='census_create'),
    path('<int:voting_id>/', views.CensusDetail.as_view(), name='census_detail'),
    path('panel/', views.render_panel_administracion, name='census_panel'),
    path('panel/<int:voting_id>', views.voting_census, name="voting_census")
]
