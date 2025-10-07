# 📑 Index du Projet EcoTravel

## 🎯 Démarrage Rapide

**Pour commencer immédiatement:**
1. Lire: [QUICK_START.md](QUICK_START.md) (3 minutes)
2. Exécuter: `./start.sh`
3. Ouvrir: http://localhost:5000

---

## 📚 Documentation

### Pour les Débutants
- **[QUICK_START.md](QUICK_START.md)** - Démarrage en 3 minutes
- **[INSTALLATION.md](INSTALLATION.md)** - Guide d'installation détaillé
- **[README.md](README.md)** - Vue d'ensemble du projet

### Pour les Utilisateurs
- **[GUIDE_UTILISATION.md](GUIDE_UTILISATION.md)** - Guide complet d'utilisation
  - Comment utiliser chaque interface
  - Exemples de requêtes SPARQL
  - Scénarios d'utilisation
  - Dépannage

### Pour les Développeurs
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Architecture technique
  - Structure du code
  - Flux de données
  - API endpoints
  - Extensibilité

### Synthèse
- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Résumé complet du projet
  - Fonctionnalités implémentées
  - Statistiques
  - Technologies utilisées

---

## 📁 Structure des Fichiers

### 📂 Racine
```
/home/sahar/CascadeProjects/eco_travel_semantic/
├── 📄 README.md                    # Documentation principale
├── 📄 QUICK_START.md               # Démarrage rapide
├── 📄 GUIDE_UTILISATION.md         # Guide utilisateur
├── 📄 ARCHITECTURE.md              # Documentation technique
├── 📄 PROJECT_SUMMARY.md           # Synthèse du projet
├── 📄 INSTALLATION.md              # Guide d'installation
├── 📄 INDEX.md                     # Ce fichier
├── 📄 requirements.txt             # Dépendances Python
├── 📄 .env.example                 # Configuration exemple
├── 📄 .gitignore                   # Fichiers ignorés
└── 🔧 start.sh                     # Script de démarrage
```

### 📂 Backend (Python/Flask)
```
backend/
├── 📄 app.py                       # Application Flask (24 routes API)
├── 📄 ontology_manager.py          # Gestionnaire RDF/OWL (rdflib)
├── 📄 sparql_queries.py            # 15 requêtes SPARQL complexes
├── 📄 recommendation_engine.py     # Système de recommandation IA
└── 📄 visualization_engine.py      # Moteur de visualisation
```

**Lignes de code:** ~2000 lignes Python

### 📂 Frontend (HTML/JS/CSS)
```
frontend/
├── 📄 index.html                   # Interface principale (6 pages)
├── js/
│   └── 📄 app.js                   # Logique JavaScript (500+ lignes)
└── css/
    └── 📄 style.css                # Styles personnalisés
```

**Lignes de code:** ~900 lignes HTML/JS/CSS

### 📂 Ontologie (RDF/OWL)
```
ontology/
├── 📄 ecotourisme.owl              # Ontologie principale
└── 📄 data_enriched.owl            # Données enrichies (30+ individus)
```

**Contenu:**
- 11 classes
- 7 propriétés d'objet
- 16 propriétés de données
- 30+ individus
- ~150 triplets RDF

---

## 🗺️ Navigation par Besoin

### "Je veux démarrer rapidement"
→ [QUICK_START.md](QUICK_START.md)

### "Je veux installer l'application"
→ [INSTALLATION.md](INSTALLATION.md)

### "Je veux apprendre à utiliser l'application"
→ [GUIDE_UTILISATION.md](GUIDE_UTILISATION.md)

### "Je veux comprendre l'architecture"
→ [ARCHITECTURE.md](ARCHITECTURE.md)

### "Je veux voir un résumé complet"
→ [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)

### "Je veux modifier le code"
→ [ARCHITECTURE.md](ARCHITECTURE.md) + Code source

### "J'ai un problème"
→ [GUIDE_UTILISATION.md](GUIDE_UTILISATION.md) section Dépannage

---

## 🎯 Fonctionnalités Principales

### 1. Ontologie RDF/OWL
**Fichiers:** `ontology/ecotourisme.owl`
- 11 classes (Destination, Hébergement, Transport, etc.)
- 30+ individus avec données réelles

### 2. API REST (24 endpoints)
**Fichier:** `backend/app.py`
- SPARQL (3 endpoints)
- Ontologie (6 endpoints)
- Recommandations (5 endpoints)
- Visualisations (5 endpoints)
- Avancé (3 endpoints)
- Système (2 endpoints)

### 3. Requêtes SPARQL (15+)
**Fichier:** `backend/sparql_queries.py`
- Hébergements écologiques
- Comparaison transports
- Analyse destinations
- Scores écologiques
- Et 11 autres...

### 4. Système de Recommandation IA
**Fichier:** `backend/recommendation_engine.py`
- Scoring multi-critères
- Calcul empreinte carbone
- Recommandations personnalisées
- Plan de voyage complet

### 5. Visualisations (6 types)
**Fichier:** `backend/visualization_engine.py`
- Graphiques en barres, ligne, radar, circulaire
- Graphe de réseau
- Analyses multidimensionnelles

### 6. Interfaces Web (6 pages)
**Fichiers:** `frontend/index.html`, `frontend/js/app.js`
- Accueil avec dashboard
- Recherche avancée
- Recommandations IA
- Éditeur SPARQL
- Visualisations
- Explorateur d'ontologie

---

## 🔍 Recherche Rapide

### Trouver une Fonctionnalité

**Recherche dans l'ontologie:**
- Classes → `ontology/ecotourisme.owl` lignes 200-350
- Propriétés → `ontology/ecotourisme.owl` lignes 30-200
- Individus → `ontology/ecotourisme.owl` lignes 350+

**Requêtes SPARQL:**
- Toutes les requêtes → `backend/sparql_queries.py`
- Requête spécifique → Rechercher `QUERY_N_` dans le fichier

**API Endpoints:**
- Toutes les routes → `backend/app.py` lignes 30+
- Route spécifique → Rechercher `@app.route`

**Interfaces:**
- HTML → `frontend/index.html`
- JavaScript → `frontend/js/app.js`
- Styles → `frontend/css/style.css`

---

## 📊 Statistiques du Projet

### Code
- **Python:** ~2000 lignes
- **JavaScript:** ~500 lignes
- **HTML/CSS:** ~400 lignes
- **Total:** ~2900 lignes

### Documentation
- **Fichiers:** 7 fichiers markdown
- **Lignes:** ~2000 lignes
- **Mots:** ~15000 mots

### Fichiers
- **Total:** 20 fichiers créés
- **Backend:** 5 fichiers Python
- **Frontend:** 3 fichiers (HTML/JS/CSS)
- **Ontologie:** 2 fichiers OWL
- **Documentation:** 7 fichiers MD
- **Configuration:** 3 fichiers

---

## 🚀 Commandes Utiles

### Démarrage
```bash
./start.sh                          # Démarrage automatique
cd backend && python app.py         # Démarrage manuel
```

### Tests
```bash
curl http://localhost:5000/api/health                    # Test API
curl http://localhost:5000/api/sparql/queries            # Liste requêtes
curl http://localhost:5000/api/ontology/statistics       # Stats ontologie
```

### Développement
```bash
source venv/bin/activate            # Activer environnement
pip install -r requirements.txt     # Installer dépendances
python backend/app.py               # Lancer serveur
```

---

## 📞 Support

### Problème d'Installation
→ [INSTALLATION.md](INSTALLATION.md) section Dépannage

### Problème d'Utilisation
→ [GUIDE_UTILISATION.md](GUIDE_UTILISATION.md) section Dépannage

### Question Technique
→ [ARCHITECTURE.md](ARCHITECTURE.md)

### Autre Question
→ Consulter [README.md](README.md)

---

## 🎓 Apprentissage

### Débutant
1. [QUICK_START.md](QUICK_START.md) - Comprendre les bases
2. [GUIDE_UTILISATION.md](GUIDE_UTILISATION.md) - Apprendre à utiliser
3. Tester chaque interface

### Intermédiaire
1. [ARCHITECTURE.md](ARCHITECTURE.md) - Comprendre l'architecture
2. Explorer le code source
3. Modifier des requêtes SPARQL

### Avancé
1. [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - Vue d'ensemble complète
2. Étendre les fonctionnalités
3. Ajouter de nouvelles classes à l'ontologie

---

## 🌟 Points Forts du Projet

✅ **Complet** - Toutes les fonctionnalités demandées
✅ **Documenté** - 7 fichiers de documentation
✅ **Modulaire** - Architecture claire et extensible
✅ **Moderne** - Technologies récentes
✅ **Fonctionnel** - Prêt à l'emploi
✅ **Éducatif** - Exemples et explications

---

## 📅 Prochaines Étapes Suggérées

1. ✅ Lire QUICK_START.md
2. ✅ Installer et lancer l'application
3. ✅ Tester les 6 interfaces
4. ✅ Exécuter des requêtes SPARQL
5. ✅ Générer des recommandations
6. ✅ Explorer l'ontologie
7. 📝 Personnaliser avec vos données
8. 🔧 Étendre les fonctionnalités

---

**Bon voyage dans l'écotourisme sémantique! 🌍🌱✨**
