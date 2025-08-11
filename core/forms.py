 # core/forms.py

from django import forms
from .models import Commande

class CommandeForm(forms.ModelForm):
    class Meta:
        model = Commande
        fields = ['nom_client', 'adresse', 'telephone', 'email', 'produit', 'quantite']
