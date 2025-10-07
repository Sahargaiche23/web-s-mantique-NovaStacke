# 🌍 EcoTravel - Application de Voyage Sémantique Écologique

Application web intelligente pour recommander des destinations, hébergements et activités touristiques à faible empreinte carbone, basée sur une ontologie RDF/OWL et des requêtes SPARQL avancées.

## 🎯 Fonctionnalités

### 1. **Ontologie RDF/OWL Complète**
- 11 classes principales (Destination, Hébergement, Transport, etc.)
- 7 propriétés d'objet (aCertification, aEmpreinte, choisit, etc.)
- 16 propriétés de données (aBudget, aCO2, aLocalisation, etc.)
- Individus avec données réelles (Tunisie, Maroc, etc.)

### 2. **15+ Requêtes SPARQL Complexes**
- Hébergements écologiques avec filtrage énergétique
- Comparaison des empreintes carbone par transport
- Analyse de biodiversité des destinations
- Scores écologiques composites
- Hiérarchie des classes de transport
- Et bien plus...

### 3. **Système de Recommandation IA**
- Algorithmes de scoring multi-critères
- Recommandations personnalisées basées sur :
  - Budget utilisateur
  - Profil écologique
  - Préférences de voyage
- Calcul d'empreinte carbone
- Génération de plans de voyage complets

### 4. **6+ Interfaces Utilisateur**
1. **Accueil** - Dashboard avec statistiques en temps réel
2. **Recherche Avancée** - Filtrage multi-critères
3. **Recommandations** - Suggestions personnalisées IA
4. **SPARQL** - Éditeur de requêtes avec requêtes prédéfinies
5. **Visualisations** - Graphiques interactifs (Chart.js)
6. **Ontologie** - Exploration des classes, propriétés et individus

### 5. **Visualisations Avancées**
- Graphiques en barres (comparaison CO2)
- Graphiques en ligne (consommation énergétique)
- Graphiques radar (scores écologiques)
- Graphiques circulaires (certifications)
- Graphiques à bulles (analyse destinations)

### 6. **API REST Complète**
- `/api/sparql/*` - Exécution de requêtes SPARQL
- `/api/recommendations/*` - Système de recommandation
- `/api/ontology/*` - Exploration de l'ontologie
- `/api/visualizations/*` - Données pour graphiques
- `/api/advanced/*` - Filtrage et comparaison avancés

## 🛠️ Technologies

### Backend
- **Flask** - Framework web Python
- **rdflib** - Manipulation RDF/OWL
- **scikit-learn** - Machine learning pour recommandations
- **numpy/pandas** - Traitement de données
- **matplotlib/seaborn/plotly** - Visualisations

### Frontend
- **HTML5/CSS3** - Structure et style
- **TailwindCSS** - Framework CSS moderne
- **JavaScript ES6+** - Logique frontend
- **Chart.js** - Graphiques interactifs

## 📦 Installation

### Prérequis
- Python 3.8+
- pip

### Étapes

1. **Cloner le projet**
```bash
cd /home/sahar/CascadeProjects/eco_travel_semantic
```

2. **Créer un environnement virtuel**
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

4. **Lancer l'application**
```bash
cd backend
python app.py
```

5. **Accéder à l'application**
Ouvrir le navigateur: `http://localhost:5000`

## 📁 Structure du Projet

```
eco_travel_semantic/
├── ontology/
│   └── ecotourisme.owl          # Ontologie RDF/OWL
├── backend/
│   ├── app.py                   # Application Flask principale
│   ├── ontology_manager.py      # Gestionnaire RDF avec rdflib
│   ├── sparql_queries.py        # 15+ requêtes SPARQL
│   ├── recommendation_engine.py # Système de recommandation IA
│   └── visualization_engine.py  # Moteur de visualisation
├── frontend/
│   ├── index.html               # Interface principale
│   └── js/
│       └── app.js               # Logique JavaScript
├── requirements.txt             # Dépendances Python
└── README.md                    # Documentation
```

## 🔍 Exemples d'Utilisation

### 1. Recherche Avancée
```javascript
// Filtrer les hébergements par consommation énergétique
POST /api/advanced/filter
{
  "max_energy": 150,
  "location": "Tunisie"
}
```

### 2. Recommandations Personnalisées
```javascript
// Générer un plan de voyage
POST /api/recommendations/travel-plan
{
  "max_budget": 1500,
  "eco_profile": "Éco-responsable",
  "preferences": "Culture et nature"
}
```

### 3. Requête SPARQL
```sparql
PREFIX eco: <http://example.org/ecotourisme#>
SELECT ?hebergement ?energie ?certification
WHERE {
  ?hebergement rdf:type eco:Hébergement .
  ?hebergement eco:aConsommationÉnergie ?energie .
  ?hebergement eco:aCertification ?certification .
  FILTER(?energie < 150)
}
ORDER BY ?energie
```

## 📊 Requêtes SPARQL Disponibles

1. **eco_accommodations** - Hébergements écologiques
2. **biodiversity_destinations** - Destinations biodiversité
3. **transport_comparison** - Comparaison transports
4. **eco_travelers** - Voyageurs éco-responsables
5. **low_impact_activities** - Activités faible impact
6. **local_gastronomy** - Gastronomie locale
7. **cultural_events** - Événements culturels
8. **destination_analysis** - Analyse destinations
9. **certifications** - Certifications écologiques
10. **transport_hierarchy** - Hiérarchie transports
11. **personalized_recommendations** - Recommandations
12. **environmental_impact** - Impact environnemental
13. **local_communities** - Communautés locales
14. **natural_resources** - Ressources naturelles
15. **eco_score** - Score écologique composite

## 🎨 Interfaces

### 1. Page d'Accueil
- Dashboard avec 4 statistiques clés
- Actions rapides vers les fonctionnalités principales

### 2. Recherche Avancée
- Filtres multi-critères (type, énergie, localisation)
- Recherche textuelle dans l'ontologie
- Affichage des résultats en temps réel

### 3. Recommandations IA
- Configuration du profil utilisateur
- Génération de recommandations personnalisées
- Affichage du score écologique et empreinte carbone

### 4. Éditeur SPARQL
- Liste de 15+ requêtes prédéfinies
- Éditeur de requêtes personnalisées
- Affichage des résultats en tableau

### 5. Visualisations
- 4+ graphiques interactifs
- Comparaisons visuelles
- Analyses multidimensionnelles

### 6. Explorateur d'Ontologie
- Navigation dans les classes
- Exploration des propriétés
- Liste des individus

## 🧠 Système de Recommandation

### Algorithmes
- **Scoring multi-critères** - Pondération de plusieurs facteurs
- **Filtrage collaboratif** - Basé sur les préférences
- **Calcul d'empreinte carbone** - Estimation CO2
- **Optimisation budget** - Respect des contraintes financières

### Critères de Scoring
- Consommation énergétique (35%)
- Certifications écologiques (25%)
- Impact environnemental (20%)
- Préférences utilisateur (20%)

## 🔒 Sécurité

- Validation des entrées utilisateur
- Protection contre les injections SPARQL
- CORS configuré pour le développement
- Gestion des erreurs robuste

## 🚀 Déploiement

### Production
```bash
# Utiliser Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 backend.app:app
```

### Docker (optionnel)
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "backend/app.py"]
```

## 📈 Améliorations Futures

- [ ] Authentification utilisateur
- [ ] Base de données pour historique
- [ ] API de géolocalisation réelle
- [ ] Intégration avec APIs de voyage
- [ ] Application mobile
- [ ] Système de notation communautaire
- [ ] Export PDF des recommandations
- [ ] Chatbot IA avec NLP

## 👥 Contribution

Ce projet est développé dans le cadre d'une application de voyage sémantique écologique.

## 📄 Licence

MIT License

## 📞 Contact

Pour toute question ou suggestion, n'hésitez pas à ouvrir une issue.

---

**Développé avec ❤️ et 🌱 pour un tourisme plus durable**
