from django.urls import path
from . import views
app_name="location"
urlpatterns = [
    path('<int:id_voiture>/',views.louer_voiture,name="louer_voiture"),
    path('mes-locations/', views.mes_locations, name='mes_locations'),
]