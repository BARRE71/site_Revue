#!/usr/bin/env python
"""
Script simplifié pour créer des données initiales pour RevueMaroc
"""
import os
import sys
import django
from django.utils import timezone
from datetime import timedelta

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'revue_maroc.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import Category, Tag, SiteSettings


def create_site_settings():
    """Créer les paramètres du site"""
    if not SiteSettings.objects.exists():
        settings = SiteSettings.objects.create(
            site_name="RevueMaroc",
            site_description="Votre source d'information privilégiée sur le développement du Maroc",
            contact_email="contact@revuemaroc.com",
            contact_phone="+212 5 22 123 456",
            address="123 Avenue Mohammed V, Casablanca, Maroc",
            facebook_url="https://facebook.com/revuemaroc",
            twitter_url="https://twitter.com/revuemaroc",
            linkedin_url="https://linkedin.com/company/revuemaroc",
            instagram_url="https://instagram.com/revuemaroc",
            monthly_price=9.99,
            yearly_price=99.99,
            shipping_cost=5.99,
            free_shipping_threshold=50.00
        )
        print(f"Paramètres du site créés: {settings.site_name}")
    else:
        print("Paramètres du site existent déjà")


def create_categories():
    """Créer les catégories principales"""
    categories_data = [
        {
            'name': 'Politique',
            'slug': 'politique',
            'description': 'Actualités politiques et analyses des décisions gouvernementales',
            'order': 1
        },
        {
            'name': 'Économie',
            'slug': 'economie',
            'description': 'Développement économique, investissements et projets d\'infrastructure',
            'order': 2
        },
        {
            'name': 'Société',
            'slug': 'societe',
            'description': 'Évolutions sociales, éducation, santé et bien-être',
            'order': 3
        },
        {
            'name': 'Culture',
            'slug': 'culture',
            'description': 'Patrimoine culturel, arts, traditions et événements',
            'order': 4
        },
        {
            'name': 'Technologie',
            'slug': 'technologie',
            'description': 'Innovation technologique, digitalisation et transformation numérique',
            'order': 5
        },
        {
            'name': 'Environnement',
            'slug': 'environnement',
            'description': 'Développement durable, énergies renouvelables et protection écologique',
            'order': 6
        },
        {
            'name': 'Tourisme',
            'slug': 'tourisme',
            'description': 'Secteur touristique, destinations et attractions du Maroc',
            'order': 7
        },
        {
            'name': 'Sport',
            'slug': 'sport',
            'description': 'Actualités sportives, compétitions et performances',
            'order': 8
        }
    ]
    
    for cat_data in categories_data:
        category, created = Category.objects.get_or_create(
            slug=cat_data['slug'],
            defaults=cat_data
        )
        if created:
            print(f"Catégorie créée: {category.name}")
        else:
            print(f"Catégorie existe déjà: {category.name}")


def create_tags():
    """Créer des tags populaires"""
    tags_data = [
        'Maroc', 'Développement', 'Innovation', 'Culture', 'Économie',
        'Politique', 'Société', 'Technologie', 'Environnement', 'Tourisme',
        'Éducation', 'Santé', 'Infrastructure', 'Investissement', 'Export',
        'Agriculture', 'Industrie', 'Services', 'Digital', 'Durabilité'
    ]
    
    for tag_name in tags_data:
        # Générer le slug automatiquement
        from django.utils.text import slugify
        slug = slugify(tag_name)
        
        try:
            # Vérifier si le tag existe déjà par nom ou slug
            existing_tag = Tag.objects.filter(name=tag_name).first() or Tag.objects.filter(slug=slug).first()
            
            if existing_tag:
                print(f"Tag existe déjà: {existing_tag.name}")
            else:
                tag = Tag.objects.create(name=tag_name, slug=slug)
                print(f"Tag créé: {tag.name}")
        except Exception as e:
            print(f"Erreur lors de la création du tag '{tag_name}': {e}")


def main():
    """Fonction principale"""
    print("Création des données initiales pour RevueMaroc...")
    
    create_site_settings()
    create_categories()
    create_tags()
    
    print("\nDonnées initiales créées avec succès!")
    print("Vous pouvez maintenant accéder à l'interface d'administration à l'adresse: http://127.0.0.1:8000/admin/")


if __name__ == '__main__':
    main()
