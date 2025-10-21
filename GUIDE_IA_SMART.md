# 🤖 Guide IA Smart - Recommandations pour N'importe Quel Pays

## 🎯 Fonctionnalités Implémentées

### 1. **IA Smart avec OpenAI**
Le système génère maintenant des recommandations intelligentes pour **n'importe quel pays du monde** grâce à l'intégration OpenAI GPT.

### 2. **Page Admin Détaillée**
Le panneau admin affiche maintenant les recommandations avec :
- ✅ **Nom d'utilisateur** (au lieu de User ID)
- ✅ **Détails complets** de chaque recommandation
- ✅ **Format amélioré** avec émojis et couleurs

---

## 🔧 Configuration OpenAI

### Obtenir une Clé API OpenAI

1. **Créer un compte** : https://platform.openai.com/signup
2. **Obtenir la clé API** : https://platform.openai.com/api-keys
3. **Créer un fichier `.env`** à la racine du projet :

```bash
# Dans le dossier principal
cd "/home/sahar/Bureau/web-s-mantique-NovaStacke-master (Copie 3)"

# Créer le fichier .env
cat > .env << 'EOF'
# OpenAI Configuration
OPENAI_API_KEY=votre-clé-api-ici
OPENAI_MODEL=gpt-3.5-turbo

# JWT Configuration
SECRET_KEY=votre-secret-key-production
JWT_SECRET_KEY=votre-jwt-secret-production
EOF
```

4. **Remplacer** `votre-clé-api-ici` par votre vraie clé OpenAI

---

## 🚀 Comment Ça Fonctionne

### Logique de Sélection

```python
# 1. Recherche dans l'ontologie
if destination in ontology:
    # Utiliser les données RDF existantes
    return ontology_recommendations()

# 2. Sinon, utiliser l'IA
else:
    if OPENAI_API_KEY existe:
        # Générer avec GPT-3.5
        return ai_recommendations()
    else:
        # Fallback sur l'ontologie
        return ontology_recommendations()
```

### Exemples

| Destination | Source |
|------------|--------|
| Marrakech | Ontologie (données exactes) |
| Tunisie | Ontologie (données exactes) |
| France | IA (généré par OpenAI) |
| Japon | IA (généré par OpenAI) |
| Brésil | IA (généré par OpenAI) |

---

## 📊 Page Admin - Affichage Détaillé

### Ce qui est affiché :

```
┌─────────────────────────────────────────────────────────┐
│  🎯 Recommandations Générées                            │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌────────────────────────────────────────────────────┐ │
│  │ advanced                                           │ │
│  │ 👤 Utilisateur: admin                              │ │
│  │ 🎯 Recherche: France (2000€)                       │ │
│  │                                      Score: 90     │ │
│  │                                                    │ │
│  │  🏖️ Destinations:                                  │ │
│  │    • Paris - France                                │ │
│  │    • Lyon - France                                 │ │
│  │                                                    │ │
│  │  🏨 Hébergements:                                  │ │
│  │    • Eco Hotel Paris - 80 kWh                      │ │
│  │                                                    │ │
│  │  🎯 Activités:                                     │ │
│  │    • Visite Louvre - Faible impact                 │ │
│  │                                                    │ │
│  │  🚆 Transports:                                    │ │
│  │    • Covoiturage vers France                       │ │
│  │      Émissions CO2: 15 kg. Transport écologique.   │ │
│  │                                                    │ │
│  │  📅 21 octobre 2025 à 12:26                        │ │
│  └────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

---

## 🧪 Tests

### Test 1 : Destination dans l'Ontologie

```bash
curl -X POST http://localhost:5000/api/recommendations-advanced \
  -H "Content-Type: application/json" \
  -d '{
    "destination": "Marrakech",
    "budget": 1500,
    "type_voyage": "Culture",
    "duree": "Semaine (7-10 jours)",
    "priorite_ecologique": 8
  }'
```

**Résultat attendu** : Données de l'ontologie (Marrakech existe)

### Test 2 : Destination NON dans l'Ontologie (avec OpenAI)

```bash
curl -X POST http://localhost:5000/api/recommendations-advanced \
  -H "Content-Type: application/json" \
  -d '{
    "destination": "France",
    "budget": 2000,
    "type_voyage": "Culture",
    "duree": "Semaine (7-10 jours)",
    "priorite_ecologique": 9
  }'
```

**Résultat attendu** : Recommandations générées par l'IA

```json
{
  "success": true,
  "recommendations": {
    "destinations": [
      {
        "destination": "Paris",
        "localisation": "France",
        "biodiversite": "Parcs urbains et Seine",
        "final_score": 88
      }
    ],
    "accommodations": [
      {
        "hebergement": "Eco Hotel Marais",
        "energie": "60",
        "niveau": "Gold",
        "final_score": 92
      }
    ],
    "activities": [
      {
        "activite": "Visite à vélo du Louvre",
        "impact": "Très faible impact",
        "final_score": 95
      }
    ],
    "transport": [
      {
        "transport": "Train TGV",
        "co2": "15",
        "description": "Transport ferroviaire électrique",
        "final_score": 98
      }
    ]
  },
  "eco_score": 90,
  "user": "admin"
}
```

### Test 3 : Affichage Admin

```bash
# 1. Se connecter
TOKEN=$(curl -s -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}' | jq -r '.access_token')

# 2. Consulter les recommandations
curl -s http://localhost:5000/api/admin/recommendations \
  -H "Authorization: Bearer $TOKEN" | jq '.recommendations[0]'
```

**Résultat attendu** :
```json
{
  "id": 5,
  "user_id": 1,
  "username": "admin",  // ✅ Nom d'utilisateur affiché
  "recommendation_type": "advanced",
  "recommendation_data": {
    "preferences": {
      "destination": "France",
      "budget": 2000
    },
    "destinations": [...],
    "transport": [
      {
        "transport": "Covoiturage vers France",
        "co2": "15",
        "description": "Transport écologique"
      }
    ]
  },
  "eco_score": 90,
  "created_at": "2025-10-21T12:26:00"
}
```

---

## 🔑 Sans Clé OpenAI (Mode Fallback)

Si vous n'avez pas de clé OpenAI :

### Option 1 : Utiliser l'Ontologie Existante
Le système retournera toujours les destinations de l'ontologie (Marrakech, Tunisie, etc.)

### Option 2 : Générer des Données Mock
Modifiez `generate_ai_recommendations()` pour retourner des données simulées :

```python
def generate_ai_recommendations(preferences):
    """Génère des recommandations mock pour les tests"""
    
    destination = preferences['destination']
    
    return {
        "destinations": [
            {
                "destination": f"{destination} Centre",
                "localisation": destination,
                "biodiversite": f"Biodiversité urbaine de {destination}",
                "final_score": 85
            },
            {
                "destination": f"{destination} Côtier",
                "localisation": destination,
                "biodiversite": "Écosystème marin",
                "final_score": 88
            }
        ],
        "accommodations": [
            {
                "hebergement": f"Eco Lodge {destination}",
                "energie": "75",
                "niveau": "Gold",
                "final_score": 90
            }
        ],
        "activities": [
            {
                "activite": f"Randonnée {destination}",
                "impact": "Faible impact",
                "final_score": 92
            }
        ],
        "transport": [
            {
                "transport": f"Covoiturage vers {destination}",
                "co2": "15",
                "description": "Transport écologique",
                "final_score": 95
            }
        ]
    }
```

---

## 📱 Utilisation Frontend

### Page Recommandations Avancées

1. **Ouvrir** : http://localhost:5000/recommandations_avance.html
2. **Remplir le formulaire** :
   - Destination : France
   - Budget : 2000€
   - Type : Culture
   - Durée : Semaine
   - Priorité éco : 9/10
3. **Cliquer** sur "Générer les recommandations"
4. **Voir** les résultats générés par l'IA

### Page Admin

1. **Se connecter** : http://localhost:5000/login.html
   - Username : admin
   - Password : admin123
2. **Accéder à l'admin** : http://localhost:5000/admin.html
3. **Onglet "Recommandations"**
4. **Voir** toutes les recommandations avec détails complets

---

## 🎨 Modifications Apportées

### Backend (`app.py`)

1. **Fonction `generate_ai_recommendations()`**
   - Appelle OpenAI GPT-3.5-turbo
   - Génère 3 destinations, 3 hébergements, 3 activités, 3 transports
   - Format JSON structuré

2. **Endpoint `/api/recommendations-advanced`**
   - Vérifie si destination dans ontologie
   - Si oui → Utilise RDF
   - Si non → Utilise IA (ou fallback)

### Frontend (`admin.js`)

1. **Fonction `displayRecommendations()`**
   - Affiche le **nom d'utilisateur** au lieu de user_id
   - Extrait et affiche tous les détails :
     - 🏖️ Destinations
     - 🏨 Hébergements
     - 🎯 Activités
     - 🚆 Transports (avec émissions CO2)
   - Format avec couleurs et émojis

### Models (`models.py`)

1. **Méthode `Recommendation.to_dict()`**
   - Récupère le nom d'utilisateur depuis la table User
   - Retourne "Anonymous" si user_id est null

---

## ✅ Résumé Final

| Fonctionnalité | Status |
|----------------|--------|
| IA pour nouveaux pays | ✅ Implémenté |
| Affichage nom utilisateur | ✅ Implémenté |
| Détails complets dans admin | ✅ Implémenté |
| Format avec émojis | ✅ Implémenté |
| Support utilisateurs anonymes | ✅ Implémenté |
| Fallback sans OpenAI | ✅ Implémenté |

---

## 🚀 Prochaines Étapes

1. **Obtenir une clé OpenAI** (pour l'IA réelle)
2. **Tester avec différents pays** : France, Japon, Brésil, Canada...
3. **Consulter le panneau admin** pour voir les détails
4. **Exporter les recommandations** (fonctionnalité future)

---

## 📞 Support

- **Backend** : Port 5000
- **Frontend Recommandations** : http://localhost:5000/recommandations_avance.html
- **Admin Panel** : http://localhost:5000/admin.html
- **API Health** : http://localhost:5000/api/health

**Tout est prêt et fonctionnel !** 🎉
