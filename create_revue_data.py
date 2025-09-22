#!/usr/bin/env python
"""
Script pour créer des données de démonstration pour la Revue Délibérée
"""

import os
import sys
import django
from datetime import date, timedelta
from decimal import Decimal

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'revue_maroc.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import Category, Tag
from livres.models import Revue, RevueArticle, Author, RevueCategory
from django.utils.text import slugify


def create_categories():
    """Créer les catégories de revues"""
    categories_data = [
        {
            'name': 'Politique et Société',
            'description': 'Analyses politiques, questions sociales et débats contemporains',
            'slug': 'politique-societe'
        },
        {
            'name': 'Économie et Développement',
            'description': 'Économie marocaine, développement durable et enjeux économiques',
            'slug': 'economie-developpement'
        },
        {
            'name': 'Culture et Identité',
            'description': 'Patrimoine culturel, identité marocaine et expressions artistiques',
            'slug': 'culture-identite'
        },
        {
            'name': 'Droit et Justice',
            'description': 'Questions juridiques, réformes et système judiciaire',
            'slug': 'droit-justice'
        },
        {
            'name': 'Éducation et Recherche',
            'description': 'Système éducatif, recherche scientifique et innovation',
            'slug': 'education-recherche'
        }
    ]
    
    categories = []
    for cat_data in categories_data:
        category, created = RevueCategory.objects.get_or_create(
            slug=cat_data['slug'],
            defaults=cat_data
        )
        categories.append(category)
        if created:
            print(f"✓ Catégorie créée : {category.name}")
        else:
            print(f"→ Catégorie existante : {category.name}")
    
    return categories


def create_tags():
    """Créer les tags thématiques"""
    tags_data = [
        'Maroc', 'Démocratie', 'Développement', 'Économie', 'Culture', 'Identité',
        'Justice', 'Éducation', 'Recherche', 'Innovation', 'Durabilité', 'Inclusion',
        'Méditerranée', 'Afrique', 'Europe', 'International', 'Local', 'Régional',
        'Histoire', 'Patrimoine', 'Modernité', 'Tradition', 'Réforme', 'Changement'
    ]
    
    tags = []
    for tag_name in tags_data:
        tag_slug = slugify(tag_name)
        tag, created = Tag.objects.get_or_create(
            slug=tag_slug,
            defaults={'name': tag_name}
        )
        tags.append(tag)
        if created:
            print(f"✓ Tag créé : {tag.name}")
        else:
            print(f"→ Tag existant : {tag.name}")
    
    return tags


def create_authors():
    """Créer des auteurs de démonstration"""
    authors_data = [
        {
            'name': 'Dr. Ahmed Benali',
            'bio': 'Professeur de sciences politiques à l\'Université Mohammed V de Rabat. Spécialiste des questions de démocratie et de gouvernance au Maroc.',
            'academic_title': 'Professeur des Universités',
            'institution': 'Université Mohammed V, Rabat',
            'country': 'MA',
            'is_featured': True
        },
        {
            'name': 'Prof. Fatima Zahra Alami',
            'bio': 'Économiste et chercheuse au Centre d\'Études Économiques de Casablanca. Expert en développement économique et politiques publiques.',
            'academic_title': 'Directrice de Recherche',
            'institution': 'Centre d\'Études Économiques, Casablanca',
            'country': 'MA',
            'is_featured': True
        },
        {
            'name': 'Dr. Karim Mansouri',
            'bio': 'Juriste et avocat spécialisé en droit constitutionnel. Membre du Conseil National des Droits de l\'Homme.',
            'academic_title': 'Docteur en Droit',
            'institution': 'Barreau de Casablanca',
            'country': 'MA',
            'is_featured': False
        },
        {
            'name': 'Dr. Leila Benjelloun',
            'bio': 'Sociologue et anthropologue. Ses recherches portent sur l\'identité culturelle et les transformations sociales au Maroc.',
            'academic_title': 'Maître de Conférences',
            'institution': 'Université Hassan II, Casablanca',
            'country': 'MA',
            'is_featured': False
        },
        {
            'name': 'Prof. Hassan El Fassi',
            'bio': 'Historien spécialisé dans l\'histoire contemporaine du Maroc. Auteur de plusieurs ouvrages sur la période post-coloniale.',
            'academic_title': 'Professeur des Universités',
            'institution': 'Université Ibn Zohr, Agadir',
            'country': 'MA',
            'is_featured': True
        }
    ]
    
    authors = []
    for author_data in authors_data:
        author_data['slug'] = slugify(author_data['name'])
        author, created = Author.objects.get_or_create(
            slug=author_data['slug'],
            defaults=author_data
        )
        authors.append(author)
        if created:
            print(f"✓ Auteur créé : {author.name}")
        else:
            print(f"→ Auteur existant : {author.name}")
    
    return authors


def create_revues(categories, tags, authors):
    """Créer des numéros de revue de démonstration"""
    revues_data = [
        {
            'numero': 25,
            'title': 'Handicaps : dévalider la justice',
            'subtitle': 'Réflexions sur l\'accessibilité et l\'inclusion dans le système judiciaire',
            'description': 'Ce numéro explore les défis de l\'accessibilité pour les personnes en situation de handicap dans le système judiciaire marocain. Il examine les obstacles actuels et propose des solutions pour une justice plus inclusive.',
            'excerpt': 'Comment rendre la justice accessible à tous ? Ce numéro propose une réflexion approfondie sur les enjeux de l\'inclusion dans le système judiciaire.',
            'editorial': 'L\'accessibilité de la justice n\'est pas seulement une question de droits, c\'est un impératif démocratique. Ce numéro invite à repenser nos pratiques pour une justice véritablement inclusive.',
            'language': 'fr',
            'pages_count': 180,
            'dimensions': '21x29.7 cm',
            'isbn': '978-2-123456-78-9',
            'issn': '1234-5678',
            'publication_date': date(2024, 6, 15),
            'format': 'both',
            'price_paper': Decimal('25.00'),
            'price_pdf': Decimal('15.00'),
            'stock_paper': 150,
            'stock_pdf': 999,
            'is_featured': True,
            'category': categories[3],  # Droit et Justice
            'tags': [tags[0], tags[1], tags[11], tags[12]]  # Maroc, Démocratie, Inclusion, Justice
        },
        {
            'numero': 24,
            'title': 'Épreuves de nationalité',
            'subtitle': 'Identité, appartenance et citoyenneté au Maroc contemporain',
            'description': 'Ce numéro examine les questions complexes de nationalité, d\'identité et de citoyenneté dans le Maroc d\'aujourd\'hui. Il explore les défis de la construction d\'une identité nationale inclusive.',
            'excerpt': 'Qu\'est-ce qu\'être marocain aujourd\'hui ? Ce numéro explore les multiples facettes de l\'identité nationale et les enjeux de la citoyenneté.',
            'editorial': 'La question de la nationalité touche au cœur de notre identité collective. Ce numéro invite à une réflexion critique sur ce qui nous unit et ce qui nous distingue.',
            'language': 'fr',
            'pages_count': 160,
            'dimensions': '21x29.7 cm',
            'isbn': '978-2-123456-77-2',
            'issn': '1234-5678',
            'publication_date': date(2024, 3, 20),
            'format': 'both',
            'price_paper': Decimal('23.00'),
            'price_pdf': Decimal('14.00'),
            'stock_paper': 120,
            'stock_pdf': 999,
            'is_featured': False,
            'category': categories[2],  # Culture et Identité
            'tags': [tags[0], tags[2], tags[4], tags[5], tags[20]]  # Maroc, Développement, Culture, Identité, Histoire
        },
        {
            'numero': 23,
            'title': 'Poursuivre les luttes',
            'description': 'Mouvements sociaux, résistances et transformations au Maroc',
            'excerpt': 'Ce numéro documente et analyse les mouvements sociaux contemporains au Maroc, leurs revendications et leur impact sur la société.',
            'editorial': 'Les luttes sociales sont le moteur du changement. Ce numéro rend hommage à tous ceux qui se battent pour un Maroc plus juste et plus démocratique.',
            'language': 'fr',
            'pages_count': 200,
            'dimensions': '21x29.7 cm',
            'isbn': '978-2-123456-76-5',
            'issn': '1234-5678',
            'publication_date': date(2023, 12, 10),
            'format': 'both',
            'price_paper': Decimal('22.00'),
            'price_pdf': Decimal('13.00'),
            'stock_paper': 80,
            'stock_pdf': 999,
            'is_featured': False,
            'category': categories[0],  # Politique et Société
            'tags': [tags[0], tags[1], tags[2], tags[22], tags[23]]  # Maroc, Démocratie, Développement, Réforme, Changement
        },
        {
            'numero': 22,
            'title': 'La faute aux pauvres',
            'subtitle': 'Pauvreté, inégalités et politiques sociales au Maroc',
            'description': 'Ce numéro analyse les mécanismes de la pauvreté et des inégalités au Maroc, et évalue l\'efficacité des politiques sociales mises en place.',
            'excerpt': 'La pauvreté n\'est pas une fatalité. Ce numéro propose des analyses et des solutions pour lutter contre les inégalités.',
            'editorial': 'Il est temps de cesser de blâmer les pauvres pour leur situation. Ce numéro invite à une réflexion critique sur les causes structurelles de la pauvreté.',
            'language': 'fr',
            'pages_count': 175,
            'dimensions': '21x29.7 cm',
            'isbn': '978-2-123456-75-8',
            'issn': '1234-5678',
            'publication_date': date(2023, 9, 5),
            'format': 'both',
            'price_paper': Decimal('21.00'),
            'price_pdf': Decimal('12.00'),
            'stock_paper': 60,
            'stock_pdf': 999,
            'is_featured': False,
            'category': categories[1],  # Économie et Développement
            'tags': [tags[0], tags[2], tags[3], tags[11], tags[12]]  # Maroc, Développement, Économie, Inclusion, Local
        }
    ]
    
    revues = []
    for revue_data in revues_data:
        revue_data['slug'] = slugify(f"deliberee-{revue_data['numero']}-{revue_data['title']}")
        # Extraire les tags avant de créer la revue
        tags_to_add = revue_data.pop('tags', [])
        
        revue, created = Revue.objects.get_or_create(
            numero=revue_data['numero'],
            defaults=revue_data
        )
        
        # Ajouter les tags après création
        if tags_to_add:
            revue.tags.set(tags_to_add)
        revues.append(revue)
        if created:
            print(f"✓ Revue créée : N°{revue.numero} - {revue.title}")
        else:
            print(f"→ Revue existante : N°{revue.numero} - {revue.title}")
    
    return revues


def create_articles(revues, authors):
    """Créer des articles de démonstration"""
    articles_data = [
        # Articles pour la revue N°25
        {
            'title': 'L\'accessibilité judiciaire : un défi démocratique',
            'abstract': 'Cet article examine les obstacles à l\'accessibilité dans le système judiciaire marocain et propose des solutions concrètes pour améliorer l\'inclusion des personnes en situation de handicap.',
            'content': 'Contenu détaillé de l\'article sur l\'accessibilité judiciaire...',
            'keywords': 'accessibilité, justice, handicap, inclusion, démocratie',
            'page_start': 15,
            'page_end': 35,
            'revue': revues[0],  # N°25
            'author': authors[2]  # Karim Mansouri
        },
        {
            'title': 'Handicap et citoyenneté : vers une approche inclusive',
            'abstract': 'Analyse des enjeux de la citoyenneté pour les personnes en situation de handicap au Maroc.',
            'content': 'Contenu détaillé de l\'article sur la citoyenneté...',
            'keywords': 'citoyenneté, handicap, inclusion, droits, Maroc',
            'page_start': 37,
            'page_end': 58,
            'revue': revues[0],  # N°25
            'author': authors[0]  # Ahmed Benali
        },
        
        # Articles pour la revue N°24
        {
            'title': 'Nationalité et identité : les enjeux contemporains',
            'abstract': 'Exploration des défis de la construction identitaire dans le Maroc contemporain.',
            'content': 'Contenu détaillé de l\'article sur l\'identité...',
            'keywords': 'nationalité, identité, Maroc, citoyenneté, culture',
            'page_start': 12,
            'page_end': 32,
            'revue': revues[1],  # N°24
            'author': authors[4]  # Hassan El Fassi
        },
        
        # Articles pour la revue N°23
        {
            'title': 'Mouvements sociaux et démocratie participative',
            'abstract': 'Analyse du rôle des mouvements sociaux dans la démocratisation du Maroc.',
            'content': 'Contenu détaillé de l\'article sur les mouvements sociaux...',
            'keywords': 'mouvements sociaux, démocratie, participation, Maroc',
            'page_start': 18,
            'page_end': 42,
            'revue': revues[2],  # N°23
            'author': authors[0]  # Ahmed Benali
        },
        
        # Articles pour la revue N°22
        {
            'title': 'Pauvreté et inégalités : analyse des mécanismes',
            'abstract': 'Examen des causes structurelles de la pauvreté et des inégalités au Maroc.',
            'content': 'Contenu détaillé de l\'article sur la pauvreté...',
            'keywords': 'pauvreté, inégalités, développement, Maroc, politiques sociales',
            'page_start': 22,
            'page_end': 48,
            'revue': revues[3],  # N°22
            'author': authors[1]  # Fatima Zahra Alami
        }
    ]
    
    for article_data in articles_data:
        article_data['slug'] = slugify(article_data['title'])
        article, created = RevueArticle.objects.get_or_create(
            slug=article_data['slug'],
            defaults=article_data
        )
        if created:
            print(f"✓ Article créé : {article.title}")
        else:
            print(f"→ Article existant : {article.title}")


def main():
    """Fonction principale"""
    print("🚀 Création des données de démonstration pour la Revue Délibérée")
    print("=" * 60)
    
    try:
        # Créer les catégories
        print("\n📚 Création des catégories...")
        categories = create_categories()
        
        # Créer les tags
        print("\n🏷️ Création des tags...")
        tags = create_tags()
        
        # Créer les auteurs
        print("\n👥 Création des auteurs...")
        authors = create_authors()
        
        # Créer les revues
        print("\n📖 Création des revues...")
        revues = create_revues(categories, tags, authors)
        
        # Créer les articles
        print("\n📄 Création des articles...")
        create_articles(revues, authors)
        
        print("\n" + "=" * 60)
        print("✅ Données de démonstration créées avec succès !")
        print(f"📊 Résumé : {len(categories)} catégories, {len(tags)} tags, {len(authors)} auteurs, {len(revues)} revues")
        print("\n🌐 Vous pouvez maintenant accéder au site et voir le catalogue des revues !")
        
    except Exception as e:
        print(f"\n❌ Erreur lors de la création des données : {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
