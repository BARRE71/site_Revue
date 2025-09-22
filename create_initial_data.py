#!/usr/bin/env python
"""
Script pour créer des données initiales pour RevueMaroc
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
from articles.models import Article, ArticleCategory
from livres.models import Author, Book, BookCategory
from subscriptions.models import SubscriptionPlan


def create_superuser():
    """Créer un superutilisateur"""
    if not User.objects.filter(username='admin').exists():
        user = User.objects.create_superuser(
            username='admin',
            email='admin@revuemaroc.com',
            password='admin123'
        )
        print(f"Superutilisateur créé: {user.username}")
    else:
        print("Superutilisateur admin existe déjà")


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
        'Développement', 'Investissement', 'Infrastructure', 'Innovation', 'Durabilité',
        'Digital', 'Énergie', 'Transport', 'Agriculture', 'Industrie', 'Commerce',
        'Finance', 'Banque', 'Startup', 'Entrepreneuriat', 'Formation', 'Recherche',
        'Santé', 'Éducation', 'Logement', 'Urbanisme', 'Rural', 'Côtier',
        'Atlas', 'Sahara', 'Méditerranée', 'Atlantique', 'Tradition', 'Modernité'
    ]
    
    for tag_name in tags_data:
        tag, created = Tag.objects.get_or_create(
            name=tag_name,
            defaults={'slug': tag_name.lower().replace(' ', '-')}
        )
        if created:
            print(f"Tag créé: {tag.name}")
        else:
            print(f"Tag existe déjà: {tag.name}")


def create_authors():
    """Créer quelques auteurs de test"""
    authors_data = [
        {
            'name': 'Dr. Ahmed Benali',
            'slug': 'ahmed-benali',
            'bio': 'Expert en économie du développement avec plus de 20 ans d\'expérience',
            'is_featured': True
        },
        {
            'name': 'Prof. Fatima Zahra',
            'slug': 'fatima-zahra',
            'bio': 'Spécialiste en politiques publiques et développement social',
            'is_featured': True
        },
        {
            'name': 'M. Karim El Amrani',
            'slug': 'karim-el-amrani',
            'bio': 'Analyste politique et consultant en affaires internationales',
            'is_featured': False
        },
        {
            'name': 'Dr. Leila Mansouri',
            'slug': 'leila-mansouri',
            'bio': 'Chercheuse en environnement et développement durable',
            'is_featured': True
        }
    ]
    
    for author_data in authors_data:
        author, created = Author.objects.get_or_create(
            slug=author_data['slug'],
            defaults=author_data
        )
        if created:
            print(f"Auteur créé: {author.name}")
        else:
            print(f"Auteur existe déjà: {author.name}")


def create_subscription_plans():
    """Créer les plans d'abonnement"""
    plans_data = [
        {
            'name': 'Plan Mensuel',
            'slug': 'plan-mensuel',
            'description': 'Accès complet à tous les articles premium et réductions sur les livres',
            'plan_type': 'monthly',
            'duration_months': 1,
            'price': 9.99,
            'is_active': True,
            'is_popular': False,
            'features': [
                'Accès à tous les articles premium',
                'Réduction de 15% sur les livres',
                'Newsletter exclusive',
                'Support prioritaire'
            ]
        },
        {
            'name': 'Plan Annuel',
            'slug': 'plan-annuel',
            'description': 'Accès premium annuel avec économies et bonus exclusifs',
            'plan_type': 'yearly',
            'duration_months': 12,
            'price': 99.99,
            'original_price': 119.88,
            'is_active': True,
            'is_popular': True,
            'features': [
                'Accès à tous les articles premium',
                'Réduction de 20% sur les livres',
                'Newsletter exclusive',
                'Support prioritaire',
                '2 mois gratuits',
                'Contenu exclusif annuel'
            ]
        },
        {
            'name': 'Plan Étudiant',
            'slug': 'plan-etudiant',
            'description': 'Tarif préférentiel pour les étudiants avec justificatif',
            'plan_type': 'monthly',
            'duration_months': 1,
            'price': 4.99,
            'is_active': True,
            'is_popular': False,
            'features': [
                'Accès à tous les articles premium',
                'Réduction de 10% sur les livres',
                'Newsletter exclusive',
                'Support standard'
            ]
        }
    ]
    
    for plan_data in plans_data:
        plan, created = SubscriptionPlan.objects.get_or_create(
            slug=plan_data['slug'],
            defaults=plan_data
        )
        if created:
            print(f"Plan créé: {plan.name}")
        else:
            print(f"Plan existe déjà: {plan.name}")


def create_sample_articles():
    """Créer quelques articles de test"""
    if not Article.objects.exists():
        # Récupérer un utilisateur et une catégorie
        user = User.objects.first()
        if not user:
            print("Aucun utilisateur trouvé pour créer des articles")
            return
            
        category = Category.objects.first()
        if not category:
            print("Aucune catégorie trouvée pour créer des articles")
            return
        
        articles_data = [
            {
                'title': 'Le Maroc, hub technologique en devenir',
                'slug': 'maroc-hub-technologique',
                'excerpt': 'Analyse du potentiel du Maroc comme centre d\'innovation technologique en Afrique',
                'content': 'Le Maroc se positionne de plus en plus comme un hub technologique prometteur...',
                'author': user,
                'category': category,
                'status': 'published',
                'is_featured': True,
                'is_premium': False,
                'published_at': timezone.now() - timedelta(days=1)
            },
            {
                'title': 'Les énergies renouvelables au Maroc',
                'slug': 'energies-renouvelables-maroc',
                'excerpt': 'État des lieux et perspectives du développement des énergies vertes',
                'content': 'Le Maroc s\'engage résolument dans la transition énergétique...',
                'author': user,
                'category': category,
                'status': 'published',
                'is_featured': True,
                'is_premium': True,
                'published_at': timezone.now() - timedelta(days=2)
            }
        ]
        
        for article_data in articles_data:
            article = Article.objects.create(**article_data)
            print(f"Article créé: {article.title}")
    else:
        print("Des articles existent déjà")


def main():
    """Fonction principale"""
    print("=== Création des données initiales pour RevueMaroc ===\n")
    
    try:
        create_superuser()
        print()
        
        create_site_settings()
        print()
        
        create_categories()
        print()
        
        create_tags()
        print()
        
        create_authors()
        print()
        
        create_subscription_plans()
        print()
        
        create_sample_articles()
        print()
        
        print("=== Données initiales créées avec succès ! ===")
        print("\nVous pouvez maintenant:")
        print("1. Vous connecter avec admin/admin123")
        print("2. Accéder à l'interface d'administration")
        print("3. Tester l'application")
        
    except Exception as e:
        print(f"Erreur lors de la création des données: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
