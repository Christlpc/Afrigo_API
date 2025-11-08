# Guide de migration Node.js → Django

## Pourquoi migrer vers Django ?

1. **Déploiement plus simple** - Pas de compilation TypeScript
2. **ORM intégré** - Gestion automatique de la base de données
3. **Admin panel** - Interface d'administration automatique
4. **PostGIS natif** - Support géospatial intégré
5. **Sécurité** - Protection intégrée contre les vulnérabilités courantes

## Étape 1 : Installation

```bash
cd backend-django
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Étape 2 : Configuration

1. Copier `.env.example` vers `.env`
2. Configurer les variables d'environnement
3. S'assurer que PostgreSQL avec PostGIS est installé

## Étape 3 : Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

## Étape 4 : Créer un superutilisateur

```bash
python manage.py createsuperuser
```

## Étape 5 : Tester

```bash
python manage.py runserver
```

Visiter `http://localhost:8000/api/health/`

## Étape 6 : Déploiement

1. Configurer Render avec les variables d'environnement
2. Build Command : `pip install -r requirements.txt && python manage.py migrate`
3. Start Command : `gunicorn afrigo.wsgi:application`

## Différences principales

### Node.js/TypeScript
- Compilation requise
- Requêtes SQL manuelles
- Gestion manuelle des erreurs
- Pas d'interface d'administration

### Django
- Pas de compilation
- ORM automatique
- Gestion d'erreurs intégrée
- Admin panel automatique

## Migration des données

Si vous avez des données existantes :

1. Les tables existent déjà dans PostgreSQL
2. Les modèles Django utilisent les mêmes noms de tables
3. Les migrations Django créeront les champs manquants
4. Pour migrer les données, utilisez des scripts de migration personnalisés

## Prochaines étapes

1. ✅ Tester localement
2. ✅ Configurer les migrations
3. ✅ Créer un superutilisateur
4. ✅ Déployer sur Render
5. ✅ Configurer les variables d'environnement

## Support

En cas de problème, consultez la documentation Django : https://docs.djangoproject.com/

