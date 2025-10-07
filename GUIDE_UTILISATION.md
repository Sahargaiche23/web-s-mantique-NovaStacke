# 📖 Guide d'Utilisation - EcoTravel

## 🚀 Démarrage Rapide

### 1. Installation et Lancement

```bash
# Se positionner dans le projet
cd /home/sahar/CascadeProjects/eco_travel_semantic

# Activer l'environnement virtuel
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt

# Lancer le serveur
cd backend
python app.py
```

L'application sera accessible sur: **http://localhost:5000**

---

## 🎯 Utilisation des Interfaces

### Interface 1: Page d'Accueil 🏠

**Objectif**: Vue d'ensemble et statistiques

**Fonctionnalités**:
- Affichage des statistiques en temps réel (destinations, hébergements, activités)
- Score écologique moyen de la plateforme
- Accès rapide aux fonctionnalités principales

**Utilisation**:
1. Ouvrir http://localhost:5000
2. Consulter les statistiques du dashboard
3. Cliquer sur les cartes pour accéder aux sections

---

### Interface 2: Recherche Avancée 🔍

**Objectif**: Trouver des options écologiques avec filtres multiples

**Fonctionnalités**:
- Filtrage par type (Destination, Hébergement, Activité, Transport)
- Filtrage par consommation énergétique maximale
- Filtrage par localisation
- Recherche textuelle dans toute l'ontologie

**Exemple d'utilisation**:
1. Cliquer sur "Recherche" dans le menu
2. Sélectionner "Hébergement" dans le filtre Type
3. Entrer "150" dans Consommation Énergie Max
4. Entrer "Tunisie" dans Localisation
5. Cliquer sur "Rechercher"

**Résultat**: Liste des hébergements en Tunisie consommant moins de 150 kWh

---

### Interface 3: Recommandations IA ⭐

**Objectif**: Obtenir des suggestions personnalisées intelligentes

**Fonctionnalités**:
- Configuration du profil utilisateur (budget, profil écologique, préférences)
- Génération automatique de recommandations
- Affichage du score écologique total
- Calcul de l'empreinte carbone estimée
- Recommandations pour: destinations, hébergements, activités, transports

**Exemple d'utilisation**:
1. Cliquer sur "Recommandations"
2. Configurer votre profil:
   - Budget: 1500 €
   - Profil Écologique: Éco-responsable
   - Préférences: Culture et nature
3. Cliquer sur "Générer Recommandations"

**Résultat**: Plan de voyage complet avec:
- Top 3 destinations adaptées
- Top 3 hébergements écologiques
- Top 5 activités à faible impact
- Meilleurs moyens de transport
- Score écologique global /100
- Empreinte carbone totale en kg CO2

---

### Interface 4: Éditeur SPARQL 💻

**Objectif**: Interroger l'ontologie avec des requêtes SPARQL

**Fonctionnalités**:
- 15+ requêtes SPARQL prédéfinies
- Éditeur de requêtes personnalisées
- Affichage des résultats en tableau
- Export des données

**Requêtes disponibles**:

#### 1. **eco_accommodations** - Hébergements écologiques
```sparql
Trouve tous les hébergements avec leur consommation énergétique 
et certification, triés par consommation croissante
```

#### 2. **biodiversity_destinations** - Destinations biodiversité
```sparql
Destinations avec biodiversité riche et nombre d'activités locales
```

#### 3. **transport_comparison** - Comparaison transports
```sparql
Compare les émissions CO2 de tous les types de transport
```

#### 4. **eco_travelers** - Voyageurs éco-responsables
```sparql
Liste les voyageurs avec profil écologique et leurs préférences
```

#### 5. **low_impact_activities** - Activités faible impact
```sparql
Activités touristiques avec impact environnemental faible
```

**Exemple d'utilisation**:
1. Cliquer sur "SPARQL"
2. Sélectionner "transport_comparison" dans la liste
3. Les résultats s'affichent automatiquement
4. Pour une requête personnalisée, écrire dans l'éditeur et cliquer "Exécuter"

**Exemple de requête personnalisée**:
```sparql
PREFIX eco: <http://example.org/ecotourisme#>
SELECT ?destination ?localisation ?biodiversite
WHERE {
  ?destination rdf:type eco:Destination .
  ?destination eco:aLocalisation ?localisation .
  ?destination eco:aBiodiversité ?biodiversite .
  FILTER(CONTAINS(?localisation, "Tunisie"))
}
```

---

### Interface 5: Visualisations 📊

**Objectif**: Explorer les données avec des graphiques interactifs

**Graphiques disponibles**:

#### 1. **Comparaison Carbone** (Graphique en barres)
- Compare les émissions CO2 par type de transport
- Couleurs: Vert (faible), Jaune (moyen), Rouge (élevé)
- Permet d'identifier les transports les plus écologiques

#### 2. **Consommation Énergétique** (Graphique en ligne)
- Évolution de la consommation des hébergements
- Tendance de l'efficacité énergétique
- Identification des hébergements les plus performants

#### 3. **Scores Écologiques** (Graphique radar)
- Comparaison multidimensionnelle des destinations
- Critères: Énergie, Certification, Activités, Score Total
- Vue d'ensemble des performances écologiques

#### 4. **Distribution Certifications** (Graphique circulaire)
- Répartition des niveaux de certification (Gold, Silver, Bronze)
- Pourcentage de chaque niveau
- État de la certification dans la plateforme

**Utilisation**:
1. Cliquer sur "Visualisations"
2. Les 4 graphiques se chargent automatiquement
3. Survoler les graphiques pour voir les détails
4. Les graphiques sont interactifs (zoom, filtres)

---

### Interface 6: Explorateur d'Ontologie 🗂️

**Objectif**: Naviguer dans la structure de l'ontologie RDF/OWL

**Sections**:

#### A. **Classes**
Liste toutes les classes de l'ontologie:
- Destination
- Hébergement
- Transport (Avion, Train, Vélo, etc.)
- ActivitéTouristique
- CertificationÉcologique
- EmpreinteCarbone
- CommunautéLocale
- ÉvénementCulturel
- GastronomieLocale
- RessourceNaturelle
- Voyageur

#### B. **Propriétés**
Affiche toutes les propriétés (relations et attributs):

**Propriétés d'objet**:
- aCertification (Hébergement → Certification)
- aEmpreinte (Transport → EmpreinteCarbone)
- choisit (Voyageur → Destination)
- implique (Activité → Communauté)
- organise (Destination → Événement)
- propose (Destination → Hébergement)
- utilise (Gastronomie → Ressource)

**Propriétés de données**:
- aBudget, aCO2, aConsommationÉnergie
- aLocalisation, aBiodiversité
- aImpactEnvironnemental
- Et 10+ autres...

#### C. **Individus**
Liste tous les individus (instances) avec leur type:
- Ali (Voyageur)
- TunisCarthage (Destination)
- HotelEcoGreen (Hébergement)
- TrainExpress (Train)
- RandonnéeAtlas (ActivitéTouristique)
- Et 20+ autres...

**Utilisation**:
1. Cliquer sur "Ontologie"
2. Explorer les 3 colonnes (Classes, Propriétés, Individus)
3. Chaque élément affiche ses informations détaillées

---

## 🔧 Utilisation de l'API REST

### Endpoints Principaux

#### 1. Santé de l'API
```bash
GET http://localhost:5000/api/health
```
Retourne l'état de l'application et statistiques de l'ontologie

#### 2. Exécuter une requête SPARQL
```bash
POST http://localhost:5000/api/sparql/execute
Content-Type: application/json

{
  "query": "PREFIX eco: <http://example.org/ecotourisme#> SELECT * WHERE { ?s ?p ?o } LIMIT 10"
}
```

#### 3. Requête SPARQL prédéfinie
```bash
GET http://localhost:5000/api/sparql/predefined/eco_accommodations
```

#### 4. Recommandations de destinations
```bash
POST http://localhost:5000/api/recommendations/destinations
Content-Type: application/json

{
  "max_budget": 1500,
  "eco_profile": "Éco-responsable",
  "preferences": "Culture et nature"
}
```

#### 5. Plan de voyage complet
```bash
POST http://localhost:5000/api/recommendations/travel-plan
Content-Type: application/json

{
  "max_budget": 2000,
  "eco_profile": "Éco-responsable",
  "preferences": "Aventure et écologie"
}
```

#### 6. Recherche dans l'ontologie
```bash
POST http://localhost:5000/api/ontology/search
Content-Type: application/json

{
  "text": "écologique"
}
```

#### 7. Filtrage avancé
```bash
POST http://localhost:5000/api/advanced/filter
Content-Type: application/json

{
  "max_energy": 150,
  "location": "Tunisie",
  "min_certification_level": "Gold"
}
```

#### 8. Données de visualisation
```bash
GET http://localhost:5000/api/visualizations/carbon-comparison
GET http://localhost:5000/api/visualizations/eco-scores
GET http://localhost:5000/api/visualizations/energy-consumption
```

---

## 💡 Cas d'Usage Pratiques

### Cas 1: Trouver un hébergement écologique en Tunisie

**Méthode 1 - Interface Recherche**:
1. Aller sur "Recherche"
2. Type: Hébergement
3. Localisation: Tunisie
4. Énergie Max: 150
5. Rechercher

**Méthode 2 - SPARQL**:
```sparql
PREFIX eco: <http://example.org/ecotourisme#>
SELECT ?hebergement ?energie ?certification
WHERE {
  ?destination eco:aLocalisation "Tunisie" .
  ?destination eco:propose ?hebergement .
  ?hebergement eco:aConsommationÉnergie ?energie .
  ?hebergement eco:aCertification ?certification .
  FILTER(?energie < 150)
}
```

---

### Cas 2: Comparer l'impact carbone des transports

**Méthode 1 - Visualisations**:
1. Aller sur "Visualisations"
2. Consulter le graphique "Comparaison Carbone"
3. Identifier le transport le plus écologique

**Méthode 2 - SPARQL**:
1. Aller sur "SPARQL"
2. Sélectionner "transport_comparison"
3. Analyser les résultats

---

### Cas 3: Planifier un voyage éco-responsable

1. Aller sur "Recommandations"
2. Configurer:
   - Budget: 1500€
   - Profil: Éco-responsable
   - Préférences: Culture et nature
3. Générer les recommandations
4. Consulter:
   - Destinations recommandées avec scores
   - Hébergements certifiés
   - Activités à faible impact
   - Transports optimaux
   - Score écologique total
   - Empreinte carbone estimée

---

## 🎓 Comprendre les Scores

### Score Écologique (/100)
Calculé selon:
- **50%** Consommation énergétique (plus c'est bas, mieux c'est)
- **25%** Certifications écologiques (Gold = +20, Silver = +10)
- **25%** Impact environnemental des activités

### Empreinte Carbone (kg CO2)
Basée sur:
- Type de transport utilisé
- Distance estimée
- Nombre de passagers (covoiturage)

**Références**:
- Vélo: 0 kg CO2
- Train: ~45 kg CO2
- Bus électrique: ~25 kg CO2
- Covoiturage: ~35 kg CO2
- Avion: ~250 kg CO2

---

## 🐛 Dépannage

### Problème: Le serveur ne démarre pas
**Solution**:
```bash
# Vérifier Python
python --version  # Doit être 3.8+

# Réinstaller les dépendances
pip install -r requirements.txt

# Vérifier le port
lsof -i :5000  # Si occupé, changer le port dans app.py
```

### Problème: Erreur de chargement de l'ontologie
**Solution**:
```bash
# Vérifier que le fichier existe
ls ontology/ecotourisme.owl

# Vérifier les permissions
chmod 644 ontology/ecotourisme.owl
```

### Problème: Les graphiques ne s'affichent pas
**Solution**:
- Vérifier la connexion internet (Chart.js est chargé via CDN)
- Ouvrir la console du navigateur (F12) pour voir les erreurs
- Vérifier que l'API répond: http://localhost:5000/api/health

---

## 📚 Ressources Supplémentaires

### Documentation SPARQL
- [SPARQL 1.1 Query Language](https://www.w3.org/TR/sparql11-query/)
- [RDFLib Documentation](https://rdflib.readthedocs.io/)

### Standards RDF/OWL
- [RDF Primer](https://www.w3.org/TR/rdf-primer/)
- [OWL 2 Web Ontology Language](https://www.w3.org/TR/owl2-overview/)

### Frameworks utilisés
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Chart.js Documentation](https://www.chartjs.org/docs/)
- [TailwindCSS Documentation](https://tailwindcss.com/docs)

---

## 🤝 Support

Pour toute question ou problème:
1. Consulter ce guide
2. Vérifier les logs du serveur
3. Consulter la console du navigateur (F12)
4. Ouvrir une issue sur le projet

---

**Bon voyage écologique! 🌍🌱**
