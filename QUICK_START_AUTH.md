# ⚡ Guide de Démarrage Rapide - Authentification EcoTravel

## 🚀 Installation en 3 Minutes

### Étape 1: Installation des Dépendances (1 min)

```bash
cd /home/sahar/Bureau/web-s-mantique-NovaStacke-master
pip install -r requirements.txt
```

**Nouvelles dépendances installées:**
- Flask-SQLAlchemy (Base de données)
- Flask-JWT-Extended (Tokens)
- Flask-Bcrypt (Hachage)
- PyJWT (JWT)

---

### Étape 2: Initialisation de la Base de Données (1 min)

```bash
python3 init_auth.py
```

**Dans le menu, choisissez l'option 1**

Le script va vous demander:
1. Nom d'utilisateur admin (défaut: `admin`)
2. Email admin (défaut: `admin@ecotravel.com`)
3. Mot de passe (minimum 6 caractères)
4. Confirmation du mot de passe

**Ou utilisez les valeurs par défaut** en appuyant sur Entrée.

---

### Étape 3: Démarrer le Serveur (1 min)

```bash
python3 backend/app.py
```

**Ou utilisez le script automatique:**
```bash
./start_with_auth.sh
```

✅ **Terminé!** L'application est maintenant accessible.

---

## 🌐 Accès aux Interfaces

### Interface Principale
```
http://localhost:5000
```
→ Dashboard écologique EcoTravel

### Page de Connexion
```
http://localhost:5000/login.html
```
→ Connexion utilisateur

### Page d'Inscription
```
http://localhost:5000/register.html
```
→ Créer un compte voyageur

### Dashboard Admin
```
http://localhost:5000/admin.html
```
→ Interface d'administration (admin uniquement)

---

## 👤 Comptes de Test

### Administrateur (Accès Complet)
```
Username: admin
Password: admin123
```

**Accès à:**
- ✅ Toutes les fonctionnalités voyageur
- ✅ Dashboard administrateur
- ✅ Gestion des utilisateurs
- ✅ Analytics et statistiques

### Créer un Compte Voyageur
1. Aller sur http://localhost:5000/register.html
2. Remplir le formulaire
3. Se connecter

---

## 🎯 Fonctionnalités Principales

### 🔐 Pour Tous les Utilisateurs

#### 1. Inscription
- Formulaire simple
- Validation automatique
- Confirmation par email (optionnel)

#### 2. Connexion
- Authentification sécurisée
- Token JWT (24h)
- Redirection automatique

#### 3. Navigation
- Menu utilisateur dans la navbar
- Déconnexion rapide
- Accès selon le rôle

---

### 🧳 Interface Voyageur

**Fonctionnalités Disponibles:**
- 🏠 Dashboard écologique
- 🔍 Recherche avancée
- 🎯 Recommandations IA
- 💻 Requêtes SPARQL
- 📊 Visualisations
- 🗣️ Chatbot IA

**Navigation:**
```
[🌍 EcoTravel]  Accueil | Recherche | Recommandations | SPARQL | Visualisations | Ontologie | Chat

                                                                    [👤 username] [Déconnexion]
```

---

### 👑 Dashboard Administrateur

**4 Onglets Principaux:**

#### 📊 Tab Dashboard
```
┌──────────────────────────────────────────┐
│  Total Users: 25    SPARQL Queries: 150  │
│  Recommendations: 45    Activities: 1250  │
├──────────────────────────────────────────┤
│  [Graphique Répartition] [Activité]      │
│  [Top Destinations]                       │
└──────────────────────────────────────────┘
```

**Affiche:**
- Statistiques globales en temps réel
- Graphiques interactifs (Chart.js)
- Top 10 destinations consultées
- Score écologique moyen

#### 👥 Tab Utilisateurs

**Gestion Complète:**
- ➕ Créer un utilisateur
- ✏️ Modifier (username, email, rôle, statut, password)
- 🗑️ Supprimer (avec confirmation)
- 👁️ Voir détails et statistiques

**Filtres:**
- 🔍 Recherche textuelle
- 📂 Par rôle (voyageur/admin)
- ✅ Par statut (actif/inactif)

**Tableau:**
```
| ID | Username  | Email         | Rôle     | Statut | Date       | Actions      |
|----|-----------|---------------|----------|--------|------------|--------------|
| 1  | admin     | admin@...     | Admin    | Actif  | 15/01/2024 | ✏️ 👁️       |
| 2  | voyageur1 | user@...      | Voyageur | Actif  | 16/01/2024 | ✏️ 👁️ 🗑️   |
```

#### 📈 Tab Activités

**Suivi en Temps Réel:**
- Toutes les actions utilisateurs
- Types: login, logout, queries, searches, recommendations
- Filtrage par type et date
- Visualisation chronologique

**Exemple:**
```
📅 15 Janvier 2024
  🔐 Connexion - 12 fois
  💻 Requête SPARQL - 8 fois
  🔍 Recherche - 5 fois
  🎯 Recommandation - 3 fois
```

#### 🎯 Tab Recommandations

**Analytics:**
- Nombre par type (destinations, hébergements, activités, transports)
- Score écologique moyen
- Historique complet
- Utilisateurs associés

---

## 🔄 Flux d'Utilisation

### Nouveau Utilisateur

```
1. Aller sur register.html
        ↓
2. Remplir le formulaire
        ↓
3. Cliquer "Créer mon compte"
        ↓
4. Redirection vers login.html
        ↓
5. Se connecter
        ↓
6. Accès à l'interface voyageur
```

### Utilisateur Existant

```
1. Aller sur login.html
        ↓
2. Entrer identifiants
        ↓
3. Cliquer "Se connecter"
        ↓
4. Si voyageur → index.html
   Si admin → admin.html
```

### Administrateur - Créer un Utilisateur

```
1. Se connecter comme admin
        ↓
2. Aller sur admin.html
        ↓
3. Tab "Utilisateurs"
        ↓
4. Cliquer "➕ Nouvel Utilisateur"
        ↓
5. Remplir le formulaire
        ↓
6. Enregistrer
```

---

## 🔧 Configuration Personnalisée

### Modifier les Clés Secrètes

Éditez le fichier `.env`:

```bash
nano .env
```

Changez ces lignes:
```env
SECRET_KEY=votre-nouvelle-cle-secrete-tres-longue
JWT_SECRET_KEY=votre-nouvelle-cle-jwt-tres-longue
```

**Générer des clés aléatoires:**
```python
import secrets
print(secrets.token_hex(32))
```

### Changer le Mot de Passe Admin

**Méthode 1: Via l'interface**
1. Connectez-vous comme admin
2. Allez dans admin.html → Utilisateurs
3. Modifiez l'utilisateur "admin"
4. Changez le mot de passe

**Méthode 2: Via Python**
```python
from backend.models import db, User
from backend.app import app

with app.app_context():
    admin = User.query.filter_by(username='admin').first()
    admin.set_password('nouveau_mot_de_passe')
    db.session.commit()
    print("✅ Mot de passe changé!")
```

---

## 📊 Commandes Utiles

### Voir les Statistiques

```bash
python3 init_auth.py
# Choisir option 4
```

**Affiche:**
- Nombre total d'utilisateurs
- Nombre d'admins / voyageurs
- Comptes actifs / inactifs
- Liste complète

### Réinitialiser la Base de Données

```bash
python3 init_auth.py
# Choisir option 3
# Taper "CONFIRMER"
```

⚠️ **ATTENTION:** Supprime toutes les données!

### Créer un Administrateur Supplémentaire

```bash
python3 init_auth.py
# Choisir option 2
```

---

## 🐛 Résolution Rapide de Problèmes

### Problème: "Module not found"

**Solution:**
```bash
pip install -r requirements.txt
```

### Problème: "Database is locked"

**Solution:**
```bash
# Arrêter le serveur (Ctrl+C)
rm database.db
python3 init_auth.py
```

### Problème: "Cannot access admin.html"

**Vérifiez le rôle:**
```python
from backend.models import User
from backend.app import app

with app.app_context():
    user = User.query.filter_by(username='votre_username').first()
    print(f"Rôle actuel: {user.role}")
    
    # Changer en admin si nécessaire
    user.role = 'admin'
    db.session.commit()
    print("✅ Rôle changé en admin")
```

### Problème: "Token expired"

**Solution:**
- Reconnectez-vous
- Les tokens expirent après 24h

### Problème: Port 5000 déjà utilisé

**Solution:**
```bash
# Trouver le processus
lsof -ti:5000

# Tuer le processus
kill -9 $(lsof -ti:5000)

# Ou changer le port dans app.py
app.run(debug=True, host='0.0.0.0', port=5001)
```

---

## 📱 Exemples d'Utilisation API

### Inscription via curl

```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "nouveau_user",
    "email": "user@example.com",
    "password": "password123"
  }'
```

### Connexion via curl

```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "admin123"
  }'
```

**Réponse:**
```json
{
  "success": true,
  "access_token": "eyJ0eXAiOiJKV1Qi...",
  "user": {
    "username": "admin",
    "role": "admin"
  }
}
```

### Requête authentifiée

```bash
# Récupérer le token de la réponse précédente
TOKEN="eyJ0eXAiOiJKV1Qi..."

curl -X GET http://localhost:5000/api/auth/me \
  -H "Authorization: Bearer $TOKEN"
```

### Liste des utilisateurs (admin)

```bash
curl -X GET "http://localhost:5000/api/admin/users?per_page=10" \
  -H "Authorization: Bearer $TOKEN"
```

---

## 📈 Métriques et Analytics

### Statistiques Disponibles

**Dashboard Admin:**
- 👥 Total utilisateurs
- 💻 Requêtes SPARQL exécutées
- 🎯 Recommandations générées
- 📊 Activités totales
- 🏖️ Top destinations
- 📈 Activité quotidienne (7 jours)
- 🌱 Score écologique moyen

**Par Utilisateur:**
- Nombre de connexions
- Requêtes SPARQL effectuées
- Recommandations demandées
- Dernière connexion
- Date d'inscription

---

## ✅ Checklist de Vérification

Après installation, vérifiez:

- [ ] Les dépendances sont installées
- [ ] La base de données est créée (database.db existe)
- [ ] Le compte admin fonctionne
- [ ] La page de connexion s'affiche
- [ ] La connexion admin fonctionne
- [ ] Le dashboard admin est accessible
- [ ] L'inscription d'un nouveau compte fonctionne
- [ ] Le nouveau compte peut se connecter
- [ ] Les fonctionnalités existantes fonctionnent toujours
- [ ] Le menu utilisateur s'affiche correctement

---

## 🎓 Apprentissage

### Pour les Développeurs

**Fichiers importants à étudier:**

1. **`backend/models.py`** - Structure de la base de données
2. **`backend/auth.py`** - Logique d'authentification
3. **`backend/admin_routes.py`** - Routes administrateur
4. **`frontend/js/admin.js`** - Interface admin
5. **`AUTHENTICATION_GUIDE.md`** - Documentation complète

### Concepts Clés

- **JWT (JSON Web Tokens)**: Tokens d'authentification
- **Bcrypt**: Hachage sécurisé des mots de passe
- **SQLAlchemy**: ORM pour la base de données
- **Décorateurs**: `@token_required`, `@admin_required`
- **RBAC**: Role-Based Access Control

---

## 🔗 Ressources Complémentaires

**Documentation Complète:**
- `AUTHENTICATION_GUIDE.md` - Guide détaillé avec API
- `README_AUTH.md` - Architecture et fonctionnalités
- `IMPLEMENTATION_SUMMARY.md` - Résumé technique

**Documentation Externe:**
- [Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io/)
- [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/)
- [Chart.js](https://www.chartjs.org/)

---

## 🎉 Vous êtes Prêt!

Votre application EcoTravel dispose maintenant de:

✅ **Authentification sécurisée**  
✅ **Gestion des utilisateurs**  
✅ **Dashboard administrateur professionnel**  
✅ **Suivi des activités**  
✅ **Analytics en temps réel**  

**Commencez à utiliser votre nouvelle plateforme!** 🚀

---

**Besoin d'aide?**
Consultez les autres guides ou vérifiez les logs du serveur.

**Bonne utilisation!** 🌍
