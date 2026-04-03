from django.db import models
from Voiture.models import Voiture
from Client.models import Client
from datetime import datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _ 
from django.utils import timezone
from decimal import Decimal, ROUND_HALF_UP
# Create your models here.
class Decision(models.TextChoices):
        EN_ATTENTE = 'EN', _('En attente')
        ACCEPTEE = 'AC', _('Acceptée')
        REFUSEE = 'RF', _('Refusée')
class Location(models.Model):
    voiture = models.ForeignKey(Voiture, on_delete=models.CASCADE,related_name="locations")
    client =models.ForeignKey(Client, on_delete=models.CASCADE,related_name="locations")  # ou User si tu veux authentification
    date_debut = models.DateField()
    date_fin = models.DateField()
    decision = models.CharField(
        max_length=2,
        choices=Decision.choices,
        default=Decision.EN_ATTENTE
    )
    
    cause_rejet = models.TextField(
        blank=True,  # peut être vide si pas refusé
        null=True,
        help_text="Raison du refus si la location est refusée par l'admin"
    )
    
    pourcentage_partiel = models.DecimalField(
        max_digits=5, decimal_places=2, default=30.0,
        help_text="Pourcentage du paiement partiel (par défaut 30%)"
    )
    
    montant_total = models.DecimalField(max_digits=10, decimal_places=2)
    montant_partiel = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    paiement_partiel_effectue = models.BooleanField(default=False)
    paiement_total_effectue = models.BooleanField(default=False)
    
    delai_paiement = models.DateTimeField(null=True, blank=True)
    
    est_active = models.BooleanField(default=False)
    est_terminer=models.BooleanField(default=False)
    
    date_creation=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.client} - {self.voiture} ({self.date_debut} → {self.date_fin})"
    @property
    def reste_a_payer(self):
        """Retourne le montant restant à payer"""
        return max(self.montant_total - self.montant_paye, 0)
    @property
    def montant_paye(self):
        if self.paiement_total_effectue:
            return self.montant_total
        elif self.paiement_partiel_effectue:
            return self.montant_partiel
        return 0
    @property
    def montant_a_payer_usd(self):
        """
        Retourne le montant restant à payer en USD.
        - Si le paiement partiel n'a pas été effectué → retourne le montant partiel.
        - Si le paiement partiel est fait mais pas le paiement total → retourne le reste à payer.
        - Si tout est payé → retourne 0.
        """
        TND_TO_USD = Decimal('0.32')  # exemple : 1 TND ≈ 0.32 USD, ajuste selon le taux réel
        if not self.paiement_partiel_effectue:
            montant = self.montant_partiel
        elif self.paiement_partiel_effectue and not self.paiement_total_effectue:
            montant = self.reste_a_payer
        else:
            montant = 0

        return (montant * TND_TO_USD).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    def clean(self):
        # Validation pour ne pas avoir actif et terminé en même temps
        if self.est_active and self.est_terminer:
            raise ValidationError("Une location ne peut pas être active et terminée en même temps.")
    def save(self, *args, **kwargs):
        nb_jours = max((self.date_fin - self.date_debut).days + 1, 1)
        self.montant_total = (self.voiture.prix_par_jour * nb_jours).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        self.montant_partiel = (
            self.montant_total * (Decimal(self.pourcentage_partiel) / Decimal('100'))
        ).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        if self.decision == Decision.ACCEPTEE and not self.delai_paiement:
            self.delai_paiement = datetime.now() + timedelta(days=2)  # délai de paiement 2 jours
        if self.decision != Decision.REFUSEE:
            self.cause_rejet = None
        super().save(*args, **kwargs)
