from django.urls import path
from . import views


print("Attributs dans views:", dir(views))  # <-- ajoute cette ligne ici


urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('recherche/', views.recherche, name='recherche'),

    path('vins/', views.liste_vins, name='liste_vins'), 
    path('cuisiniers/', views.liste_cuisiniers, name='liste_cuisiniers'),
    path('commander/', views.passer_commande, name='passer_commande'),
    path('commande/confirmation/', views.confirmation_commande, name='confirmation_commande'),
    path('mes-commandes/', views.mes_commandes, name='mes_commandes'), 
    path('panier/ajouter/<str:produit_type>/<int:produit_id>/', views.ajouter_au_panier, name='ajouter_au_panier'),
    path('panier/', views.voir_panier, name='voir_panier'),
    path('panier/vider/', views.vider_panier, name='vider_panier'),
    path('plats/', views.liste_plats, name='liste_plats'),
    path('marche/', views.liste_produits_marche, name='liste_produits_marche'),
     path('inscription/', views.inscription, name='inscription'),
     path('logout/', views.deconnexion, name='logout'),

]

