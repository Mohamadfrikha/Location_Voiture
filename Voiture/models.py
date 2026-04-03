from django.db import models


class Carburant(models.TextChoices):
    ESSENCE = "essence", "Essence"
    DIESEL = "diesel", "Diesel"
    ELECTRIQUE = "electrique", "Electrique"
    HYBRIDE = "hybride", "Hybride"
class Boite(models.TextChoices):
    MANUELLE = "manuelle", "Manuelle"
    AUTOMATIQUE = "automatique", "Automatique"
class Marque(models.Model):
    nom = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='marques/')

    def __str__(self):
        return self.nom
class Modele(models.Model):
    nom = models.CharField(max_length=100)
    marque = models.ForeignKey(Marque, on_delete=models.CASCADE, related_name="modeles")

    annee = models.PositiveIntegerField()
    carburant = models.CharField(
        max_length=20,
        choices=Carburant.choices,
        default=Carburant.ESSENCE
    ) # Essence / Diesel / Hybride / Electrique
    boite = models.CharField(
        max_length=20,
        choices=Boite.choices, 
        default=Boite.MANUELLE
    )     

    def __str__(self):
        return f"{self.marque.nom} {self.nom} {self.annee}"
class Voiture(models.Model):
    modele = models.ForeignKey(Modele, on_delete=models.CASCADE,related_name="voitures")
    couleur = models.CharField(max_length=20)
    prix_par_jour = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='voitures/')
    kilometrage = models.IntegerField(help_text="Kilométrage en km",default=0)
    location_disponible = models.BooleanField(default=True)
    date_ajout = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.modele} ({self.couleur})"
class ImageVoiture(models.Model):
    voiture = models.ForeignKey(
        Voiture,
        on_delete=models.CASCADE,
        related_name="images"
    )
    image = models.ImageField(upload_to="voitures/")

    def __str__(self):
        return f"Image de {self.voiture}"