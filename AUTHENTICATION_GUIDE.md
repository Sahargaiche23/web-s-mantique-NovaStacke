# 🔐 Guide d'Authentification EcoTravel

## Vue d'ensemble

Le système d'authentification EcoTravel offre une gestion complète des utilisateurs avec :
- ✅ Inscription et connexion sécurisées
- 👑 Gestion des rôles (Voyageur / Admin)
- 🎯 Suivi des activités utilisateur
- 📊 Dashboard administrateur complet
- 🔒 Authentification JWT

---

## 🚀 Installation et Configuration

### 1. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 2. Configurer les variables d'environnement

Créez un fichier `.env` à la racine du projet (copiez depuis `.env.example`) :

```bash
cp .env.example .env
```

Modifiez le fichier `.env` avec vos propres valeurs :

```env
# Sécurité (IMPORTANT: Changez ces valeurs en production!)
SECRET_KEY=votre-cle-secrete-tres-longue-et-aleatoire
JWT_SECRET_KEY=votre-cle-jwt-tres-longue-et-aleatoire

# Base de données
DATABASE_URI=sqlite:///database.db
```

**⚠️ IMPORTANT:** En production, utilisez des clés secrètes fortes et aléatoires !

### 3. Initialiser la base de données

```bash
python init_auth.py
```

Choisissez l'option **1** pour l'initialisation complète.

Le script va créer :
- Les tables de base de données
- Un compte administrateur par défaut
- (Optionnel) Des comptes de test

---

## 👥 Types d'Utilisateurs

### 🧳 Voyageur (Role: `voyageur`)

**Accès :**
- Interface principale EcoTravel
- Recommandations personnalisées
- Recherche dans l'ontologie
- Requêtes SPARQL
- Chatbot IA
- Visualisations

**Restrictions :**
- Pas d'accès au panneau d'administration

### 👑 Administrateur (Role: `admin`)

**Accès à tout ce que le voyageur a, PLUS :**
- 🖥️ Dashboard administrateur complet
- 👥 Gestion CRUD des utilisateurs
- 📊 Analytics et statistiques
- 📈 Historique des activités
- 🎯 Suivi des recommandations

---

## 🌐 Pages Web

### Pages Publiques

#### **Login** (`login.html`)
- Connexion utilisateur
- Redirection automatique selon le rôle
- Compte démo disponible

#### **Register** (`register.html`)
- Inscription nouveaux utilisateurs
- Création automatique de compte "voyageur"
- Validation des données

### Pages Privées

#### **Interface Voyageur** (`index.html`)
- Accessible après connexion
- Dashboard écologique
- Toutes les fonctionnalités de base

#### **Admin Dashboard** (`admin.html`)
- **Réservé aux administrateurs uniquement**
- Gestion complète des utilisateurs
- Analytics en temps réel

---

## 🖥️ Admin Dashboard - Fonctionnalités

### 📊 Tab Dashboard

**Vue Globale :**
- 📈 Nombre total d'utilisateurs
- 💻 Requêtes SPARQL exécutées
- 🎯 Recommandations générées
- 🏖️ Top destinations consultées

**Graphiques Interactifs :**
- Répartition des utilisateurs par rôle (Doughnut Chart)
- Activité quotidienne sur 7 jours (Line Chart)
- Score écologique moyen global

### 👥 Tab Gestion des Utilisateurs

**CRUD Complet :**
- ➕ Créer un nouvel utilisateur
- ✏️ Modifier les informations (username, email, rôle, statut)
- 🗑️ Supprimer un utilisateur
- 👁️ Voir les détails et statistiques

**Filtrage Avancé :**
- 🔍 Recherche textuelle (username, email)
- 📂 Filtrage par rôle (voyageur/admin)
- ✅ Filtrage par statut (actif/inactif)

**Historique Complet :**
- Toutes les actions utilisateur
- Connexions
- Requêtes SPARQL
- Recommandations générées

### 📈 Tab Activités

**Suivi en temps réel :**
- Toutes les activités de la plateforme
- Filtrage par type d'activité
- Filtrage par date
- Visualisation chronologique

**Types d'activités trackées :**
- 🔐 Connexions
- 💻 Requêtes SPARQL
- 🔍 Recherches
- 🎯 Recommandations
- 📝 Inscriptions

### 🎯 Tab Recommandations

**Analytics des recommandations :**
- Statistiques par type (destinations, hébergements, activités, transports)
- Score écologique moyen
- Historique complet
- Données utilisateur associées

---

## 🔌 API Endpoints

### Authentification

```
POST /api/auth/register
```
Inscription d'un nouvel utilisateur

**Body:**
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "password123",
  "role": "voyageur"
}
```

**Response:**
```json
{
  "success": true,
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "role": "voyageur",
    "created_at": "2024-01-15T10:30:00"
  }
}
```

---

```
POST /api/auth/login
```
Connexion utilisateur

**Body:**
```json
{
  "username": "john_doe",
  "password": "password123"
}
```

**Response:**
```json
{
  "success": true,
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "username": "john_doe",
    "role": "voyageur"
  }
}
```

---

```
GET /api/auth/me
```
Récupérer les informations de l'utilisateur connecté

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:**
```json
{
  "success": true,
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "role": "voyageur",
    "is_active": true
  }
}
```

### Admin Routes (Nécessite rôle admin)

```
GET /api/admin/users
```
Liste tous les utilisateurs avec filtrage

**Query Parameters:**
- `search` - Recherche textuelle
- `role` - Filtrer par rôle
- `active_only` - Uniquement les actifs
- `page` - Numéro de page
- `per_page` - Résultats par page

---

```
GET /api/admin/users/<user_id>
```
Détails d'un utilisateur avec ses statistiques

---

```
POST /api/admin/users
```
Créer un nouvel utilisateur

---

```
PUT /api/admin/users/<user_id>
```
Modifier un utilisateur

---

```
DELETE /api/admin/users/<user_id>
```
Supprimer un utilisateur

---

```
GET /api/admin/dashboard/stats
```
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
  "top_destinations": [
    {"name": "Destination1", "views": 45}
  ],
  "daily_activity": [
    {"date": "2024-01-15", "count": 25}
  ]
}
```

---

## 💻 Utilisation dans le Frontend

### Stocker le token après connexion

```javascript
// Après une connexion réussie
localStorage.setItem('access_token', data.access_token);
localStorage.setItem('user', JSON.stringify(data.user));
```

### Envoyer des requêtes authentifiées

```javascript
function getAuthHeaders() {
    const token = localStorage.getItem('access_token');
    return {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
    };
}

// Exemple d'utilisation
fetch('/api/admin/users', {
    headers: getAuthHeaders()
})
.then(response => response.json())
.then(data => console.log(data));
```

### Vérifier le rôle utilisateur

```javascript
const user = JSON.parse(localStorage.getItem('user'));

if (user && user.role === 'admin') {
    // Afficher les fonctionnalités admin
}
```

### Déconnexion

```javascript
function logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
    window.location.href = 'login.html';
}
```

---

## 🔒 Sécurité

### Protection des routes

Le système utilise des décorateurs pour protéger les routes :

```python
@token_required
def protected_route(current_user_id):
    # Route accessible uniquement aux utilisateurs authentifiés
    pass

@admin_required
def admin_route(current_user_id, current_user):
    # Route accessible uniquement aux administrateurs
    pass
```

### Hachage des mots de passe

Les mots de passe sont hachés avec **bcrypt** :

```python
user.set_password('plain_password')  # Hash automatique
user.check_password('plain_password')  # Vérification
```

### JWT Tokens

- **Access Token**: Valide 24 heures
- **Refresh Token**: Valide 30 jours
- Stockés côté client dans localStorage

---

## 📊 Base de Données

### Tables

#### **users**
- `id` - ID unique
- `username` - Nom d'utilisateur (unique)
- `email` - Email (unique)
- `password_hash` - Mot de passe haché
- `role` - Rôle (voyageur/admin)
- `created_at` - Date de création
- `last_login` - Dernière connexion
- `is_active` - Statut du compte

#### **user_activities**
- `id` - ID unique
- `user_id` - Référence utilisateur
- `activity_type` - Type d'activité
- `activity_data` - Données JSON
- `timestamp` - Date/heure
- `ip_address` - Adresse IP

#### **recommendations**
- `id` - ID unique
- `user_id` - Référence utilisateur
- `recommendation_type` - Type
- `recommendation_data` - Données JSON
- `eco_score` - Score écologique
- `created_at` - Date de création

#### **destination_views**
- `id` - ID unique
- `user_id` - Référence utilisateur
- `destination_name` - Nom de la destination
- `view_count` - Nombre de vues
- `last_viewed` - Dernière consultation

---

## 🎯 Comptes par Défaut

Après initialisation avec `init_auth.py` :

### Admin
- **Username:** `admin`
- **Password:** `admin123`
- **Email:** `admin@ecotravel.com`
- **Rôle:** Admin

**⚠️ IMPORTANT:** Changez le mot de passe admin en production !

---

## 🐛 Dépannage

### Erreur: "Authentication required"
- Vérifiez que le token est bien stocké dans localStorage
- Vérifiez que le token n'est pas expiré (24h)
- Reconnectez-vous

### Erreur: "Admin access required"
- Vérifiez le rôle de l'utilisateur
- Seuls les utilisateurs avec `role=admin` peuvent accéder au dashboard admin

### Base de données corrompue
```bash
# Réinitialiser complètement
python init_auth.py
# Choisir option 3
```

---

## 📝 Logs d'Activité

Toutes les activités importantes sont enregistrées :

- Inscriptions
- Connexions/Déconnexions
- Créations/Modifications/Suppressions d'utilisateurs (par admin)
- Requêtes SPARQL
- Recherches
- Recommandations générées

Ces logs sont consultables dans l'interface admin.

---

## 🚀 Démarrage Rapide

```bash
# 1. Installer les dépendances
pip install -r requirements.txt

# 2. Initialiser la base de données
python init_auth.py

# 3. Démarrer le serveur
python backend/app.py

# 4. Ouvrir le navigateur
# - Interface utilisateur: http://localhost:5000
# - Connexion: http://localhost:5000/login.html
# - Admin: http://localhost:5000/admin.html
```

---

## 📚 Ressources Additionnelles

- **Flask-JWT-Extended**: https://flask-jwt-extended.readthedocs.io/
- **Flask-SQLAlchemy**: https://flask-sqlalchemy.palletsprojects.com/
- **Flask-Bcrypt**: https://flask-bcrypt.readthedocs.io/

---

## ✨ Fonctionnalités Futures Possibles

- [ ] Récupération de mot de passe par email
- [ ] Authentification à deux facteurs (2FA)
- [ ] Logs d'audit détaillés
- [ ] Export des données utilisateur (RGPD)
- [ ] Limitation du taux de requêtes (rate limiting)
- [ ] Sessions multiples par utilisateur
- [ ] OAuth2 (Google, Facebook, etc.)

---

**Développé avec ❤️ pour EcoTravel** 🌍
