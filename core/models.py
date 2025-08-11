from django.db import models
from django.contrib.auth.models import User

class Plat(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField()
    prix = models.PositiveIntegerField()
    image = models.ImageField(upload_to='plats/', blank=True, null=True)  # Optionnel
    vin_recommande = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.nom

class ProduitMarche(models.Model):
    nom = models.CharField(max_length=100)
    prix = models.PositiveIntegerField()
    image = models.ImageField(upload_to='marche/', blank=True, null=True)  # Optionnel

    def __str__(self):
        return self.nom

class Cuisinier(models.Model):
    nom = models.CharField(max_length=100)
    bio = models.TextField()
    prix = models.PositiveIntegerField()
    image = models.ImageField(upload_to='cuisiniers/', blank=True, null=True)  # Optionnel
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return self.nom

class Commande(models.Model):
    nom_client = models.CharField(max_length=100)
    adresse = models.CharField(max_length=255, default='')
    telephone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    produit = models.CharField(max_length=255)
    quantite = models.PositiveIntegerField(default=1)
    date_commande = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Commande de {self.nom_client} - {self.produit}"
    

class LigneCommande(models.Model):
    commande = models.ForeignKey('Commande', on_delete=models.CASCADE, related_name='lignes')
    produit_type = models.CharField(max_length=50)  # 'plat', 'marche', 'vin'
    produit_id = models.PositiveIntegerField()
    nom_produit = models.CharField(max_length=100)
    prix_unitaire = models.PositiveIntegerField()
    quantite = models.PositiveIntegerField(default=1)

    def get_total(self):
        return self.prix_unitaire * self.quantite

    def __str__(self):
        return f"{self.nom_produit} x{self.quantite} ({self.produit_type})"


class ReservationCuisinier(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    cuisinier = models.ForeignKey(Cuisinier, on_delete=models.CASCADE)
    date = models.DateField()
    heure = models.TimeField()
    lieu = models.CharField(max_length=255)

    def __str__(self):
        return f"Réservation {self.cuisinier.nom} par {self.client.username} le {self.date}"

class Vin(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    prix = models.PositiveIntegerField()
    image = models.ImageField(upload_to='vins/', blank=True, null=True)  # Optionnel

    def __str__(self):
        return self.nom

class Publicite(models.Model):
    titre = models.CharField(max_length=200)
    image = models.ImageField(upload_to='publicites/', blank=True, null=True)  # Optionnel
    lien = models.URLField(blank=True, null=True)
    actif = models.BooleanField(default=True)

    def __str__(self):
        return self.titre
