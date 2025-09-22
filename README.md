# RevueMaroc - Plateforme d'Information sur le Développement du Maroc

## 🎯 Description du Projet

RevueMaroc est une plateforme web moderne développée avec Django qui offre :
- **Articles et analyses** sur le développement du Maroc
- **Vente de livres** numériques et physiques
- **Système d'abonnements** premium
- **Interface multilingue** (Français, Arabe, Anglais)
- **Design responsive** inspiré des meilleures plateformes e-commerce

## 🏗️ Architecture Technique

### Technologies Utilisées
- **Backend** : Django 5.0.6
- **Base de données** : SQLite (développement) / PostgreSQL (production)
- **Frontend** : Bootstrap 5, HTML5, CSS3, JavaScript
- **Paiements** : Stripe, PayPal
- **Authentification** : Django Auth avec rôles personnalisés
- **Internationalisation** : Support multilingue complet

### Applications Django
- **`core`** : Fonctionnalités principales, pages statiques, contact
- **`articles`** : Gestion des articles, blog, commentaires
- **`livres`** : E-commerce, gestion des livres, panier, commandes
- **`users`** : Gestion des utilisateurs, profils, rôles
- **`subscriptions`** : Plans d'abonnement, paiements récurrents

## 🚀 Installation et Configuration

### Prérequis
- Python 3.11+
- pip
- Git

### Installation

1. **Cloner le projet**
   ```bash
   git clone <repository-url>
   cd revue_maroc
   ```

2. **Créer un environnement virtuel**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # ou
   venv\Scripts\activate     # Windows
   ```

3. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurer la base de données**
   ```bash
   python manage.py migrate
   ```

5. **Créer un superutilisateur**
   ```bash
   python manage.py createsuperuser
   ```

6. **Lancer le serveur de développement**
   ```bash
   python manage.py runserver
   ```

### Configuration de Production

1. **Base de données PostgreSQL**
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'revue_maroc_db',
           'USER': 'revue_maroc_user',
           'PASSWORD': 'your_secure_password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

2. **Variables d'environnement**
   ```bash
   export SECRET_KEY="your-secret-key"
   export DEBUG=False
   export ALLOWED_HOSTS="yourdomain.com,www.yourdomain.com"
   ```

3. **Configuration des paiements**
   ```bash
   export STRIPE_PUBLISHABLE_KEY="pk_live_..."
   export STRIPE_SECRET_KEY="sk_live_..."
   export PAYPAL_CLIENT_ID="your-paypal-client-id"
   export PAYPAL_CLIENT_SECRET="your-paypal-secret"
   ```

## 📁 Structure du Projet

```
revue_maroc/
├── core/                   # Application principale
│   ├── models.py          # Modèles de base (Contact, Newsletter, etc.)
│   ├── views.py           # Vues principales (accueil, contact, etc.)
│   ├── urls.py            # URLs de l'application
│   └── admin.py           # Interface d'administration
├── articles/              # Gestion des articles
│   ├── models.py          # Modèles Article, Commentaire, etc.
│   ├── views.py           # Vues pour les articles
│   └── urls.py            # URLs des articles
├── livres/                # E-commerce des livres
│   ├── models.py          # Modèles Book, Order, Cart, etc.
│   ├── views.py           # Vues pour la boutique
│   └── urls.py            # URLs des livres
├── users/                 # Gestion des utilisateurs
│   ├── models.py          # Profils utilisateur étendus
│   ├── views.py           # Vues d'authentification
│   └── urls.py            # URLs des utilisateurs
├── subscriptions/         # Gestion des abonnements
│   ├── models.py          # Plans et abonnements
│   ├── views.py           # Vues des abonnements
│   └── urls.py            # URLs des abonnements
├── templates/             # Templates HTML
│   ├── base.html          # Template de base
│   ├── core/              # Templates de l'application core
│   ├── articles/          # Templates des articles
│   ├── livres/            # Templates des livres
│   ├── users/             # Templates des utilisateurs
│   └── subscriptions/     # Templates des abonnements
├── static/                # Fichiers statiques
│   ├── css/               # Styles CSS
│   ├── js/                # JavaScript
│   └── images/            # Images
├── media/                 # Fichiers uploadés
├── manage.py              # Script de gestion Django
├── requirements.txt        # Dépendances Python
└── README.md              # Ce fichier
```

## 🔧 Fonctionnalités Principales

### 1. Système d'Articles
- **CRUD complet** pour les articles
- **Catégorisation** et tags
- **Système de commentaires**
- **Articles premium** (réservés aux abonnés)
- **Recherche avancée** et filtres

### 2. E-commerce des Livres
- **Catalogue de livres** avec images et descriptions
- **Système de panier** et commandes
- **Paiements sécurisés** (Stripe/PayPal)
- **Gestion des stocks** et formats
- **Système de notation** et avis

### 3. Gestion des Utilisateurs
- **Inscription/Connexion** par email
- **Rôles personnalisés** (Normal, Abonné, Admin)
- **Profils utilisateur** étendus
- **Gestion des abonnements**

### 4. Système d'Abonnements
- **Plans mensuels/annuels**
- **Paiements récurrents**
- **Accès premium** aux articles
- **Réductions** sur les livres

## 🎨 Design et Interface

### Inspirations
- **Amazon** : Organisation des produits et navigation
- **AbeBooks** : Présentation des livres
- **Medium** : Interface de lecture des articles

### Composants UI
- **Navigation responsive** avec menu déroulant
- **Cartes de produits** avec effets hover
- **Formulaires stylisés** avec validation
- **Système de grille** Bootstrap 5
- **Icônes Font Awesome** pour une meilleure UX

## 🔒 Sécurité

### Authentification
- **Sessions sécurisées** Django
- **Validation des mots de passe** robuste
- **Protection CSRF** sur tous les formulaires

### Autorisations
- **Permissions granulaires** par rôle
- **Vérification des accès** aux contenus premium
- **Protection des routes** sensibles

### Paiements
- **HTTPS obligatoire** en production
- **Intégration sécurisée** Stripe/PayPal
- **Validation des transactions** côté serveur

## 🌐 Internationalisation

### Langues Supportées
- **Français** (langue principale)
- **Arabe** (support RTL)
- **Anglais** (international)

### Configuration
- **Fichiers de traduction** dans `locale/`
- **Sélecteur de langue** dans l'interface
- **Contenu multilingue** pour les articles

## 📊 Base de Données

### Modèles Principaux
- **User** : Utilisateurs et authentification
- **Article** : Contenu du blog avec métadonnées
- **Book** : Catalogue des livres
- **Order** : Commandes et paiements
- **Subscription** : Plans et abonnements actifs

### Relations
- **One-to-Many** : User → Articles, User → Orders
- **Many-to-Many** : Articles ↔ Tags, Books ↔ Categories
- **One-to-One** : User ↔ UserProfile

## 🚀 Déploiement

### Environnement de Production
- **Serveur web** : Nginx + Gunicorn
- **Base de données** : PostgreSQL
- **Cache** : Redis
- **Fichiers statiques** : CDN ou serveur dédié

### Variables d'Environnement
```bash
# Production
export DJANGO_SETTINGS_MODULE=revue_maroc.settings.production
export SECRET_KEY="your-production-secret-key"
export DEBUG=False
export DATABASE_URL="postgresql://user:pass@host:port/db"
```

## 🧪 Tests

### Exécution des Tests
```bash
# Tests unitaires
python manage.py test

# Tests avec couverture
coverage run --source='.' manage.py test
coverage report
coverage html
```

### Tests Automatisés
- **Tests unitaires** pour tous les modèles
- **Tests d'intégration** pour les vues
- **Tests de sécurité** pour l'authentification

## 📈 Performance

### Optimisations
- **Requêtes optimisées** avec select_related/prefetch_related
- **Cache Redis** pour les données fréquemment consultées
- **Pagination** pour les listes longues
- **Images optimisées** et lazy loading

### Monitoring
- **Logs structurés** pour le debugging
- **Métriques de performance** avec Django Debug Toolbar
- **Surveillance des erreurs** en production

## 🤝 Contribution

### Guidelines
1. **Fork** le projet
2. **Créer** une branche pour votre fonctionnalité
3. **Commiter** vos changements
4. **Pousser** vers la branche
5. **Créer** une Pull Request

### Standards de Code
- **PEP 8** pour le style Python
- **Docstrings** pour toutes les fonctions
- **Tests** pour les nouvelles fonctionnalités
- **Messages de commit** explicites

## 📞 Support

### Contact
- **Email** : contact@revuemaroc.com
- **Documentation** : [Lien vers la documentation]
- **Issues** : [Lien vers le tracker d'issues]

### Communauté
- **Forum** : [Lien vers le forum]
- **Discord** : [Lien vers le serveur Discord]
- **Newsletter** : [Lien pour s'abonner]

## 📄 Licence

Ce projet est sous licence [MIT](LICENSE). Voir le fichier LICENSE pour plus de détails.

## 🙏 Remerciements

- **Django** pour le framework web robuste
- **Bootstrap** pour le design responsive
- **Stripe/PayPal** pour les solutions de paiement
- **Communauté open source** pour les contributions

---

**RevueMaroc** - Votre fenêtre sur le développement du Maroc 🇲🇦
