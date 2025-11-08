# Instructions de déploiement Render

## ⚠️ IMPORTANT : Structure du dépôt

Le code Django est dans le dossier `backend-django/`. 

### Si Render clone depuis la racine du dépôt

Vous devez configurer dans Render Dashboard :

1. **Root Directory** : `backend-django`
2. **Build Command** : 
   ```bash
   pip install --upgrade pip && pip install -r requirements.txt && python manage.py migrate --noinput && python manage.py collectstatic --noinput
   ```
3. **Start Command** : 
   ```bash
   gunicorn afrigo.wsgi:application --bind 0.0.0.0:$PORT
   ```

### Ou déplacer le code à la racine

Si vous préférez avoir le code à la racine du dépôt, déplacez tous les fichiers de `backend-django/` vers la racine.

## Configuration Render

### Variables d'environnement requises

- `SECRET_KEY` : Clé secrète Django (générez une clé aléatoire)
- `DEBUG` : `False` (pour la production)
- `ALLOWED_HOSTS` : Votre domaine Render (ex: `afrigo-backend.onrender.com`)
- `DB_NAME` : Nom de la base de données PostgreSQL
- `DB_USER` : Utilisateur PostgreSQL
- `DB_PASSWORD` : Mot de passe PostgreSQL
- `DB_HOST` : Host PostgreSQL (fourni par Render)
- `DB_PORT` : `5432`
- `CORS_ALLOWED_ORIGINS` : Origines autorisées (ex: `https://votre-frontend.com`)

### Base de données PostgreSQL

Assurez-vous que PostGIS est activé :

```sql
CREATE EXTENSION IF NOT EXISTS postgis;
```

## Vérification

Après le déploiement :

1. Vérifiez `/api/health/` → devrait retourner `{"status": "OK"}`
2. Vérifiez `/admin/` → interface d'administration Django
3. Testez l'API avec Postman ou curl

## Problèmes courants

### Erreur : "Module not found: GDAL"

Si vous obtenez une erreur GDAL, c'est que PostGIS nécessite GDAL. Sur Render, GDAL devrait être disponible via le système. Si ce n'est pas le cas, contactez le support Render.

### Erreur : "Pillow installation failed"

Assurez-vous que Python 3.11.9 est utilisé (vérifié dans `runtime.txt`).

### Erreur : "Database connection failed"

Vérifiez que les variables d'environnement de la base de données sont correctement configurées dans Render Dashboard.

