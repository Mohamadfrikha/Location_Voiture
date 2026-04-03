from django.contrib import admin

from Voiture.models import Modele, Voiture,Marque,ImageVoiture

# Register your models here.
@admin.register(Marque)
class MarqueAdmin(admin.ModelAdmin):
    list_display = ['nom']
    list_filter = ['nom']
@admin.register(Modele)
class ModeleAdmin(admin.ModelAdmin):
    list_display = ['nom','marque','annee','carburant','boite']
    list_filter = ['marque','annee','carburant','boite']

@admin.register(Voiture)
class VoitureAdmin(admin.ModelAdmin):
    list_display = ['marque__nom','modele__nom', 'location_disponible']
    list_filter = [  'location_disponible']
    search_fields = ['marque__nom', 'modele__nom']
    date_hierarchy = 'date_ajout'
    readonly_fields = ['date_ajout']
    def marque__nom(self, obj):
        return obj.modele.marque.nom
    marque__nom.short_description = 'Marque'
    def modele__nom(self, obj):
        return obj.modele.nom
    modele__nom.short_description = 'Modèle'
admin.site.register(ImageVoiture)