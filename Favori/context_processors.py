from .models import Favori
from Voiture.models import Voiture

def nb_voitures_favoris(request):
    nb = 0
    if request.user.is_authenticated:
        favoris = Favori.objects.filter(user=request.user)
        nb = Voiture.objects.filter(favoris__in=favoris).distinct().count()
    return {'nb_favoris': nb}