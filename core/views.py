from django.shortcuts import render, redirect
from .models import Plat, ProduitMarche, Cuisinier, Commande, Vin, Publicite
from .forms import CommandeForm
from django.shortcuts import get_object_or_404
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm


print("core/views.py chargé") 



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



def liste_vins(request):
    vins = Vin.objects.all()
    return render(request, 'core/liste_vins.html', {'vins': vins})

def liste_cuisiniers(request):
    cuisiniers = Cuisinier.objects.filter(disponible=True)
    return render(request, 'core/liste_cuisiniers.html', {'cuisiniers': cuisiniers})

 
from .models import LigneCommande

def passer_commande(request):
    panier = request.session.get('panier', {})
    if not panier:
        return redirect('accueil')  # panier vide, pas de commande possible

    if request.method == 'POST':
        form = CommandeForm(request.POST)
        if form.is_valid():
            commande = form.save()

            # Création des lignes de commande à partir du panier
            for cle, item in panier.items():
                produit_type, produit_id = cle.split('_')
                LigneCommande.objects.create(
                    commande=commande,
                    produit_type=produit_type,
                    produit_id=int(produit_id),
                    nom_produit=item['nom'],
                    prix_unitaire=int(item['prix']),
                    quantite=item['quantite']
                )

            # Vider panier après validation
            request.session['panier'] = {}

            return redirect('confirmation_commande')
    else:
        form = CommandeForm()

    return render(request, 'core/passer_commande.html', {'form': form, 'panier': panier})




def confirmation_commande(request):
    return render(request, 'core/confirmation_commande.html')




def ajouter_au_panier(request, produit_type, produit_id):
    if produit_type not in ['plat', 'marche', 'vin']:
        return redirect('accueil')

    if produit_type == 'plat':
        produit = get_object_or_404(Plat, id=produit_id)
    elif produit_type == 'marche':
        produit = get_object_or_404(ProduitMarche, id=produit_id)
    else:  # vin
        produit = get_object_or_404(Vin, id=produit_id)

    panier = request.session.get('panier', {})
    cle = f"{produit_type}_{produit_id}"

    if cle in panier:
        panier[cle]['quantite'] += 1
    else:
        panier[cle] = {
            'nom': produit.nom,
            'prix': float(produit.prix),
            'quantite': 1
        }

    request.session['panier'] = panier
    return redirect('voir_panier')

def voir_panier(request):
    panier = request.session.get('panier', {})
    total = 0
    # Calculer total général et total ligne
    for cle, item in panier.items():
        item['total_ligne'] = item['prix'] * item['quantite']
        total += item['total_ligne']
    return render(request, 'core/panier.html', {'panier': panier, 'total': total})


def vider_panier(request):
    if 'panier' in request.session:
        del request.session['panier']
    return redirect('voir_panier')


def liste_plats(request):
    plats = Plat.objects.all()
    print(f"Plats en base : {plats}")
    return render(request, 'core/liste_plats.html', {'plats': plats})




def liste_produits_marche(request):
    produits = ProduitMarche.objects.all()
    return render(request, 'core/liste_produits_marche.html', {'produits': produits})



def inscription(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accueil')  # Redirige vers l'accueil
    else:
        form = UserCreationForm()
    return render(request, 'registration/inscription.html', {'form': form})

 

def deconnexion(request):
    logout(request)
    return redirect('login')
