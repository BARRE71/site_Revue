# RevueMaroc - Plateforme de Revue Culturelle et Littéraire du Maroc

## 🎯 Vue d'ensemble

RevueMaroc est une application web Django moderne qui offre une plateforme complète pour la publication d'articles, la vente de livres numériques et physiques, et la gestion d'abonnements premium. Le projet est maintenant hébergé dans le dossier `site_Revue` sur le bureau, complètement indépendant de l'ancien projet `maroc_platform`.

## 🚀 Fonctionnalités Principales

### 📰 Articles et Blog
- Système de publication d'articles avec catégories et tags
- Articles premium réservés aux abonnés
- Système de commentaires et interactions
- Recherche et filtrage avancés

### 📚 E-commerce de Livres
- Catalogue de livres numériques et physiques
- Système de panier d'achat
- Intégration avec Stripe pour les paiements
- Gestion des commandes et livraisons

### 👥 Gestion des Utilisateurs
- Inscription et connexion sécurisées
- Profils utilisateurs personnalisés
- Rôles : Utilisateur normal, Abonné, Administrateur
- Tableau de bord personnel

### 💳 Système d'Abonnements
- Plans mensuels et annuels
- Paiements récurrents via Stripe
- Accès aux contenus premium
- Newsletter personnalisée

## 🛠️ Architecture Technique

### Backend
- **Framework** : Django 5.0.6
- **Base de données** : SQLite (développement) / PostgreSQL (production)
- **Authentification** : Django Auth avec profils personnalisés
- **API** : REST API avec Django REST Framework (à implémenter)

### Frontend
- **Framework CSS** : Bootstrap 5
- **Icônes** : Font Awesome
- **JavaScript** : Vanilla JS + jQuery (optionnel)
- **Responsive** : Design mobile-first

### Applications Django
- **`core`** : Modèles de base, vues principales, contextes globaux
- **`articles`** : Gestion des articles et commentaires
- **`livres`** : Catalogue et vente de livres
- **`users`** : Gestion des utilisateurs et profils
- **`subscriptions`** : Plans d'abonnement et paiements

## 📁 Structure du Projet

```
site_Revue/
├── revue_maroc/          # Configuration principale du projet
│   ├── settings.py       # Paramètres Django
│   ├── urls.py          # URLs principales
│   └── wsgi.py          # Configuration WSGI
├── core/                 # Application principale
│   ├── models.py        # Modèles de base (Category, Tag, etc.)
│   ├── views.py         # Vues principales (home, about, contact)
│   ├── urls.py          # URLs de l'application core
│   └── admin.py         # Interface d'administration
├── articles/             # Gestion des articles
│   ├── models.py        # Modèles Article et Comment
│   ├── views.py         # Vues des articles
│   └── urls.py          # URLs des articles
├── livres/               # E-commerce des livres
│   ├── models.py        # Modèles Book, Author, Order
│   ├── views.py         # Vues des livres
│   └── urls.py          # URLs des livres
├── users/                # Gestion des utilisateurs
│   ├── models.py        # Modèle UserProfile
│   ├── views.py         # Vues d'authentification
│   └── urls.py          # URLs des utilisateurs
├── subscriptions/        # Gestion des abonnements
│   ├── models.py        # Modèles Subscription et Payment
│   ├── views.py         # Vues des abonnements
│   └── urls.py          # URLs des abonnements
├── templates/            # Templates HTML
│   ├── base.html        # Template de base
│   ├── core/            # Templates de l'application core
│   ├── articles/        # Templates des articles
│   ├── livres/          # Templates des livres
│   ├── users/           # Templates des utilisateurs
│   └── subscriptions/   # Templates des abonnements
├── static/               # Fichiers statiques
├── media/                # Fichiers uploadés
├── manage.py            # Script de gestion Django
└── requirements.txt      # Dépendances Python
```

## 🚀 Installation et Configuration

### Prérequis
- Python 3.11+
- pip (gestionnaire de paquets Python)
- Git (pour le contrôle de version)

### Installation

1. **Cloner le projet** (si applicable)
```bash
cd C:\Users\lenovo\Desktop
git clone [URL_DU_REPO] site_Revue
cd site_Revue
```

2. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

3. **Configurer la base de données**
```bash
python manage.py makemigrations
python manage.py migrate
```

4. **Créer un superutilisateur**
```bash
python manage.py createsuperuser
```

5. **Créer les données initiales**
```bash
python create_simple_data.py
```

6. **Démarrer le serveur de développement**
```bash
python manage.py runserver
```

### Accès
- **Site web** : http://127.0.0.1:8000/
- **Administration** : http://127.0.0.1:8000/admin/

## 🔧 Configuration

### Variables d'environnement
Créez un fichier `.env` à la racine du projet :

```env
SECRET_KEY=votre_clé_secrète
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
STRIPE_PUBLIC_KEY=votre_clé_publique_stripe
STRIPE_SECRET_KEY=votre_clé_secrète_stripe
```

### Base de données
- **Développement** : SQLite (par défaut)
- **Production** : PostgreSQL recommandé

## 📊 Base de Données

### Modèles Principaux
- **User** : Utilisateurs Django avec profils étendus
- **Category** : Catégories pour articles et livres
- **Tag** : Tags pour le classement du contenu
- **Article** : Articles du blog avec statuts et métadonnées
- **Book** : Livres avec formats et gestion des stocks
- **Order** : Commandes et gestion des ventes
- **Subscription** : Abonnements et plans de paiement

## 🎨 Interface Utilisateur

### Design System
- **Couleurs** : Palette professionnelle avec bleu primaire
- **Typographie** : Hiérarchie claire et lisible
- **Composants** : Cards, boutons, formulaires Bootstrap 5
- **Responsive** : Adaptation mobile, tablette et desktop

### Pages Principales
- **Accueil** : Présentation, statistiques, contenu en vedette
- **Articles** : Liste, filtres, recherche, pagination
- **Livres** : Catalogue, détails, panier, commande
- **À propos** : Mission, équipe, valeurs
- **Contact** : Formulaire de contact et informations

## 🔒 Sécurité

### Authentification
- Sessions Django sécurisées
- Protection CSRF sur tous les formulaires
- Validation des permissions par rôle

### Données
- Validation des formulaires côté serveur
- Protection contre les injections SQL
- Chiffrement des mots de passe

## 🚀 Déploiement

### Production
- **Serveur** : Gunicorn + Nginx
- **Base de données** : PostgreSQL
- **Fichiers statiques** : CDN ou serveur web
- **HTTPS** : Certificat SSL obligatoire

### Environnement
- **Python** : 3.11+
- **Django** : 5.0.6
- **Serveur** : Linux recommandé

## 📈 Évolutions Futures

### Phase 2
- API REST complète
- Application mobile React Native
- Système de notifications push
- Analytics et reporting avancés

### Phase 3
- Intelligence artificielle pour recommandations
- Système de gamification
- Intégration réseaux sociaux
- Marketplace multi-vendeurs

## 🤝 Contribution

### Développement
1. Fork du projet
2. Création d'une branche feature
3. Commit des changements
4. Pull Request avec description détaillée

### Standards
- **Code** : PEP 8 pour Python
- **Templates** : HTML5 sémantique
- **CSS** : BEM methodology
- **Tests** : Couverture > 80%

## 📞 Support

### Contact
- **Email** : contact@revuemaroc.com
- **Site web** : https://revuemaroc.com
- **Documentation** : Wiki du projet

### Communauté
- **Forum** : Discussions et questions
- **Slack** : Équipe de développement
- **GitHub** : Issues et contributions

---

**RevueMaroc** - Propulsé par Django et l'innovation technologique marocaine 🇲🇦

*Dernière mise à jour : Août 2025*
