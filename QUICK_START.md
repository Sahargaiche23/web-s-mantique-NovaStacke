# ⚡ Démarrage Rapide - EcoTravel

## 🎯 En 3 Minutes

### Étape 1: Installation (1 min)

```bash
cd /home/sahar/CascadeProjects/eco_travel_semantic
chmod +x start.sh
./start.sh
```

Le script va automatiquement:
- ✅ Créer l'environnement virtuel
- ✅ Installer toutes les dépendances
- ✅ Vérifier l'ontologie
- ✅ Lancer le serveur

### Étape 2: Accès (30 sec)

Ouvrir votre navigateur: **http://localhost:5000**

### Étape 3: Exploration (1 min 30)

1. **Voir les statistiques** → Page d'accueil
2. **Générer des recommandations** → Onglet "Recommandations"
3. **Explorer l'ontologie** → Onglet "Ontologie"

---

## 🎮 Premiers Tests

### Test 1: Vérifier l'API
```bash
curl http://localhost:5000/api/health
```

**Résultat attendu:**
```json
{
  "status": "healthy",
  "ontology_loaded": true,
  "statistics": {
    "total_triples": 150,
    "classes": 11,
    "individuals": 30
  }
}
```

### Test 2: Requête SPARQL Simple
```bash
curl http://localhost:5000/api/sparql/predefined/eco_accommodations
```

**Résultat:** Liste des hébergements écologiques

### Test 3: Recommandations
```bash
curl -X POST http://localhost:5000/api/recommendations/destinations \
  -H "Content-Type: application/json" \
  -d '{"max_budget": 1500, "eco_profile": "Éco-responsable"}'
```

**Résultat:** Top destinations recommandées

---

## 📱 Interface Web - Guide Visuel

### 1. Page d'Accueil 🏠
```
┌─────────────────────────────────────────┐
│  🌍 EcoTravel                           │
├─────────────────────────────────────────┤
│  [Destinations: 4] [Hébergements: 5]   │
│  [Activités: 8]    [Score Éco: 85]     │
├─────────────────────────────────────────┤
│  [🔮 Recommandations] [🔍 Recherche]   │
│  [📊 Visualisations]                    │
└─────────────────────────────────────────┘
```

### 2. Recommandations ⭐
```
┌─────────────────────────────────────────┐
│  Votre Profil                           │
│  Budget: [1500€]                        │
│  Profil: [Éco-responsable ▼]           │
│  [🎯 Générer Recommandations]          │
├─────────────────────────────────────────┤
│  Score Écologique Total: 87/100        │
│  Empreinte Carbone: 45 kg CO2          │
├─────────────────────────────────────────┤
│  🌍 Destinations                        │
│  ✓ TunisCarthage (Score: 92/100)       │
│  ✓ Marrakech (Score: 88/100)           │
├─────────────────────────────────────────┤
│  🏨 Hébergements                        │
│  ✓ HotelEcoGreen (Énergie: 120 kWh)    │
│  ✓ RiadEcologique (Énergie: 95 kWh)    │
└─────────────────────────────────────────┘
```

### 3. SPARQL 💻
```
┌──────────┬──────────────────────────────┐
│ Requêtes │  Éditeur SPARQL              │
│          │  PREFIX eco: <...>           │
│ • eco_   │  SELECT ?dest ?loc           │
│   accomm │  WHERE {                     │
│ • biodiv │    ?dest rdf:type            │
│ • transp │      eco:Destination .       │
│ • ...    │  }                           │
│          │  [▶ Exécuter]                │
├──────────┴──────────────────────────────┤
│  Résultats (3 lignes)                   │
│  dest          | loc                    │
│  TunisCarthage | Tunisie                │
│  Marrakech     | Maroc                  │
└─────────────────────────────────────────┘
```

### 4. Visualisations 📊
```
┌──────────────────┬──────────────────┐
│  Comparaison CO2 │  Consommation    │
│  [Graphique Bar] │  [Graphique Line]│
├──────────────────┼──────────────────┤
│  Scores Éco      │  Certifications  │
│  [Graphique Radar│  [Graphique Pie] │
└──────────────────┴──────────────────┘
```

---

## 🎓 Scénarios d'Utilisation

### Scénario 1: Voyageur Éco-Responsable

**Objectif:** Trouver un voyage à faible empreinte carbone

1. Aller sur "Recommandations"
2. Configurer:
   - Budget: 1500€
   - Profil: Éco-responsable
   - Préférences: Nature et culture
3. Cliquer "Générer"
4. Consulter:
   - Destinations avec biodiversité
   - Hébergements certifiés
   - Activités faible impact
   - Transports verts (train, vélo)

**Résultat:** Plan de voyage avec score éco 85+ et empreinte < 50 kg CO2

---

### Scénario 2: Comparaison de Transports

**Objectif:** Choisir le transport le plus écologique

1. Aller sur "Visualisations"
2. Consulter le graphique "Comparaison CO2"
3. Observer:
   - ✅ Vélo: 0 kg CO2
   - ✅ Train: 45 kg CO2
   - ⚠️ Bus: 25 kg CO2
   - ❌ Avion: 250 kg CO2

**Résultat:** Le train réduit les émissions de 70% vs avion

---

### Scénario 3: Recherche d'Hébergement Spécifique

**Objectif:** Trouver un hôtel écologique en Tunisie

**Méthode A - Interface:**
1. Aller sur "Recherche"
2. Filtrer:
   - Type: Hébergement
   - Localisation: Tunisie
   - Énergie max: 150 kWh
3. Rechercher

**Méthode B - SPARQL:**
1. Aller sur "SPARQL"
2. Sélectionner "eco_accommodations"
3. Modifier la requête pour ajouter:
   ```sparql
   FILTER(CONTAINS(?localisation, "Tunisie"))
   ```

**Résultat:** Liste des hébergements éco en Tunisie avec scores

---

## 🔧 Dépannage Rapide

### Problème: Port 5000 occupé
```bash
# Trouver le processus
lsof -i :5000

# Tuer le processus
kill -9 <PID>

# Ou changer le port dans backend/app.py
app.run(port=5001)
```

### Problème: Module non trouvé
```bash
# Réactiver l'environnement
source venv/bin/activate

# Réinstaller
pip install -r requirements.txt
```

### Problème: Ontologie non chargée
```bash
# Vérifier le fichier
ls -lh ontology/ecotourisme.owl

# Vérifier les permissions
chmod 644 ontology/ecotourisme.owl
```

---

## 📊 Données de Test

### Destinations Disponibles
- **TunisCarthage** (Tunisie) - Biodiversité méditerranéenne
- **Marrakech** (Maroc) - Oasis et jardins
- **Djerba** (Tunisie) - Écosystème marin
- **Sahara** (Algérie) - Désert unique

### Hébergements Disponibles
- **HotelEcoGreen** - 120 kWh, Certification Gold
- **RiadEcologique** - 95 kWh, Certification Gold
- **EcoLodgeDjerba** - 110 kWh, Certification Silver
- **CampementEcologique** - 50 kWh, Certification Gold

### Transports Disponibles
- **TrainExpress** - 45 kg CO2
- **BusElectrique** - 25 kg CO2
- **VeloPartage** - 0 kg CO2
- **CovoiturageLocal** - 35 kg CO2
- **AvionLowCost** - 250 kg CO2

### Activités Disponibles
- **RandonnéeAtlas** - Faible impact
- **PlongeeRecif** - Faible impact, sensibilisation
- **TrekkingDesert** - Faible impact
- **VisiteMedina** - Préservation patrimoine
- **ObservationOiseaux** - Très faible impact

---

## 🎯 Objectifs Pédagogiques

Cette application démontre:

✅ **Web Sémantique**
- Ontologie RDF/OWL complète
- Requêtes SPARQL avancées
- Raisonnement sur les données

✅ **Intelligence Artificielle**
- Système de recommandation multi-critères
- Scoring et pondération
- Personnalisation utilisateur

✅ **Développement Full-Stack**
- Backend Flask avec API REST
- Frontend moderne responsive
- Architecture modulaire

✅ **Visualisation de Données**
- Graphiques interactifs
- Tableaux de bord
- Analyses multidimensionnelles

✅ **Développement Durable**
- Calcul d'empreinte carbone
- Promotion du tourisme responsable
- Sensibilisation écologique

---

## 📚 Ressources

- **README.md** - Documentation complète
- **GUIDE_UTILISATION.md** - Guide détaillé
- **ARCHITECTURE.md** - Architecture technique
- **Code source** - Commenté et structuré

---

## 🚀 Prochaines Étapes

1. ✅ Lancer l'application
2. ✅ Tester les fonctionnalités
3. ✅ Explorer l'ontologie
4. ✅ Générer des recommandations
5. ✅ Analyser les visualisations
6. 📝 Personnaliser avec vos données
7. 🔧 Étendre les fonctionnalités
8. 🌍 Déployer en production

---

**Bon voyage écologique! 🌍🌱✨**
