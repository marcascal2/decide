from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.CensusCreate.as_view(), name='census_create'),
    path('<int:voting_id>/', views.CensusDetail.as_view(), name='census_detail'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('admin/', views.all_census, name='admin_census_panel'),
    path('all_census/',views.all_census, name='all_census'),
    path('group_by_voting/<int:voting_id>',views.group_by_voting, name='group_by_voting'),
    path('group_by_voter/<int:voter_id>',views.group_by_voter, name='group_by_voter'),
    path('group_by_date/<str:date>',views.group_by_date, name='group_by_date'),
    path('group_by_adscripcion/<str:adscripcion>',views.group_by_adscripcion, name='group_by_adscripcion'),
    path('group_by_question/<str:question>',views.group_by_question, name='group_by_question'),
    path('all_census/search/',views.filter_by, name='filter_by'),
    path('import_by_voting/', views.import_by_voting, name="import_by_voting"),
    path('export_by_voting/<int:voting_id>', views.export_by_voting, name="export_by_voting"),
    #TODO: quitar
    path('panel/', views.render_panel_administracion, name='census_panel'),
    path('panel/<int:voting_id>', views.voting_census, name="voting_census")
]
