# Guide de migration vers Django

## Avantages de Django

✅ **Pas de compilation TypeScript** - Déploiement plus simple
✅ **ORM intégré** - Gestion automatique de la base de données
✅ **Admin panel** - Interface d'administration automatique
✅ **PostGIS natif** - Support géospatial intégré
✅ **Sécurité** - Protection CSRF, XSS intégrée
✅ **Scalabilité** - Architecture solide et éprouvée

## Migration des données

Si vous avez déjà des données dans PostgreSQL :

1. Les modèles Django utilisent les mêmes noms de tables
2. Les migrations Django créeront les tables si elles n'existent pas
3. Pour migrer les données existantes, utilisez `python manage.py loaddata`

## Déploiement

### Render

1. **Build Command** :
```bash
pip install -r requirements.txt && python manage.py migrate
```

2. **Start Command** :
```bash
gunicorn afrigo.wsgi:application
```

3. **Variables d'environnement** :
```
SECRET_KEY=your-secret-key
DEBUG=False
DB_NAME=afrigo_db
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=your-host
DB_PORT=5432
ALLOWED_HOSTS=your-domain.com
```

## Différences avec Node.js

1. **Pas de compilation** - Python est interprété directement
2. **ORM au lieu de requêtes SQL** - Plus sûr et plus maintenable
3. **Admin panel** - Interface d'administration automatique
4. **Migrations** - Gestion automatique des changements de schéma

## Prochaines étapes

1. Tester localement
2. Configurer les migrations
3. Créer un superutilisateur
4. Déployer sur Render
5. Configurer les variables d'environnement

