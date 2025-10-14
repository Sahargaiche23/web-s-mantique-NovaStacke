# 🔐 Système d'Authentification EcoTravel - Guide Complet

## 📋 Table des Matières
1. [Vue d'ensemble](#vue-densemble)
2. [Installation Rapide](#installation-rapide)
3. [Architecture](#architecture)
4. [Fonctionnalités](#fonctionnalités)
5. [Interface Admin](#interface-admin)
6. [API Documentation](#api-documentation)
7. [Sécurité](#sécurité)

---

## 🎯 Vue d'ensemble

Le système d'authentification EcoTravel est une solution complète qui ajoute :

✅ **Gestion des utilisateurs** avec rôles (Voyageur/Admin)  
✅ **Authentification JWT** sécurisée  
✅ **Dashboard administrateur** avec analytics  
✅ **Suivi des activités** en temps réel  
✅ **Interface utilisateur moderne** avec Tailwind CSS  
✅ **API RESTful complète**  

**✨ Points Forts:**
- 🚀 Installation en 3 minutes
- 🎨 Interface moderne et responsive
- 📊 Analytics détaillées
- 🔒 Sécurité renforcée
- 📝 Logging complet des activités

---

## ⚡ Installation Rapide

### Méthode 1: Script Automatique (Recommandé)

```bash
# 1. Rendre le script exécutable (si ce n'est pas déjà fait)
chmod +x start_with_auth.sh

# 2. Lancer le script
./start_with_auth.sh
```

Le script va automatiquement :
- ✓ Vérifier les dépendances
- ✓ Installer les packages manquants
- ✓ Initialiser la base de données
- ✓ Créer un compte admin
- ✓ Démarrer le serveur

### Méthode 2: Installation Manuelle

```bash
# 1. Installer les dépendances
pip install -r requirements.txt

# 2. Configurer l'environnement
cp .env.example .env
# Éditez .env avec vos propres valeurs

# 3. Initialiser la base de données
python3 init_auth.py

# 4. Démarrer le serveur
python3 backend/app.py
```

### 3. Accéder à l'application

- 🌐 **Interface principale**: http://localhost:5000
- 🔐 **Connexion**: http://localhost:5000/login.html
- 👑 **Admin Dashboard**: http://localhost:5000/admin.html

**Compte admin par défaut:**
- Username: `admin`
- Password: `admin123`

⚠️ **Changez ce mot de passe en production!**

---

## 🏗️ Architecture

### Structure des Fichiers

```
web-s-mantique-NovaStacke-master/
│
├── backend/
│   ├── app.py                    # Application Flask principale (MODIFIÉ)
│   ├── models.py                 # Modèles de base de données (NOUVEAU)
│   ├── auth.py                   # Module d'authentification (NOUVEAU)
│   ├── admin_routes.py           # Routes admin (NOUVEAU)
│   ├── ontology_manager.py       # Gestion ontologie (EXISTANT)
│   ├── recommendation_engine.py  # Moteur de recommandation (EXISTANT)
│   └── ...
│
├── frontend/
│   ├── index.html               # Interface principale (MODIFIÉ)
│   ├── login.html               # Page de connexion (NOUVEAU)
│   ├── register.html            # Page d'inscription (NOUVEAU)
│   ├── admin.html               # Dashboard admin (NOUVEAU)
│   └── js/
│       ├── app.js               # JavaScript principal (MODIFIÉ)
│       └── admin.js             # JavaScript admin (NOUVEAU)
│
├── init_auth.py                 # Script d'initialisation (NOUVEAU)
├── start_with_auth.sh           # Script de démarrage (NOUVEAU)
├── database.db                  # Base de données SQLite (GÉNÉRÉ)
├── requirements.txt             # Dépendances (MODIFIÉ)
├── .env.example                 # Configuration exemple (MODIFIÉ)
├── AUTHENTICATION_GUIDE.md      # Guide détaillé (NOUVEAU)
└── README_AUTH.md               # Ce fichier (NOUVEAU)
```

### Technologies Utilisées

**Backend:**
- Flask (Framework web)
- Flask-SQLAlchemy (ORM)
- Flask-JWT-Extended (Authentification)
- Flask-Bcrypt (Hachage de mots de passe)
- SQLite (Base de données)

**Frontend:**
- HTML5 / CSS3
- Tailwind CSS (Framework CSS)
- JavaScript vanilla
- Chart.js (Graphiques)

---

## 🎨 Fonctionnalités

### 👤 Pour les Voyageurs

#### Interface Utilisateur
- ✅ Inscription simple et rapide
- ✅ Connexion sécurisée
- ✅ Accès à toutes les fonctionnalités existantes
- ✅ Menu utilisateur dans la navigation

#### Fonctionnalités Préservées
- 🔍 Recherche dans l'ontologie
- 💡 Recommandations personnalisées
- 💻 Requêtes SPARQL
- 📊 Visualisations
- 💬 Chatbot IA
- 🌍 Dashboard écologique

### 👑 Pour les Administrateurs

#### Dashboard Admin Complet

**📊 Onglet Dashboard:**
- Vue globale des statistiques
- Graphiques interactifs
- Top destinations consultées
- Métriques en temps réel

**👥 Onglet Gestion Utilisateurs:**
- Liste complète des utilisateurs
- Création / Modification / Suppression
- Filtrage avancé
- Historique des activités par utilisateur
- Statistiques individuelles

**📈 Onglet Activités:**
- Timeline des activités
- Filtrage par type et date
- Visualisation graphique
- Export possible

**🎯 Onglet Recommandations:**
- Statistiques des recommandations
- Filtrage par type
- Scores écologiques moyens
- Analyse des tendances

---

## 🖥️ Interface Admin

### Vue d'Ensemble du Dashboard

```
┌─────────────────────────────────────────────────────┐
│  🖥️ Admin Dashboard                      [Déconnexion]│
├─────────────────────────────────────────────────────┤
│  📊 Dashboard | 👥 Utilisateurs | 📈 Activités | 🎯 Reco│
├─────────────────────────────────────────────────────┤
│                                                       │
│  ┌───────┐  ┌───────┐  ┌───────┐  ┌───────┐        │
│  │ 25    │  │ 150   │  │ 45    │  │ 1250  │        │
│  │Users  │  │Queries│  │Recos  │  │Activ. │        │
│  └───────┘  └───────┘  └───────┘  └───────┘        │
│                                                       │
│  ┌──────────────────┐    ┌──────────────────┐      │
│  │  👥 Répartition  │    │  📈 Activité     │      │
│  │  [Doughnut]      │    │  [Line Chart]    │      │
│  └──────────────────┘    └──────────────────┘      │
│                                                       │
│  🏖️ Top Destinations:                               │
│  #1 Tunis (45 vues)    #2 Marrakech (38)...         │
└─────────────────────────────────────────────────────┘
```

### Gestion des Utilisateurs

**Tableau des utilisateurs:**
| ID | Username | Email | Rôle | Statut | Inscription | Actions |
|----|----------|-------|------|--------|-------------|---------|
| 1  | admin    | admin@... | 👑 Admin | ✅ Actif | 15/01/2024 | ✏️ 👁️ |
| 2  | voyageur1| user@...  | 🧳 Voyageur | ✅ Actif | 16/01/2024 | ✏️ 👁️ 🗑️ |

**Actions disponibles:**
- ✏️ **Modifier**: Changer username, email, rôle, statut, mot de passe
- 👁️ **Détails**: Voir statistiques complètes et historique
- 🗑️ **Supprimer**: Supprimer l'utilisateur (avec confirmation)

**Filtres:**
- 🔍 Recherche textuelle (username/email)
- 📂 Par rôle (voyageur/admin)
- ✅ Par statut (actif/inactif)

---

## 📡 API Documentation

### Authentification Endpoints

#### POST `/api/auth/register`
Créer un nouveau compte utilisateur

**Request:**
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "securepassword123"
}
```

**Response (201):**
```json
{
  "success": true,
  "message": "User registered successfully",
  "user": {
    "id": 3,
    "username": "john_doe",
    "email": "john@example.com",
    "role": "voyageur",
    "created_at": "2024-01-15T10:30:00"
  }
}
```

#### POST `/api/auth/login`
Se connecter

**Request:**
```json
{
  "username": "john_doe",
  "password": "securepassword123"
}
```

**Response (200):**
```json
{
  "success": true,
  "access_token": "eyJ0eXAiOiJKV1Qi...",
  "refresh_token": "eyJ0eXAiOiJKV1Qi...",
  "user": {
    "id": 3,
    "username": "john_doe",
    "role": "voyageur"
  }
}
```

#### GET `/api/auth/me`
Récupérer les informations de l'utilisateur connecté

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200):**
```json
{
  "success": true,
  "user": {
    "id": 3,
    "username": "john_doe",
    "email": "john@example.com",
    "role": "voyageur",
    "is_active": true
  }
}
```

### Admin Endpoints (Requiert rôle admin)

#### GET `/api/admin/users`
Liste tous les utilisateurs

**Query Parameters:**
- `search` - Recherche textuelle
- `role` - Filtrer par rôle (voyageur/admin)
- `active_only` - true/false
- `page` - Numéro de page (défaut: 1)
- `per_page` - Résultats par page (défaut: 50)

#### GET `/api/admin/users/<user_id>`
Détails d'un utilisateur avec statistiques

#### POST `/api/admin/users`
Créer un utilisateur (admin uniquement)

#### PUT `/api/admin/users/<user_id>`
Modifier un utilisateur

#### DELETE `/api/admin/users/<user_id>`
Supprimer un utilisateur

#### GET `/api/admin/dashboard/stats`
Statistiques complètes du dashboard

**Response:**
```json
{
  "success": true,
  "users": {
    "total": 25,
    "active": 23,
    "admins": 2,
    "voyageurs": 23,
    "new_last_30d": 5
  },
  "activities": {
    "total": 1250,
    "logins": 450,
    "sparql_queries": 600,
    "searches": 200
  },
  "recommendations": {
    "total": 180,
    "avg_eco_score": 78.5
  },
  "top_destinations": [...],
  "daily_activity": [...]
}
```

---

## 🔒 Sécurité

### Mesures de Sécurité Implémentées

1. **Hachage des mots de passe**
   - Utilisation de Bcrypt
   - Salt automatique
   - Jamais de stockage en clair

2. **Tokens JWT**
   - Access Token: 24h
   - Refresh Token: 30 jours
   - Signature cryptographique

3. **Protection des routes**
   - Décorateurs `@token_required`
   - Décorateurs `@admin_required`
   - Vérification automatique

4. **Validation des données**
   - Validation côté serveur
   - Vérification unicité email/username
   - Longueur minimale des mots de passe

5. **CORS configuré**
   - Origins autorisées définies
   - Headers sécurisés

### Bonnes Pratiques

**En Production:**

1. **Changez les clés secrètes:**
```env
SECRET_KEY=utilisez-une-cle-tres-longue-et-aleatoire-ici
JWT_SECRET_KEY=utilisez-une-autre-cle-tres-longue-ici
```

Générez des clés aléatoires:
```python
import secrets
print(secrets.token_hex(32))
```

2. **Utilisez HTTPS**
3. **Changez le mot de passe admin par défaut**
4. **Activez les logs de sécurité**
5. **Limitez les tentatives de connexion**

---

## 📊 Base de Données

### Schéma

```sql
-- Table users
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'voyageur',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_login DATETIME,
    is_active BOOLEAN DEFAULT 1
);

-- Table user_activities
CREATE TABLE user_activities (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    activity_type VARCHAR(50) NOT NULL,
    activity_data TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    ip_address VARCHAR(50),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Table recommendations
CREATE TABLE recommendations (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    recommendation_type VARCHAR(50),
    recommendation_data TEXT,
    eco_score FLOAT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Table destination_views
CREATE TABLE destination_views (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    destination_name VARCHAR(200),
    view_count INTEGER DEFAULT 1,
    last_viewed DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

---

## 🛠️ Commandes Utiles

### Gestion de la Base de Données

```bash
# Initialiser/Réinitialiser
python3 init_auth.py

# Options disponibles:
# 1. Initialiser la base de données
# 2. Créer un nouvel administrateur
# 3. Réinitialiser la base de données (DANGER!)
# 4. Afficher les statistiques
```

### Gestion des Utilisateurs (via Python)

```python
from backend.models import db, User
from backend.app import app

with app.app_context():
    # Créer un utilisateur
    user = User(username='test', email='test@test.com', role='voyageur')
    user.set_password('password123')
    db.session.add(user)
    db.session.commit()
    
    # Lister tous les utilisateurs
    users = User.query.all()
    for u in users:
        print(f"{u.username} - {u.role}")
    
    # Changer le rôle
    user = User.query.filter_by(username='test').first()
    user.role = 'admin'
    db.session.commit()
```

---

## 🐛 Dépannage

### Problème: "Module not found"
**Solution:**
```bash
pip install -r requirements.txt
```

### Problème: "Database locked"
**Solution:**
```bash
# Arrêter tous les processus Python
# Supprimer database.db
rm database.db
# Réinitialiser
python3 init_auth.py
```

### Problème: "Authentication failed"
**Solution:**
1. Vérifier que le token est dans localStorage
2. Vérifier que le token n'est pas expiré
3. Reconnecter l'utilisateur

### Problème: "Admin access denied"
**Solution:**
Vérifier le rôle de l'utilisateur dans la base:
```python
from backend.models import User
from backend.app import app

with app.app_context():
    user = User.query.filter_by(username='votre_username').first()
    print(f"Role: {user.role}")
    # Si nécessaire, changer le rôle:
    user.role = 'admin'
    db.session.commit()
```

---

## 📝 Notes de Version

### Version 1.0.0 (Actuelle)

**Fonctionnalités:**
- ✅ Système d'authentification complet
- ✅ Gestion des rôles (voyageur/admin)
- ✅ Dashboard administrateur
- ✅ Suivi des activités
- ✅ API RESTful
- ✅ Interface moderne

**Non inclus (futures versions):**
- ⏳ Récupération de mot de passe par email
- ⏳ Authentification à deux facteurs (2FA)
- ⏳ OAuth2 (Google, Facebook)
- ⏳ Rate limiting
- ⏳ Export de données (RGPD)

---

## 🤝 Support

Pour toute question ou problème:

1. Consultez `AUTHENTICATION_GUIDE.md` pour plus de détails
2. Vérifiez les logs du serveur
3. Consultez la documentation Flask-JWT-Extended

---

## 📄 Licence

Ce système d'authentification est fourni en complément du projet EcoTravel.

---

**🌍 Développé pour EcoTravel - Voyage Sémantique Écologique**

Bon voyage dans le monde de l'authentification sécurisée! 🚀
