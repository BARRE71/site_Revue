from django import forms
from .models import RevueCategory, Revue


class RevueFilterForm(forms.Form):
    """Formulaire de filtrage pour le catalogue des revues"""
    
    # Filtre par catégorie
    category = forms.ModelChoiceField(
        queryset=RevueCategory.objects.filter(is_active=True),
        required=False,
        empty_label="Toutes les catégories",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    # Filtre par langue
    language = forms.ChoiceField(
        choices=[('', 'Toutes les langues'), ('fr', 'Français'), ('ar', 'Arabe'), ('en', 'Anglais')],
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    # Filtre par format
    format = forms.ChoiceField(
        choices=[('', 'Tous les formats'), ('papier', 'Format papier'), ('pdf', 'Format PDF'), ('both', 'Les deux formats')],
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    # Filtre par prix
    min_price = forms.DecimalField(
        required=False,
        min_value=0,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Prix min (€)',
            'step': '0.01'
        })
    )
    
    max_price = forms.DecimalField(
        required=False,
        min_value=0,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Prix max (€)',
            'step': '0.01'
        })
    )
    
    # Filtre par année
    year = forms.IntegerField(
        required=False,
        min_value=1900,
        max_value=2100,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Année'
        })
    )
    
    # Filtre par thème
    theme = forms.CharField(
        required=False,
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Rechercher par thème...'
        })
    )
    
    def clean(self):
        """Validation personnalisée du formulaire"""
        cleaned_data = super().clean()
        min_price = cleaned_data.get('min_price')
        max_price = cleaned_data.get('max_price')
        
        # Vérifier que le prix minimum n'est pas supérieur au prix maximum
        if min_price and max_price and min_price > max_price:
            raise forms.ValidationError(
                "Le prix minimum ne peut pas être supérieur au prix maximum."
            )
        
        return cleaned_data


class AddToCartForm(forms.Form):
    """Formulaire pour ajouter une revue au panier"""
    
    format = forms.ChoiceField(
        choices=[('papier', 'Format papier'), ('pdf', 'Format PDF')],
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'})
    )
    
    quantity = forms.IntegerField(
        min_value=1,
        max_value=10,
        initial=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '1',
            'max': '10'
        })
    )
    
    def __init__(self, *args, **kwargs):
        revue = kwargs.pop('revue', None)
        super().__init__(*args, **kwargs)
        
        if revue:
            # Adapter les choix de format selon la disponibilité
            format_choices = []
            if revue.is_available_paper:
                format_choices.append(('papier', 'Format papier'))
            if revue.is_available_pdf:
                format_choices.append(('pdf', 'Format PDF'))
            
            if format_choices:
                self.fields['format'].choices = format_choices
                if len(format_choices) == 1:
                    self.fields['format'].initial = format_choices[0][0]
                    self.fields['format'].widget.attrs['disabled'] = True


class CartItemUpdateForm(forms.Form):
    """Formulaire pour mettre à jour un article du panier"""
    
    quantity = forms.IntegerField(
        min_value=1,
        max_value=10,
        widget=forms.NumberInput(attrs={
            'class': 'form-control form-control-sm',
            'min': '1',
            'max': '10'
        })
    )
