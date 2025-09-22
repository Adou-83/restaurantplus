from django.db import models
from django.contrib.auth.models import User
from PIL import Image
import os



# --- Helper pour créer thumbnails ---
def create_thumbnail(image_field, size=(200, 200)):
    if not image_field:
        return
    img = Image.open(image_field.path)
    img.thumbnail(size)
    thumb_path = image_field.path.replace('.', '_thumb.')
    img.save(thumb_path)
    return thumb_path





STATUT_CHOICES = [
    ('en_attente', 'En attente'),
    ('en_preparation', 'En préparation'),
    ('livree', 'Livrée'),
    ('annulee', 'Annulée'),
]

class Commande(models.Model):
    client = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    nom_client = models.CharField(max_length=100)
    adresse = models.CharField(max_length=255, default='')
    telephone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    produit = models.CharField(max_length=255)
    quantite = models.PositiveIntegerField(default=1)
    date_commande = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')

    def __str__(self):
        return f"Commande {self.id} - {self.nom_client} ({self.statut})"

class Plat(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField()
    prix = models.PositiveIntegerField()
    stock = models.PositiveIntegerField(default=100)  # Ajouter stock pour gestion
    image = models.ImageField(upload_to='plats/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='plats/thumbnails/', blank=True, null=True)
    vin_recommande = models.CharField(max_length=100, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            # Redimensionner image principale
            img = Image.open(self.image.path)
            if img.height > 800 or img.width > 800:
                img.thumbnail((800, 800))
                img.save(self.image.path)
            # Créer thumbnail
            thumb_path = create_thumbnail(self.image, (200, 200))
            if thumb_path:
                self.thumbnail.name = os.path.join('plats/thumbnails/', os.path.basename(thumb_path))
                super().save(update_fields=['thumbnail'])

    def __str__(self):
        return self.nom

class ProduitMarche(models.Model):
    nom = models.CharField(max_length=100)
    prix = models.PositiveIntegerField()
    stock = models.PositiveIntegerField(default=100)
    image = models.ImageField(upload_to='marche/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='marche/thumbnails/', blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            img = Image.open(self.image.path)
            if img.height > 800 or img.width > 800:
                img.thumbnail((800, 800))
                img.save(self.image.path)
            thumb_path = create_thumbnail(self.image, (200, 200))
            if thumb_path:
                self.thumbnail.name = os.path.join('marche/thumbnails/', os.path.basename(thumb_path))
                super().save(update_fields=['thumbnail'])

    def __str__(self):
        return self.nom

 
 

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
    
class Cuisinier(models.Model):
    nom = models.CharField(max_length=100)
    bio = models.TextField()
    prix = models.PositiveIntegerField()
    stock = models.PositiveIntegerField(default=1)
    image = models.ImageField(upload_to='cuisiniers/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='cuisiniers/thumbnails/', blank=True, null=True)
    disponible = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            img = Image.open(self.image.path)
            if img.height > 800 or img.width > 800:
                img.thumbnail((800, 800))
                img.save(self.image.path)
            thumb_path = create_thumbnail(self.image, (200, 200))
            if thumb_path:
                self.thumbnail.name = os.path.join('cuisiniers/thumbnails/', os.path.basename(thumb_path))
                super().save(update_fields=['thumbnail'])

    def __str__(self):
        return self.nom



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
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='vins/', blank=True, null=True)  # Optionnel

    def __str__(self):
        return self.nom
    

class Vin(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    prix = models.PositiveIntegerField()
    stock = models.PositiveIntegerField(default=100)
    image = models.ImageField(upload_to='vins/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='vins/thumbnails/', blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            img = Image.open(self.image.path)
            if img.height > 800 or img.width > 800:
                img.thumbnail((800, 800))
                img.save(self.image.path)
            thumb_path = create_thumbnail(self.image, (200, 200))
            if thumb_path:
                self.thumbnail.name = os.path.join('vins/thumbnails/', os.path.basename(thumb_path))
                super().save(update_fields=['thumbnail'])

    def __str__(self):
        return self.nom

 
class Publicite(models.Model):
    titre = models.CharField(max_length=200)
    image = models.ImageField(upload_to='publicites/', blank=True, null=True)  # Optionnel
    lien = models.URLField(blank=True, null=True)
    actif = models.BooleanField(default=True)

    def __str__(self):
        return self.titre
