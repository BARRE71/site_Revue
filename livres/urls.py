from django.urls import path
from . import views

app_name = 'livres'

urlpatterns = [
    # Catalogue des revues
    path('', views.revue_list, name='revue_list'),
    path('catalogue/', views.revue_list, name='catalogue'),
    
    # Détail d'une revue
    path('revue/<slug:slug>/', views.revue_detail, name='revue_detail'),
    path('revue/<slug:slug>/telecharger-pdf/', views.download_revue_pdf, name='download_revue_pdf'),
    
    # Détail d'un auteur
    path('auteur/<slug:slug>/', views.author_detail, name='author_detail'),
    
    # Revues par catégorie
    path('categorie/<slug:category_slug>/', views.category_revues, name='category_revues'),
    
    # Recherche
    path('recherche/', views.search_revues, name='search_revues'),
    
    # Panier (nécessite une connexion)
    path('panier/', views.cart_detail, name='cart_detail'),
    path('panier/ajouter/<int:revue_id>/', views.add_to_cart, name='add_to_cart'),
    path('panier/modifier/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('panier/supprimer/<int:item_id>/', views.remove_cart_item, name='remove_cart_item'),
    path('cart/count/', views.cart_count, name='cart_count'),
    
    # Checkout et commandes
    path('checkout/', views.checkout, name='checkout'),
    path('commande/<int:order_id>/', views.order_detail, name='order_detail'),
    path('commandes/', views.order_list, name='order_list'),
]
