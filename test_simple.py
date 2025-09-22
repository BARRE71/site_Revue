#!/usr/bin/env python
"""
Script de test simple pour vérifier la configuration Django
"""
import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'revue_maroc.settings')

try:
    django.setup()
    print("✅ Django configuré avec succès")
    
    # Vérifier les applications installées
    from django.conf import settings
    print(f"✅ Applications installées: {settings.INSTALLED_APPS}")
    
    # Vérifier la base de données
    from django.db import connection
    cursor = connection.cursor()
    print("✅ Connexion à la base de données réussie")
    
    # Vérifier les modèles
    from django.apps import apps
    print(f"✅ Modèles disponibles: {[model.__name__ for model in apps.get_models()]}")
    
    print("\n🎉 Configuration Django valide !")
    
except Exception as e:
    print(f"❌ Erreur: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
