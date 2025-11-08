# Corrections pour le déploiement Render

## Problèmes corrigés

1. **Pillow 10.1.0 incompatible avec Python 3.13** → Mise à jour vers Pillow 10.4.0
2. **GDAL nécessite compilation native** → Retiré de requirements.txt (sera géré par Render si nécessaire)
3. **Python 3.13 utilisé par défaut** → Spécification de Python 3.11.9 dans runtime.txt

## Modifications apportées

### 1. requirements.txt
- Pillow mis à jour vers 10.4.0 (compatible avec Python 3.11)
- GDAL retiré (sera installé via le système si nécessaire sur Render)

### 2. runtime.txt
- Ajout de `python-3.11.9` pour forcer Python 3.11

### 3. render.yaml
- Build command mis à jour avec `--upgrade pip`
- Ajout de `--noinput` pour les migrations et collectstatic
- Start command avec bind sur `0.0.0.0:$PORT`

### 4. settings.py
- Gestion conditionnelle de PostGIS (ne bloque pas si GDAL n'est pas disponible)

## Instructions de déploiement

1. **Dans Render Dashboard**, configurez :
   - **Build Command** : `pip install --upgrade pip && pip install -r requirements.txt && python manage.py migrate --noinput && python manage.py collectstatic --noinput`
   - **Start Command** : `gunicorn afrigo.wsgi:application --bind 0.0.0.0:$PORT`
   - **Python Version** : `3.11.9` (ou utilisez runtime.txt)

2. **Variables d'environnement** :
   - `SECRET_KEY` : Clé secrète Django
   - `DEBUG` : `False`
   - `ALLOWED_HOSTS` : Votre domaine Render
   - `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT` : Configuration PostgreSQL
   - `CORS_ALLOWED_ORIGINS` : Origines autorisées pour CORS

3. **Base de données PostgreSQL** :
   - Assurez-vous que PostGIS est activé : `CREATE EXTENSION IF NOT EXISTS postgis;`

## Si PostGIS n'est pas disponible

Si vous obtenez une erreur concernant PostGIS, vous pouvez temporairement utiliser PostgreSQL standard en modifiant `settings.py` :

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',  # Au lieu de postgis
        # ...
    }
}
```

Et retirer `'django.contrib.gis'` de `INSTALLED_APPS`.

## Vérification

Après le déploiement, vérifiez :
1. `/api/health/` devrait retourner `{"status": "OK"}`
2. `/admin/` devrait afficher l'interface d'administration
3. Les logs ne devraient pas afficher d'erreurs GDAL/PostGIS

