from django import forms
from django.utils.html import format_html
import json

class FeaturesWidget(forms.Textarea):
    """Widget personnalisé pour la saisie des fonctionnalités"""
    
    def __init__(self, attrs=None):
        default_attrs = {
            'rows': 6,
            'cols': 50,
            'placeholder': 'Saisissez les fonctionnalités, une par ligne:\nAccès à tous les numéros\nSupport prioritaire\nTéléchargement PDF\nContenu exclusif'
        }
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)
    
    def format_value(self, value):
        """Convertir la liste JSON en texte lisible"""
        if not value:
            return ''
        try:
            if isinstance(value, str):
                features = json.loads(value)
            else:
                features = value
            return '\n'.join(features)
        except (json.JSONDecodeError, TypeError):
            return str(value)
    
    def value_from_datadict(self, data, files, name):
        """Convertir le texte en liste JSON"""
        value = data.get(name, '')
        if not value:
            return '[]'
        
        # Diviser par lignes et nettoyer
        features = [line.strip() for line in value.split('\n') if line.strip()]
        return json.dumps(features, ensure_ascii=False)
    
    def render(self, name, value, attrs=None, renderer=None):
        """Rendu du widget avec aide visuelle"""
        html = super().render(name, value, attrs, renderer)
        
        help_text = format_html(
            '<div class="help" style="margin-top: 5px; font-size: 12px; color: #666;">'
            '<strong>Format:</strong> Une fonctionnalité par ligne. '
            'Exemple:<br>'
            '• Accès à tous les numéros<br>'
            '• Support prioritaire<br>'
            '• Téléchargement PDF'
            '</div>'
        )
        
        return html + help_text
