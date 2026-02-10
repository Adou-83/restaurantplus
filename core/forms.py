 # core/forms.py

from django import forms
from .models import Commande
from django.contrib.auth.models import User

class CommandeForm(forms.ModelForm):
    class Meta:
        model = Commande
        fields = ['nom_client', 'adresse', 'telephone', 'email']

    def clean_nom_client(self):
        nom = self.cleaned_data['nom_client']
        if not nom.strip():
            raise forms.ValidationError("Le nom du client est obligatoire.")
        return nom

    def clean_telephone(self):
        tel = self.cleaned_data['telephone']
        if not tel.isdigit():
            raise forms.ValidationError("Le téléphone doit contenir uniquement des chiffres.")
        return tel

# ---------------------------------
# Formulaire pour le profil utilisateur
# ---------------------------------
class ProfilForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
