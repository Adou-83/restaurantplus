from django.shortcuts import render, redirect, get_object_or_404
from .models import Plat, ProduitMarche, Cuisinier, Commande, Vin, Publicite, LigneCommande
from .forms import CommandeForm
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.db.models import Q
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import ProfilForm

print("core/views.py chargé") 

# -------------------- Accueil --------------------
def accueil(request):
    plats = Plat.objects.all()
    produits_marche = ProduitMarche.objects.all()
    vins = Vin.objects.all()
    cuisiniers = Cuisinier.objects.filter(disponible=True)
    publicites = Publicite.objects.filter(actif=True)

    context = {
        'plats': plats,
        'produits_marche': produits_marche,
        'vins': vins,
        'cuisiniers': cuisiniers,
        'publicites': publicites,
    }
    return render(request, 'core/accueil.html', context)

def recherche(request):
    query = request.GET.get('q', '').strip()  # récupérer la recherche
    plats = vins = produits = []

    if query:
        plats = Plat.objects.filter(nom__icontains=query)
        vins = Vin.objects.filter(nom__icontains=query)
        produits = ProduitMarche.objects.filter(nom__icontains=query)

    context = {
        'query': query,
        'plats': plats,
        'vins': vins,
        'produits': produits,
    }
    return render(request, 'core/recherche.html', context)
# -------------------- Listes --------------------
def liste_plats(request):
    plats = Plat.objects.all()
    return render(request, 'core/liste_plats.html', {'plats': plats})

def liste_vins(request):
    vins = Vin.objects.all()
    return render(request, 'core/liste_vins.html', {'vins': vins})

def liste_produits_marche(request):
    produits = ProduitMarche.objects.all()
    return render(request, 'core/liste_produits_marche.html', {'produits': produits})

def liste_cuisiniers(request):
    cuisiniers = Cuisinier.objects.filter(disponible=True)
    return render(request, 'core/liste_cuisiniers.html', {'cuisiniers': cuisiniers})

# -------------------- Panier --------------------
def ajouter_au_panier(request, produit_type, produit_id):
    if produit_type not in ['plat', 'marche', 'vin']:
        return redirect('accueil')

    if produit_type == 'plat':
        produit = get_object_or_404(Plat, id=produit_id)
    elif produit_type == 'marche':
        produit = get_object_or_404(ProduitMarche, id=produit_id)
    else:
        produit = get_object_or_404(Vin, id=produit_id)

    if produit.stock <= 0:
        messages.error(request, f"Le produit {produit.nom} est épuisé.")
        return redirect('accueil')

    panier = request.session.get('panier', {})
    cle = f"{produit_type}_{produit_id}"

    if cle in panier:
        if panier[cle]['quantite'] + 1 > produit.stock:
            messages.error(request, f"Quantité maximale pour {produit.nom} atteinte ({produit.stock}).")
        else:
            panier[cle]['quantite'] += 1
    else:
        panier[cle] = {'nom': produit.nom, 'prix': float(produit.prix), 'quantite': 1}

    request.session['panier'] = panier
    messages.success(request, f"{produit.nom} ajouté au panier.")
    return redirect('voir_panier')


def voir_panier(request):
    panier = request.session.get('panier', {})
    total = sum(item['prix'] * item['quantite'] for item in panier.values())
    return render(request, 'core/panier.html', {'panier': panier, 'total': total})

def vider_panier(request):
    if 'panier' in request.session:
        del request.session['panier']
    messages.success(request, "Panier vidé avec succès.")
    return redirect('voir_panier')

# -------------------- Commandes --------------------
def passer_commande(request):
    panier = request.session.get('panier', {})
    if not panier:
        messages.error(request, "Votre panier est vide.")
        return redirect('accueil')

    if request.method == 'POST':
        form = CommandeForm(request.POST)
        if form.is_valid():
            commande = form.save(commit=False)
            if request.user.is_authenticated:
                commande.client = request.user

            produits_list = [f"{item['nom']} x{item['quantite']}" for item in panier.values()]
            commande.produit = ', '.join(produits_list)
            commande.quantite = sum(item['quantite'] for item in panier.values())
            commande.save()

            for cle, item in panier.items():
                produit_type, produit_id = cle.split('_')
                if produit_type == 'plat':
                    produit = Plat.objects.get(id=produit_id)
                elif produit_type == 'marche':
                    produit = ProduitMarche.objects.get(id=produit_id)
                else:
                    produit = Vin.objects.get(id=produit_id)

                LigneCommande.objects.create(
                    commande=commande,
                    produit_type=produit_type,
                    produit_id=int(produit_id),
                    nom_produit=item['nom'],
                    prix_unitaire=int(item['prix']),
                    quantite=item['quantite']
                )
                produit.stock -= item['quantite']
                produit.save()

            request.session['panier'] = {}
            messages.success(request, "Commande passée avec succès !")
            return redirect('confirmation_commande')
    else:
        form = CommandeForm()

    return render(request, 'core/passer_commande.html', {'form': form, 'panier': panier})

def confirmation_commande(request):
    return render(request, 'core/confirmation_commande.html')

def mes_commandes(request):
    commandes = None
    if request.user.is_authenticated:
        commandes = Commande.objects.filter(client=request.user).order_by('-date_commande')
    else:
        email = request.GET.get('email')
        if email:
            commandes = Commande.objects.filter(email=email).order_by('-date_commande')
    return render(request, 'core/mes_commandes.html', {'commandes': commandes})

# -------------------- Auth --------------------

def inscription(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # création de l'utilisateur
            login(request, user)  # connexion automatique
            messages.success(request, "Bienvenue ! Votre compte a été créé avec succès ✅")
            return redirect('/')  # redirection vers la page d'accueil
    else:
        form = UserCreationForm()
    return render(request, 'registration/inscription.html', {'form': form})
def deconnexion(request):
    logout(request)
    return redirect('login')

# -------------------- Email --------------------
def envoyer_email_confirmation(commande):
    if not commande.email:
        return
    sujet = f"Confirmation de votre commande #{commande.id}"
    html_message = render_to_string('core/email_confirmation.html', {'commande': commande})
    message = strip_tags(html_message)
    send_mail(sujet, message, None, [commande.email], html_message=html_message)


    

@login_required
def profil(request):
    commandes = Commande.objects.filter(client=request.user).order_by('-date_commande')
    
    if request.method == 'POST':
        form = ProfilForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Profil mis à jour avec succès.")
            return redirect('profil')
    else:
        form = ProfilForm(instance=request.user)

    return render(request, 'registration/profil.html', {
        'form': form,
        'commandes': commandes
    })
