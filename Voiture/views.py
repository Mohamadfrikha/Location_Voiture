from pyexpat import model
from django.db.models import Count,Exists, OuterRef
from django.core import paginator
from django.shortcuts import render
from Location.models import Location,Decision
from .models import ImageVoiture, Marque, Modele, Voiture
from django.core.paginator import Paginator
from Favori.models import Favori
from datetime import date
# Create your views here.
def ListeVoitures(request):
    voitures_list = Voiture.objects.select_related('modele', 'modele__marque').filter(location_disponible=True).annotate(nb_favoris=Count('favoris'))
    if request.user.is_authenticated:
        favoris_subquery = Favori.objects.filter(
            user=request.user,
            voiture=OuterRef('pk')
        )
        voitures_list = voitures_list.annotate(
            favorie=Exists(favoris_subquery)  # True si user a liké
        )
    else:
        from django.db.models import Value, BooleanField
        voitures_list = voitures_list.annotate(favorie=Value(False, output_field=BooleanField()))
    sort_by = request.GET.get('marque')
    modele_id = request.GET.get('modele')
    paginator = Paginator(voitures_list, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    marques = Marque.objects.all()
    liste_marques = []
    for marque in marques:
        modele = Modele.objects.filter(marque=marque)
        voiture_count = sum(Voiture.objects.filter(modele=m, location_disponible=True).count() for m in modele)
        v={
            'marque': marque,
            'nb_voitures': voiture_count,
            
        }
        print(v)
        liste_marques.append(v)
    voitures_list = voitures_list.order_by('-id')
    context = {
        'page_obj': page_obj,
        'sort_by': request.GET.get('marque'),
        'liste_marques': liste_marques,
        'models': Modele.objects.filter(marque_id=sort_by).all() if sort_by else None  ,
        'modele_id':modele_id
    }
    return render(request, 'Voiture/accueil.html', context)

def DetailsVoiture(request, voiture_id):
    voiture = Voiture.objects.select_related('modele', 'modele__marque').get(id=voiture_id)
    images=ImageVoiture.objects.filter(voiture=voiture)
    locations_indesponibles = Location.objects.filter(voiture=voiture, est_active=True)
    peut_modifier = False
    peut_payer = False
    peut_demande = True
    if request.user.is_authenticated:
        location_qs = Location.objects.filter(
            voiture=voiture_id,
            client=request.user,
            est_terminer=False,   
        ).exclude(decision=Decision.REFUSEE)
        location = location_qs.first()  # prend le premier objet ou None
        print(location)
        if location:
            peut_demande = False 
            if location.est_active==False:
                peut_modifier = True
            if location.decision == Decision.ACCEPTEE and location.delai_paiement.date() >= date.today():
                peut_payer = True
    print("peut_modifier:", peut_modifier)
    print("peut_payer:", peut_payer)
    print("peut_demande:", peut_demande)
    context = {
        'voiture': voiture,
        'images': images,
        'locations_indesponibles': locations_indesponibles,
        'peut_modifier': peut_modifier,
        'peut_payer': peut_payer,
        'peut_demande':peut_demande,
        'loc':location
    }
    return render(request, 'Voiture/details.html', context)
def ListeVoituresParMarque(request):
    marque_id = request.GET.get('marque')
    modele_id = request.GET.get('modele')
    voitures_list = Voiture.objects.select_related('modele', 'modele__marque').all().annotate(nb_favoris=Count('favoris'))
    if request.user.is_authenticated:
        favoris_subquery = Favori.objects.filter(
            user=request.user,
            voiture=OuterRef('pk')
        )
        voitures_list = voitures_list.annotate(
            favorie=Exists(favoris_subquery)  # True si user a liké
        )
    else:
        from django.db.models import Value, BooleanField
        voitures_list = voitures_list.annotate(favorie=Value(False, output_field=BooleanField()))
    if marque_id:
        voitures_list = voitures_list.filter(modele__marque_id=marque_id)
        nb_resultats = voitures_list.count()
    if modele_id:
        voitures_list = voitures_list.filter(modele_id=modele_id)
        nb_resultats = voitures_list.count()
    nb_resultats = voitures_list.count()
    paginator = Paginator(voitures_list, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'marque_id': marque_id,
        'modele_id': modele_id,
        'nb_resultats': nb_resultats,
        'liste_marques': Marque.objects.all(),
        'liste_modeles': Modele.objects.filter(marque_id=marque_id).all() if marque_id else None
        
    }
    return render(request, 'Voiture/voitures.html', context)