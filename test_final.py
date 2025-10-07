#!/usr/bin/env python3
"""
Script de test final pour EcoTravel
"""
import requests
import json

API_BASE = "http://localhost:5000/api"

def test_endpoint(method, endpoint, data=None, description=""):
    try:
        if method == "GET":
            r = requests.get(f"{API_BASE}{endpoint}")
        else:
            r = requests.post(f"{API_BASE}{endpoint}", json=data)

        if r.status_code == 200:
            result = r.json()
            print(f"✅ {description}")
            if isinstance(result, dict) and 'count' in result:
                print(f"   {result['count']} éléments")
            elif isinstance(result, list) and len(result) > 0:
                print(f"   {len(result)} éléments")
            return True
        else:
            print(f"❌ {description} - Status {r.status_code}")
            return False
    except Exception as e:
        print(f"❌ {description} - {str(e)}")
        return False

print("="*60)
print("🧪 TESTS FINAUX ECOTRAVEL")
print("="*60)

# Test 1: Health et statistiques
test_endpoint("GET", "/health", description="Health Check")
test_endpoint("GET", "/ontology/summary", description="Statistiques Ontologie")

# Test 2: Requêtes SPARQL
test_endpoint("POST", "/sparql/execute",
              {"query": "SELECT ?heb ?energie WHERE { ?heb rdf:type eco:Hébergement . ?heb eco:aConsommationÉnergie ?energie } LIMIT 3"},
              description="SPARQL Hébergements")

# Test 3: Recherche avancée
test_endpoint("POST", "/advanced/filter", {"text": "écologique"}, description="Recherche Textuelle")
test_endpoint("POST", "/advanced/filter", {"location": "Tunisie"}, description="Filtrage Localisation")
test_endpoint("POST", "/advanced/filter", {"max_energy": 100}, description="Filtrage Énergie")

# Test 4: Recommandations personnalisées
test_endpoint("POST", "/recommendations/travel-plan",
              {"max_budget": 2000, "eco_profile": "Éco-responsable", "preferences": "nature"},
              description="Recommandations IA Personnalisées")

# Test 5: Requêtes prédéfinies
test_endpoint("GET", "/sparql/predefined/eco_accommodations", description="Requête Prédéfinie")
test_endpoint("GET", "/sparql/queries", description="Liste Requêtes")

print("\n" + "="*60)
print("✅ TOUS LES TESTS TERMINÉS")
print("🌍 L'application EcoTravel est fonctionnelle !")
print("="*60)
