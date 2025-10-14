# 🏗️ Architecture Technique - EcoTravel

## 📐 Vue d'Ensemble

```
┌─────────────────────────────────────────────────────────────┐
│                     FRONTEND (HTML/JS)                       │
│  ┌──────────┬──────────┬──────────┬──────────┬──────────┐  │
│  │  Accueil │Recherche │Recommand.│  SPARQL  │  Viz     │  │
│  └──────────┴──────────┴──────────┴──────────┴──────────┘  │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP/REST API
┌────────────────────────▼────────────────────────────────────┐
│                    BACKEND (Flask)                           │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              app.py (Routes API)                      │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────┬──────────┬──────────┬──────────────────────┐ │
│  │ Ontology │  SPARQL  │Recommend.│   Visualization      │ │
│  │ Manager  │ Queries  │  Engine  │      Engine          │ │
│  └──────────┴──────────┴──────────┴──────────────────────┘ │
└────────────────────────┬────────────────────────────────────┘
                         │ rdflib
┌────────────────────────▼────────────────────────────────────┐
│              ONTOLOGIE RDF/OWL                               │
│              ecotourisme.owl                                 │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Classes │ Propriétés │ Individus │ Restrictions      │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎯 Couche Frontend

### Technologies
- **HTML5** - Structure sémantique
- **TailwindCSS** - Styling moderne et responsive
- **JavaScript ES6+** - Logique client
- **Chart.js** - Visualisations interactives

### Composants

#### 1. **Navigation** (`index.html`)
```html
<nav> → Menu principal avec 6 liens
  ├── Accueil
  ├── Recherche
  ├── Recommandations
  ├── SPARQL
  ├── Visualisations
  └── Ontologie
```

#### 2. **Pages** (Single Page Application)
```javascript
// app.js - Gestion des pages
showPage(pageName) {
  - Cache toutes les pages
  - Affiche la page demandée
  - Charge les données spécifiques
}
```

#### 3. **Communication API** (`app.js`)
```javascript
const API_BASE = 'http://localhost:5000/api';

// Fonctions principales:
- loadHomeData()          → Statistiques
- performSearch()         → Recherche avancée
- generateRecommendations() → IA recommandations
- executeSPARQL()         → Requêtes SPARQL
- loadVisualizations()    → Graphiques
- loadOntologyData()      → Explorer ontologie
```

---

## ⚙️ Couche Backend

### Architecture Flask

```python
backend/
├── app.py                    # Application principale + Routes
├── ontology_manager.py       # Gestionnaire RDF/OWL
├── sparql_queries.py         # 15 requêtes SPARQL
├── recommendation_engine.py  # Système IA
└── visualization_engine.py   # Données graphiques
```

### 1. **app.py** - Application Flask

#### Routes Principales

**Santé & Info**
```python
GET  /api/health              → État de l'application
GET  /api/ontology/statistics → Stats ontologie
```

**SPARQL**
```python
POST /api/sparql/execute           → Requête personnalisée
GET  /api/sparql/predefined/<name> → Requête prédéfinie
GET  /api/sparql/queries           → Liste requêtes
```

**Ontologie**
```python
GET  /api/ontology/classes         → Toutes les classes
GET  /api/ontology/properties      → Toutes les propriétés
GET  /api/ontology/individuals     → Tous les individus
POST /api/ontology/search          → Recherche textuelle
GET  /api/ontology/related/<name>  → Entités liées
```

**Recommandations**
```python
POST /api/recommendations/accommodations → Hébergements
POST /api/recommendations/destinations   → Destinations
POST /api/recommendations/activities     → Activités
POST /api/recommendations/transport      → Transports
POST /api/recommendations/travel-plan    → Plan complet
```

**Visualisations**
```python
GET /api/visualizations/carbon-comparison  → Graphique CO2
GET /api/visualizations/eco-scores         → Scores éco
GET /api/visualizations/energy-consumption → Énergie
GET /api/visualizations/network-graph      → Réseau
```

**Avancé**
```python
POST /api/advanced/filter             → Filtrage multi-critères
POST /api/advanced/compare            → Comparaison entités
GET  /api/advanced/eco-score/<entity> → Score d'une entité
```

---

### 2. **ontology_manager.py** - Gestionnaire RDF

#### Classe OntologyManager

```python
class OntologyManager:
    def __init__(self, ontology_path):
        self.graph = Graph()  # rdflib Graph
        self.eco = Namespace("http://example.org/ecotourisme#")
        
    # Méthodes principales:
    - load_ontology()           → Charge le fichier OWL
    - execute_sparql(query)     → Exécute requête SPARQL
    - get_all_classes()         → Liste classes
    - get_all_properties()      → Liste propriétés
    - get_all_individuals()     → Liste individus
    - add_individual()          → Ajoute instance
    - save_ontology()           → Sauvegarde modifications
    - search_by_text()          → Recherche textuelle
    - get_related_entities()    → Relations d'une entité
```

#### Gestion RDF avec rdflib

```python
# Chargement
self.graph.parse(ontology_path, format="xml")

# Requête SPARQL
results = self.graph.query(sparql_query)

# Ajout de triplet
self.graph.add((subject, predicate, object))

# Sauvegarde
self.graph.serialize(destination=path, format='xml')
```

---

### 3. **sparql_queries.py** - Requêtes SPARQL

#### Structure

```python
class SPARQLQueries:
    PREFIX = """
    PREFIX eco: <http://example.org/ecotourisme#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    """
    
    # 15 requêtes prédéfinies
    QUERY_1_ECO_ACCOMMODATIONS = PREFIX + """..."""
    QUERY_2_BIODIVERSITY_DESTINATIONS = PREFIX + """..."""
    # ... jusqu'à QUERY_15
```

#### Exemples de Requêtes Complexes

**Requête 8 - Analyse Destination** (Agrégation)
```sparql
SELECT ?destination ?localisation 
       (COUNT(DISTINCT ?hebergement) AS ?nbHebergements)
       (AVG(?energie) AS ?energieMoyenne)
WHERE {
    ?destination rdf:type eco:Destination .
    OPTIONAL {
        ?destination eco:propose ?hebergement .
        ?hebergement eco:aConsommationÉnergie ?energie
    }
}
GROUP BY ?destination ?localisation
```

**Requête 15 - Score Écologique** (Calcul composite)
```sparql
SELECT ?destination
       ((100 - AVG(?energie)) + 
        (COUNT(DISTINCT ?certification) * 10) + 
        (COUNT(DISTINCT ?activiteFaible) * 5) AS ?scoreTotal)
WHERE { ... }
GROUP BY ?destination
ORDER BY DESC(?scoreTotal)
```

---

### 4. **recommendation_engine.py** - IA

#### Classe RecommendationEngine

```python
class RecommendationEngine:
    def __init__(self, ontology_manager):
        self.ontology = ontology_manager
        self.scaler = MinMaxScaler()
```

#### Algorithmes de Scoring

**Score Écologique**
```python
def calculate_eco_score(accommodation_data):
    score = 100
    
    # Pénalité énergie
    score -= min(energie / 2, 50)
    
    # Bonus certification
    if 'gold': score += 20
    elif 'silver': score += 10
    
    return max(0, min(100, score))
```

**Empreinte Carbone**
```python
def calculate_carbon_footprint(transport_type, distance_km):
    emission_factors = {
        'Avion': 0.255,
        'Train': 0.041,
        'Vélo': 0.0,
        ...
    }
    return distance_km * emission_factors[transport_type]
```

**Recommandations Hébergements**
```python
def recommend_accommodations(user_preferences, limit=5):
    # 1. Récupérer données via SPARQL
    results = self.ontology.execute_sparql(query)
    
    # 2. Calculer scores
    for result in results:
        eco_score = calculate_eco_score(result)
        budget_score = calculate_budget_score(result, user_prefs)
        preference_score = calculate_preference_score(result, user_prefs)
        
        # 3. Score pondéré
        final_score = (
            eco_score * 0.5 +
            budget_score * 0.3 +
            preference_score * 0.2
        )
    
    # 4. Trier et retourner top N
    return sorted(recommendations, key=lambda x: x['final_score'])[:limit]
```

**Plan de Voyage Complet**
```python
def generate_travel_plan(user_preferences):
    return {
        'recommendations': {
            'destinations': recommend_destinations(),
            'accommodations': recommend_accommodations(),
            'activities': recommend_activities(),
            'transport': recommend_transport()
        },
        'total_eco_score': calculate_total_score(),
        'estimated_carbon_footprint': calculate_total_carbon()
    }
```

---

### 5. **visualization_engine.py** - Visualisations

#### Classe VisualizationEngine

```python
class VisualizationEngine:
    def __init__(self, ontology_manager):
        self.ontology = ontology_manager
```

#### Génération de Données pour Chart.js

**Graphique en Barres**
```python
def create_carbon_comparison_chart():
    return {
        'type': 'bar',
        'title': 'Comparaison CO2',
        'labels': ['Train', 'Bus', 'Avion', ...],
        'datasets': [{
            'label': 'Émissions CO2 (kg)',
            'data': [45, 25, 250, ...],
            'backgroundColor': ['green', 'yellow', 'red', ...]
        }]
    }
```

**Graphique Radar**
```python
def create_eco_scores_chart():
    return {
        'type': 'radar',
        'labels': ['Énergie', 'Certification', 'Activités', 'Total'],
        'datasets': [
            {
                'label': 'Destination 1',
                'data': [85, 90, 75, 83]
            },
            ...
        ]
    }
```

---

## 🗄️ Couche Données - Ontologie RDF/OWL

### Structure de l'Ontologie

```turtle
@prefix eco: <http://example.org/ecotourisme#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
```

### Classes (11)

```
eco:Destination
eco:Hébergement
eco:Transport
  ├── eco:Avion
  ├── eco:Train
  ├── eco:Vélo
  ├── eco:TransportPublic
  └── eco:Covoiturage
eco:ActivitéTouristique
eco:Voyageur
eco:CertificationÉcologique
eco:EmpreinteCarbone
eco:CommunautéLocale
eco:ÉvénementCulturel
eco:GastronomieLocale
eco:RessourceNaturelle
```

### Propriétés d'Objet (7)

```
eco:aCertification      (Hébergement → Certification)
eco:aEmpreinte         (Transport → EmpreinteCarbone)
eco:choisit            (Voyageur → Destination)
eco:implique           (Activité → Communauté)
eco:organise           (Destination → Événement)
eco:propose            (Destination → Hébergement)
eco:utilise            (Gastronomie → Ressource)
```

### Propriétés de Données (16)

```
eco:aBudget            : decimal
eco:aCO2               : decimal
eco:aConsommationÉnergie : decimal
eco:aLocalisation      : string
eco:aBiodiversité      : string
eco:aImpactEnvironnemental : string
eco:aProduitLocal      : boolean
... (et 9 autres)
```

### Individus (30+)

```
Voyageurs: Ali, Fatima, Mohamed
Destinations: TunisCarthage, Marrakech, Djerba, Sahara
Hébergements: HotelEcoGreen, RiadEcologique, EcoLodgeDjerba, ...
Transports: TrainExpress, BusElectrique, VeloPartage, ...
Activités: RandonnéeAtlas, PlongeeRecif, TrekkingDesert, ...
```

---

## 🔄 Flux de Données

### Exemple: Génération de Recommandations

```
1. USER → Frontend
   └─ Remplit formulaire profil
   
2. Frontend → Backend
   └─ POST /api/recommendations/travel-plan
      Body: {budget: 1500, eco_profile: "Éco-responsable"}
   
3. Backend → RecommendationEngine
   └─ generate_travel_plan(user_preferences)
   
4. RecommendationEngine → OntologyManager
   └─ execute_sparql(QUERY_11_PERSONALIZED_RECOMMENDATIONS)
   
5. OntologyManager → RDF Graph
   └─ graph.query(sparql_query)
   
6. RDF Graph → OntologyManager
   └─ Résultats SPARQL
   
7. OntologyManager → RecommendationEngine
   └─ Données formatées
   
8. RecommendationEngine
   └─ Calcul des scores (eco_score, budget_score, etc.)
   └─ Tri et sélection top N
   
9. RecommendationEngine → Backend
   └─ Plan de voyage complet avec scores
   
10. Backend → Frontend
    └─ JSON response
    
11. Frontend → USER
    └─ Affichage des recommandations
```

---

## 🔐 Sécurité

### Mesures Implémentées

1. **Validation des entrées**
   - Filtrage des requêtes SPARQL
   - Validation des paramètres API

2. **CORS**
   - Configuration pour développement
   - À restreindre en production

3. **Gestion des erreurs**
   - Try/catch sur toutes les opérations
   - Messages d'erreur informatifs

4. **Limites**
   - Limite de résultats SPARQL (100)
   - Timeout API (30s)

---

## 📊 Performance

### Optimisations

1. **Cache côté client**
   - Statistiques chargées une fois
   - Graphiques mis en cache

2. **Requêtes SPARQL optimisées**
   - OPTIONAL pour données manquantes
   - LIMIT sur résultats
   - INDEX sur propriétés fréquentes

3. **Lazy loading**
   - Données chargées à la demande
   - Graphiques générés au besoin

---

## 🚀 Déploiement

### Développement
```bash
python backend/app.py
# → http://localhost:5000
```

### Production
```bash
gunicorn -w 4 -b 0.0.0.0:5000 backend.app:app
```

### Docker
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "backend.app:app"]
```

---

## 📈 Extensibilité

### Ajouter une Nouvelle Classe

1. **Ontologie** (`ecotourisme.owl`)
```xml
<Class rdf:about="http://example.org/ecotourisme#NouvelleClasse"/>
```

2. **Requête SPARQL** (`sparql_queries.py`)
```python
QUERY_16_NEW = PREFIX + """
SELECT ?entity WHERE {
    ?entity rdf:type eco:NouvelleClasse .
}
"""
```

3. **Route API** (`app.py`)
```python
@app.route('/api/nouvelle-classe', methods=['GET'])
def get_nouvelle_classe():
    results = ontology.execute_sparql(SPARQLQueries.QUERY_16_NEW)
    return jsonify(results)
```

4. **Frontend** (`app.js`)
```javascript
async function loadNouvelleClasse() {
    const response = await fetch(`${API_BASE}/nouvelle-classe`);
    const data = await response.json();
    displayResults(data);
}
```

---

**Architecture modulaire, scalable et maintenable! 🏗️✨**
