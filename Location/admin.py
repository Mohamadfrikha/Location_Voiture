from django.contrib import admin
from .models import Location
# Register your models here.
from .utils import accepter_location_admin  # import

@admin.action(description="Accepter la location et notifier le client")
def accepter_location(modeladmin, request, queryset):
    for loc in queryset:
        accepter_location_admin(loc.id)
@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['client_nom','Voiture','date_debut','date_fin']
    search_fields = ['client__nom']
    actions = [accepter_location] 
    def client_nom(self, obj):
        return f'{obj.client}'
    def Voiture(self,obj):
        return f'{obj.voiture}'
    client_nom.short_description = "Nom du client"
    Voiture.short_description = "Voiture"