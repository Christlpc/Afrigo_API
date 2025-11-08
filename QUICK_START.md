# Quick Start - Backend Django AfriGo

## Installation rapide

### 1. Créer l'environnement virtuel

```bash
cd backend-django
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 2. Installer les dépendances

```bash
pip install -r requirements.txt
```

**Note** : Sur certains systèmes, GDAL peut nécessiter une installation système supplémentaire.

### 3. Configurer l'environnement

Créer un fichier `.env` :

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DB_NAME=afrigo_db
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432
```

### 4. Préparer la base de données

```bash
# Activer PostGIS dans PostgreSQL
psql -U postgres -d afrigo_db -c "CREATE EXTENSION IF NOT EXISTS postgis;"

# Créer les migrations
python manage.py makemigrations

# Appliquer les migrations
python manage.py migrate
```

### 5. Créer un superutilisateur

```bash
python manage.py createsuperuser
```

### 6. Lancer le serveur

```bash
python manage.py runserver
```

## Test de l'API

### Inscription

```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "client@example.com",
    "phone": "+237612345678",
    "password": "password123",
    "password_confirm": "password123",
    "userType": "client",
    "firstName": "Jean",
    "lastName": "Dupont"
  }'
```

### Connexion

```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "client@example.com",
    "password": "password123"
  }'
```

### Créer une adresse

```bash
curl -X POST http://localhost:8000/api/addresses/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "fullAddress": "123 Rue de la République, Douala",
    "latitude": 4.0511,
    "longitude": 9.7679,
    "addressLabel": "Maison",
    "city": "Douala"
  }'
```

### Créer une route

```bash
curl -X POST http://localhost:8000/api/routes/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "pickupAddressId": 1,
    "dropoffAddressId": 2,
    "pickupLatitude": 4.0511,
    "pickupLongitude": 9.7679,
    "dropoffLatitude": 4.0611,
    "dropoffLongitude": 9.7779,
    "routeType": "taxi"
  }'
```

## Admin Panel

Accéder à l'interface d'administration :

```
http://localhost:8000/admin/
```

Utiliser les identifiants du superutilisateur créé.

## Problèmes courants

### GDAL non trouvé

Sur Ubuntu/Debian :
```bash
sudo apt-get install gdal-bin libgdal-dev
```

Sur macOS :
```bash
brew install gdal
```

### PostGIS non activé

```bash
psql -U postgres -d afrigo_db -c "CREATE EXTENSION IF NOT EXISTS postgis;"
```

### Migrations en conflit

```bash
python manage.py makemigrations --merge
python manage.py migrate
```

## Prochaines étapes

1. ✅ Tester l'API localement
2. ✅ Configurer les variables d'environnement pour la production
3. ✅ Déployer sur Render
4. ✅ Configurer le domaine personnalisé

