from django.urls import path
from . import views
app_name = "favori"
urlpatterns = [ 
    path("<int:voiture_id>/",views.ajout_Favorie,name="ajout_favorie"),
    path("voiture/",views.listeVoitureFavori,name="voiture_favoris"),
    path("defavori/<int:voiture_id>/", views.defavori, name="defavori")
]
