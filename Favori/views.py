from django.shortcuts import render,redirect
from .models import Favori
from django.shortcuts import get_object_or_404
from Voiture.models import Voiture
from django.core.paginator import Paginator
# Create your views here.
def ajout_Favorie(request, voiture_id):
    if not request.user.is_authenticated:
        return redirect('client:client_login')

    voiture = get_object_or_404(Voiture, id=voiture_id)

    favori, created = Favori.objects.get_or_create(
        user=request.user,
        voiture=voiture
    )

    if not created:
        favori.delete()
    return redirect(request.META.get('HTTP_REFERER', '/'))

def listeVoitureFavori(request):
    user=request.user
    if not user.is_authenticated:
        return redirect('client:client_login')
    favoris=Favori.objects.filter(user=user)
    liste_voitures = Voiture.objects.filter(favoris__in=favoris).select_related('modele', 'modele__marque').distinct()
    paginator = Paginator(liste_voitures, 1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        "nb_voitures":liste_voitures.count()
    }
    return render(request,"Voiture/voitures_favoris.html",context)
def defavori(request, voiture_id):
    if not request.user.is_authenticated:
        return redirect('client:client_login')
    
    voiture = get_object_or_404(Voiture, id=voiture_id)

    Favori.objects.filter(user=request.user, voiture=voiture).delete()

    return redirect('favori:voiture_favoris')

        



    