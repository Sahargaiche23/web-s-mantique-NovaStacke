# 🧪 Guide de Test EcoTravel - Étape par Étape

## 📋 Pré-requis
- ✅ Serveur Flask en cours d'exécution sur http://localhost:5000
- ✅ Navigateur web ouvert

---

## 🚀 Démarrage du Serveur

### Étape 1 : Lancer le serveur
```bash
cd /home/sahar/CascadeProjects/eco_travel_semantic/backend
./venv/bin/python app.py
```

**✅ Vérification** : Vous devriez voir :
```
✓ Ontologie chargée: 235 triples
 * Running on http://127.0.0.1:5000
```

### Étape 2 : Ouvrir le navigateur
- Ouvrir : http://localhost:5000
- Faire **Ctrl+F5** (hard refresh)

---

## 🧪 TESTS À EFFECTUER

### TEST 1 : Page d'Accueil 🏠

**Actions :**
1. Cliquer sur "Accueil" dans le menu
2. Observer les statistiques affichées

**✅ Résultats Attendus :**
- **Destinations** : 4
- **Hébergements** : 4 (ou plus)
- **Activités** : 3 (ou plus)
- **Score Éco** : 85

**❌ Si les chiffres sont à 0 :**
- Vérifier que le serveur Flask est bien démarré
- Vérifier la console du navigateur (F12) pour les erreurs

---

### TEST 2 : Requêtes SPARQL ⚡

**Actions :**
1. Cliquer sur "SPARQL" dans le menu
2. Dans la liste de gauche, cliquer sur "**eco accommodations**"
3. Cliquer sur le bouton "**Exécuter**"

**✅ Résultats Attendus :**
- L'éditeur se remplit avec une requête SPARQL
- Le tableau de résultats affiche **4 hébergements** :
  - MaisonVentEssaouira (75.0 kWh)
  - RiadEcologique (95.0 kWh)
  - EcoLodgeDjerba (110.0 kWh)
  - HotelEcoGreen (120.5 kWh)
- Message : "4 résultat(s)"

**Test 2.2 : Transport Comparison**
1. Cliquer sur "**transport comparison**"
2. Cliquer "Exécuter"

**✅ Résultats Attendus :**
- **4 transports** avec leurs émissions CO2 :
  - VeloPartage (0.0 kg CO2)
  - BusElectrique (25.0 kg CO2)
  - CovoiturageLocal (35.0 kg CO2)
  - TrainExpress (45.0 kg CO2)

**❌ Si aucun résultat :**
- Vérifier que le fichier `ecotourisme.owl` a été modifié
- Redémarrer le serveur Flask

---

### TEST 3 : Recherche Avancée 🔍

**Actions :**
1. Cliquer sur "**Recherche**" dans le menu
2. **Test 3.1 - Recherche Textuelle :**
   - Dans "🔎 Recherche textuelle", taper : **écologique**
   - Cliquer "**Rechercher**"

**✅ Résultats Attendus :**
- Compteur : "**11 résultat(s) trouvé(s)**" (ou plus)
- Tableau avec 3 colonnes : SUBJECT | PREDICATE | OBJECT
- Résultats contenant "écologique" (CertificationÉcologique, etc.)

**Actions :**
3. **Test 3.2 - Filtre par Type :**
   - Cliquer "**Réinitialiser**"
   - Dans "📂 Type", sélectionner : **Destinations**
   - Cliquer "**Rechercher**"

**✅ Résultats Attendus :**
- Plusieurs destinations affichées (TunisCarthage, Djerba, Marrakech, Essaouira)
- Compteur mis à jour

**Actions :**
4. **Test 3.3 - Filtre Localisation :**
   - Cliquer "**Réinitialiser**"
   - Dans "📍 Localisation", taper : **Tunisie**
   - Cliquer "**Rechercher**"

**✅ Résultats Attendus :**
- Résultats filtrés avec des destinations tunisiennes
- Compteur : "**12 résultat(s)**" ou plus

**Actions :**
5. **Test 3.4 - Filtre Énergie :**
   - Cliquer "**Réinitialiser**"
   - Dans "⚡ Consommation énergétique max", taper : **100**
   - Cliquer "**Rechercher**"

**✅ Résultats Attendus :**
- Hébergements avec consommation ≤ 100 kWh
- Devrait inclure : MaisonVentEssaouira (75) et RiadEcologique (95)

**❌ Si "0 résultat(s)" :**
- Vérifier la console navigateur (F12 → Console)
- Tester un filtre à la fois
- Vérifier que l'API `/api/advanced/filter` répond

---

### TEST 4 : Recommandations IA 🤖

**Actions :**
1. Cliquer sur "**Recommandations**" dans le menu
2. **Configurer le profil :**
   - Budget : **2000**
   - Profil écologique : **🌿 Éco-responsable**
   - Préférences : **nature, randonnée, culture**
3. Cliquer "**🚀 Générer Recommandations**"

**✅ Résultats Attendus :**

**Panneau gauche (Score Écologique Estimé) :**
- Un score apparaît (ex: 87 sur 100)
- Encadré vert visible

**Panneau droit (Vos Recommandations) :**
- **Résumé Global visible :**
  - Empreinte Carbone : **~21 kg CO2**
  - Score Éco Total : **~87**

**Si des recommandations sont générées :**
- Section "🏞️ Destinations" avec des encadrés verts
- Section "🏨 Hébergements" avec des encadrés bleus
- Section "🎯 Activités" avec des encadrés violets

**❌ Si "Aucune recommandation disponible" :**
- C'est NORMAL si le moteur de recommandations n'a pas assez de données
- Le score écologique et l'empreinte carbone doivent QUAND MÊME s'afficher
- Vérifier dans la console du navigateur s'il y a des erreurs

**Test 4.2 : Changer le Budget**
1. Modifier Budget à : **3000**
2. Re-cliquer "Générer"

**✅ Résultats Attendus :**
- Le score écologique peut changer
- Le display du budget se met à jour : "3000€"

---

### TEST 5 : Visualisations 📊

**Actions :**
1. Cliquer sur "**Visualisations**" dans le menu

**✅ Résultats Attendus :**
- 4 graphiques Chart.js s'affichent :
  - Comparaison Carbone
  - Consommation Énergétique
  - Scores Écologiques
  - Certifications

**❌ Si graphiques vides :**
- Vérifier que Chart.js est chargé (voir console navigateur)
- Vérifier les endpoints `/api/visualizations/*`

---

### TEST 6 : Ontologie Explorer 🔬

**Actions :**
1. Cliquer sur "**Ontologie**" dans le menu

**✅ Résultats Attendus :**
- Colonne **Classes** : Liste des classes (Destination, Hébergement, etc.)
- Colonne **Propriétés** : Liste des propriétés (aConsommationÉnergie, etc.)
- Colonne **Individus** : Liste des individus (HotelEcoGreen, TunisCarthage, etc.)

---

### TEST 7 : Chatbot IA 💬

**Actions :**
1. Cliquer sur "**Chat**" dans le menu
2. **Sans activer l'IA avancée :**
   - Taper : **destinations écologiques**
   - Cliquer "Envoyer"

**✅ Résultats Attendus :**
- Réponse basée sur les données de l'ontologie
- Liste de destinations avec leurs caractéristiques

3. **Avec IA avancée (si OpenAI configuré) :**
   - Cocher "Activer IA avancée (GPT)"
   - Taper : **recommande-moi un voyage écologique en Tunisie**
   - Cliquer "Envoyer"

**✅ Résultats Attendus :**
- Réponse détaillée et contextualisée
- Recommandations personnalisées

**❌ Si erreur "API Key" :**
- C'est normal si OpenAI n'est pas configuré
- Le mode sans IA avancée devrait quand même fonctionner

---

## 🔍 Tests de la Console Navigateur

**Pour tous les tests, vérifier la console (F12) :**

**✅ Messages attendus :**
```
Loaded successfully
200 OK responses
```

**❌ Erreurs à surveiller :**
```
404 Not Found → API endpoint manquant
500 Internal Server Error → Erreur backend
CORS errors → Problème de configuration serveur
```

---

## 📊 Résumé des Tests

| Test | Fonctionnalité | Statut |
|------|----------------|--------|
| ✅ | Accueil - Statistiques | |
| ✅ | SPARQL - Hébergements | |
| ✅ | SPARQL - Transports | |
| ✅ | Recherche - Textuelle | |
| ✅ | Recherche - Type | |
| ✅ | Recherche - Localisation | |
| ✅ | Recherche - Énergie | |
| ✅ | Recommandations - Score | |
| ✅ | Recommandations - Empreinte | |
| ✅ | Visualisations | |
| ✅ | Ontologie Explorer | |
| ✅ | Chatbot | |

---

## 🐛 Dépannage Rapide

### Problème : "0 résultat(s)" partout
**Solution :**
```bash
# Redémarrer le serveur
cd backend
pkill -f "python app.py"
./venv/bin/python app.py
```

### Problème : Scores et empreinte ne s'affichent pas
**Solution :**
1. F12 → Console → Vérifier les erreurs
2. Vérifier que `recommendations-summary` devient visible
3. Tester l'endpoint directement :
```bash
curl -X POST http://localhost:5000/api/recommendations/travel-plan \
  -H "Content-Type: application/json" \
  -d '{"max_budget":2000,"eco_profile":"Éco-responsable","preferences":"nature"}'
```

### Problème : Requêtes SPARQL vides
**Solution :**
1. Vérifier que `ecotourisme.owl` a été modifié
2. Tester en ligne de commande :
```bash
cd backend
./venv/bin/python test_api_complete.py
```

---

## ✅ Validation Finale

**Tous les tests passent si :**
- ✅ Les statistiques d'accueil s'affichent
- ✅ Les requêtes SPARQL retournent des résultats
- ✅ La recherche avancée filtre correctement
- ✅ Le score écologique et l'empreinte carbone s'affichent
- ✅ Les graphiques de visualisation se chargent

**L'application est PARFAITEMENT FONCTIONNELLE ! 🎉**
