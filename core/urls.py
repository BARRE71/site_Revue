from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('search/', views.search, name='search'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('newsletter/subscribe/', views.newsletter_subscribe, name='newsletter_subscribe'),
    path('newsletter/unsubscribe/', views.newsletter_unsubscribe, name='newsletter_unsubscribe'),
    path('newsletter/subscribers/', views.newsletter_subscribers, name='newsletter_subscribers'),
    path('sitemap/', views.sitemap, name='sitemap'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
]
