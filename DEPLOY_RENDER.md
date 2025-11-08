# Déploiement sur Render - Django

## Configuration Render

### 1. Variables d'environnement

Dans le dashboard Render, configurez :

```
SECRET_KEY=<générer-une-clé-secrète>
DEBUG=False
ALLOWED_HOSTS=votre-domaine.render.com
DB_NAME=afrigo_db
DB_USER=postgres
DB_PASSWORD=<mot-de-passe-postgres>
DB_HOST=<host-postgres-render>
DB_PORT=5432
CORS_ALLOWED_ORIGINS=https://votre-frontend.com
```

### 2. Commandes de build

- **Build Command** : 
```bash
pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput
```

- **Start Command** :
```bash
gunicorn afrigo.wsgi:application
```

### 3. PostGIS

Assurez-vous que PostGIS est activé sur votre base de données PostgreSQL :

```sql
CREATE EXTENSION IF NOT EXISTS "postgis";
```

### 4. Migrations

Les migrations s'exécutent automatiquement lors du build. Si nécessaire, exécutez manuellement :

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Superutilisateur

Pour créer un superutilisateur, utilisez le shell Render ou exécutez :

```bash
python manage.py createsuperuser
```

## Avantages du déploiement Django

✅ Pas de compilation TypeScript
✅ Migrations automatiques
✅ Admin panel accessible
✅ Gestion des erreurs simplifiée
✅ Logs intégrés

## Vérification

Après le déploiement :

1. Vérifiez `/api/health/` - devrait retourner `{"status": "OK"}`
2. Vérifiez `/admin/` - interface d'administration
3. Testez l'API avec Postman ou curl

## Support

En cas de problème, vérifiez les logs dans Render Dashboard.

