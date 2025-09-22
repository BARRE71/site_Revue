from django.urls import path
from . import views

app_name = 'subscriptions'

urlpatterns = [
    # Plans d'abonnement
    path('', views.plan_list, name='plan_list'),
    
    # Abonnement
    path('souscrire/<int:plan_id>/', views.subscribe, name='subscribe'),
    
    # Gestion de l'abonnement
    path('mon-abonnement/', views.my_subscription, name='my_subscription'),
    path('annuler/<int:subscription_id>/', views.cancel_subscription, name='cancel_subscription'),
    path('historique/', views.subscription_history, name='subscription_history'),
    
    # Newsletter
    path('newsletter/desabonner/<int:subscription_id>/', views.newsletter_unsubscribe, name='newsletter_unsubscribe'),
]
