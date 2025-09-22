# Generated manually for RevueMaroc project

from django.db import migrations, models
import django_countries.fields
import django.core.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Date de modification')),
                ('name', models.CharField(max_length=100, verbose_name='Nom')),
                ('slug', models.SlugField(unique=True, verbose_name='Slug')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('image', models.ImageField(blank=True, upload_to='categories/', verbose_name='Image')),
                ('is_active', models.BooleanField(default=True, verbose_name='Actif')),
                ('order', models.PositiveIntegerField(default=0, verbose_name="Ordre d'affichage")),
            ],
            options={
                'verbose_name': 'Catégorie',
                'verbose_name_plural': 'Catégories',
                'ordering': ['order', 'name'],
            },
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Date de modification')),
                ('name', models.CharField(max_length=100, verbose_name='Nom complet')),
                ('email', models.EmailField(max_length=254, verbose_name='Adresse email')),
                ('subject', models.CharField(max_length=200, verbose_name='Sujet')),
                ('message', models.TextField(verbose_name='Message')),
                ('phone', models.CharField(blank=True, max_length=20, validators=[django.core.validators.RegexValidator(message="Le numéro de téléphone doit être au format: '+999999999'. Jusqu'à 15 chiffres autorisés.", regex='^\\+?1?\\d{9,15}$')], verbose_name='Téléphone')),
                ('country', django_countries.fields.CountryField(blank=True, max_length=2, verbose_name='Pays')),
                ('city', models.CharField(blank=True, max_length=100, verbose_name='Ville')),
                ('address', models.TextField(blank=True, verbose_name='Adresse complète')),
                ('is_read', models.BooleanField(default=False, verbose_name='Message lu')),
                ('response', models.TextField(blank=True, verbose_name='Réponse')),
            ],
            options={
                'verbose_name': 'Message de contact',
                'verbose_name_plural': 'Messages de contact',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Newsletter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Date de modification')),
                ('title', models.CharField(max_length=200, verbose_name='Titre')),
                ('content', models.TextField(verbose_name='Contenu')),
                ('is_sent', models.BooleanField(default=False, verbose_name='Newsletter envoyée')),
                ('sent_at', models.DateTimeField(blank=True, null=True, verbose_name='Date d\'envoi')),
                ('subscribers_count', models.PositiveIntegerField(default=0, verbose_name='Nombre d\'abonnés')),
            ],
            options={
                'verbose_name': 'Newsletter',
                'verbose_name_plural': 'Newsletters',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='SiteSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Date de modification')),
                ('site_name', models.CharField(default='RevueMaroc', max_length=100, verbose_name='Nom du site')),
                ('site_description', models.TextField(blank=True, verbose_name='Description du site')),
                ('contact_email', models.EmailField(blank=True, max_length=254, verbose_name='Email de contact')),
                ('contact_phone', models.CharField(blank=True, max_length=20, verbose_name='Téléphone de contact')),
                ('address', models.TextField(blank=True, verbose_name='Adresse')),
                ('facebook_url', models.URLField(blank=True, verbose_name='URL Facebook')),
                ('twitter_url', models.URLField(blank=True, verbose_name='URL Twitter')),
                ('linkedin_url', models.URLField(blank=True, verbose_name='URL LinkedIn')),
                ('instagram_url', models.URLField(blank=True, verbose_name='URL Instagram')),
                ('logo', models.ImageField(blank=True, upload_to='site/', verbose_name='Logo du site')),
                ('favicon', models.ImageField(blank=True, upload_to='site/', verbose_name='Favicon')),
                ('monthly_price', models.DecimalField(decimal_places=2, default=9.99, max_digits=10, verbose_name='Prix mensuel (€)')),
                ('yearly_price', models.DecimalField(decimal_places=2, default=99.99, max_digits=10, verbose_name='Prix annuel (€)')),
                ('shipping_cost', models.DecimalField(decimal_places=2, default=5.99, max_digits=10, verbose_name='Frais de livraison (€)')),
                ('free_shipping_threshold', models.DecimalField(decimal_places=2, default=50.0, max_digits=10, verbose_name='Seuil livraison gratuite (€)')),
            ],
            options={
                'verbose_name': 'Paramètre du site',
                'verbose_name_plural': 'Paramètres du site',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Date de modification')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Nom')),
                ('slug', models.SlugField(unique=True, verbose_name='Slug')),
                ('color', models.CharField(default='#007bff', max_length=7, verbose_name='Couleur')),
            ],
            options={
                'verbose_name': 'Tag',
                'verbose_name_plural': 'Tags',
                'ordering': ['name'],
            },
        ),
    ]
