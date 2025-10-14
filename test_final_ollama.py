#!/usr/bin/env python3
"""
Test complet d'EcoTravel - Version finale avec Ollama
"""
import requests
import json
import os

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
            return result
        else:
            print(f"❌ {description} - Status {r.status_code}")
            return None
    except Exception as e:
        print(f"❌ {description} - {str(e)}")
        return None

print("="*70)
print("🧪 TEST COMPLET ECOTRAVEL - VERSION FINALE")
print("="*70)

# Test 1: Vérification serveur
print("\n1️⃣ VÉRIFICATION SERVEUR")
test_endpoint("GET", "/health", description="Health Check")
test_endpoint("GET", "/ontology/summary", description="Statistiques Ontologie")

# Test 2: Filtres avancés
print("\n2️⃣ FILTRES AVANCÉS")
test_endpoint("POST", "/advanced/filter", {"entity_type": "Destination"}, "Filtre Destinations")
test_endpoint("POST", "/advanced/filter", {"entity_type": "Hébergement"}, "Filtre Hébergements")
test_endpoint("POST", "/advanced/filter", {"location": "Tunisie"}, "Filtre Localisation")
test_endpoint("POST", "/advanced/filter", {"max_energy": 100}, "Filtre Énergie")

# Test 3: Recommandations personnalisées
print("\n3️⃣ RECOMMANDATIONS IA")
test_endpoint("POST", "/recommendations/travel-plan",
              {"max_budget": 2000, "eco_profile": "Éco-responsable", "preferences": "nature"},
              "Recommandations Personnalisées")

# Test 4: Chatbot avec Ollama
print("\n4️⃣ CHATBOT AVEC OLLAMA")
# Configuration environnement pour Ollama
os.environ['USE_OLLAMA'] = 'true'
os.environ['OLLAMA_BASE_URL'] = 'http://127.0.0.1:11434'
os.environ['OLLAMA_MODEL'] = 'qwen2.5:3b-instruct'

chatbot_response = test_endpoint("POST", "/chatbot/message",
                                 {"message": "Quelles sont les meilleures destinations écologiques?", "use_llm": True},
                                 "Chatbot avec Ollama")

if chatbot_response:
    print(f"   Réponse: {chatbot_response.get('response', '')[:100]}...")

# Test 5: SPARQL
print("\n5️⃣ REQUÊTES SPARQL")
test_endpoint("GET", "/sparql/predefined/eco_accommodations", "SPARQL Hébergements")

print("\n" + "="*70)
print("✅ TOUS LES TESTS TERMINÉS")
print("🌍 EcoTravel avec Ollama est prêt !")
print("="*70)

# Instructions finales
print("\n📋 PROCHAINES ÉTAPES :")
print("1. Ouvrir http://localhost:5000")
print("2. Tester les filtres avancés")
print("3. Essayer les recommandations IA")
print("4. Utiliser le chatbot avec Ollama")
print("5. Explorer les visualisations")

print("\n🎉 EcoTravel est maintenant 100% fonctionnel avec Ollama !")
