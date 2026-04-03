from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from . import views
app_name = 'voiture'
urlpatterns = [
    path('',views.ListeVoitures,name='accueil'),
    path('/<int:voiture_id>/',views.DetailsVoiture,name='details_voiture'),
    path('/voitures/',views.ListeVoituresParMarque,name='voitures'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
