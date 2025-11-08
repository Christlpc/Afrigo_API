# AfriGo Backend - Django

Backend Django pour l'application VTC AfriGo.

## Installation

1. Créer un environnement virtuel :
```bash
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
```

2. Installer les dépendances :
```bash
pip install -r requirements.txt
```

3. Configurer les variables d'environnement :
Créer un fichier `.env` :
```
SECRET_KEY=your-secret-key
DEBUG=True
DB_NAME=afrigo_db
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432
```

4. Appliquer les migrations :
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Créer un superutilisateur :
```bash
python manage.py createsuperuser
```

6. Lancer le serveur :
```bash
python manage.py runserver
```

## Structure

- `apps/accounts/` - Authentification et gestion des utilisateurs
- `apps/routes/` - Gestion des commandes de taxi
- `apps/wallet/` - Gestion du portefeuille
- `apps/addresses/` - Gestion des adresses avec PostGIS
- `apps/core/` - Utilitaires communs

## API Endpoints

- `/api/auth/register/` - Inscription
- `/api/auth/login/` - Connexion
- `/api/auth/profile/` - Profil utilisateur
- `/api/routes/` - Liste et création de routes
- `/api/routes/<id>/` - Détails d'une route
- `/api/routes/<id>/cancel/` - Annuler une route
- `/api/routes/<id>/pay-wallet/` - Payer avec le wallet
- `/api/wallet/balance/` - Solde du wallet
- `/api/wallet/recharge/` - Recharger le wallet
- `/api/wallet/transactions/` - Historique des transactions
- `/api/addresses/` - Liste et création d'adresses
- `/api/addresses/<id>/favorite/` - Marquer comme favorite

## Déploiement sur Render

1. Configurer les variables d'environnement dans Render
2. Build Command : `pip install -r requirements.txt && python manage.py migrate`
3. Start Command : `gunicorn afrigo.wsgi:application`

## Documentation

Voir `API_DOCUMENTATION.md` pour la documentation complète de l'API.

