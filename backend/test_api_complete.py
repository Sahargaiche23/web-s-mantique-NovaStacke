#!/usr/bin/env python3
"""
Script de test complet pour l'API EcoTravel
"""
import requests
import json

API_BASE = "http://localhost:5000/api"

def print_test(name, success, details=""):
    status = "✅ PASS" if success else "❌ FAIL"
    print(f"{status} | {name}")
    if details:
        print(f"     {details}")

print("="*70)
print("🧪 TESTS API ECOTRAVEL")
print("="*70)

# TEST 1: Health Check
print("\n📋 Test 1: Health Check")
try:
    r = requests.get(f"{API_BASE}/health")
    data = r.json()
    print_test("Health Check", r.status_code == 200, f"Triples: {data.get('total_triples', 0)}")
except Exception as e:
    print_test("Health Check", False, str(e))

# TEST 2: Ontology Summary
print("\n📋 Test 2: Ontology Summary")
try:
    r = requests.get(f"{API_BASE}/ontology/summary")
    data = r.json()
    if isinstance(data, list) and len(data) > 0:
        data = data[0]
    print_test("Ontology Summary", r.status_code == 200)
    print(f"     Destinations: {data.get('nbDestinations', 0)}")
    print(f"     Hébergements: {data.get('nbHebergements', 0)}")
    print(f"     Activités: {data.get('nbActivites', 0)}")
except Exception as e:
    print_test("Ontology Summary", False, str(e))

# TEST 3: SPARQL Query - Hébergements
print("\n📋 Test 3: SPARQL - Hébergements avec énergie")
try:
    query = """
    SELECT ?heb ?energie WHERE {
      ?heb rdf:type eco:Hébergement .
      ?heb eco:aConsommationÉnergie ?energie .
    }
    ORDER BY ?energie
    """
    r = requests.post(f"{API_BASE}/sparql/execute", json={"query": query})
    data = r.json()
    results = data.get('results', [])
    print_test("SPARQL Hébergements", len(results) > 0, f"{len(results)} hébergements trouvés")
    if results:
        for res in results[:3]:
            print(f"     - {res.get('heb')}: {res.get('energie')} kWh")
except Exception as e:
    print_test("SPARQL Hébergements", False, str(e))

# TEST 4: SPARQL Query - Transports et CO2
print("\n📋 Test 4: SPARQL - Transports et CO2")
try:
    query = """
    SELECT ?t ?co2 WHERE {
      ?t eco:aEmpreinte ?e .
      ?e eco:aCO2 ?co2 .
    }
    ORDER BY ?co2
    """
    r = requests.post(f"{API_BASE}/sparql/execute", json={"query": query})
    data = r.json()
    results = data.get('results', [])
    print_test("SPARQL Transports", len(results) > 0, f"{len(results)} transports trouvés")
    if results:
        for res in results[:3]:
            print(f"     - {res.get('t')}: {res.get('co2')} kg CO2")
except Exception as e:
    print_test("SPARQL Transports", False, str(e))

# TEST 5: Recherche Textuelle
print("\n📋 Test 5: Recherche Textuelle - 'écologique'")
try:
    r = requests.post(f"{API_BASE}/ontology/search", json={"text": "écologique"})
    data = r.json()
    results = data.get('results', [])
    print_test("Recherche Textuelle", len(results) > 0, f"{len(results)} résultats")
    if results:
        for res in results[:3]:
            print(f"     - {res.get('subject', res.get('entity', '-'))}")
except Exception as e:
    print_test("Recherche Textuelle", False, str(e))

# TEST 6: Filtrage Avancé
print("\n📋 Test 6: Filtrage Avancé - Localisation 'Tunisie'")
try:
    r = requests.post(f"{API_BASE}/advanced/filter", json={"location": "Tunisie"})
    data = r.json()
    results = data.get('results', [])
    print_test("Filtrage Avancé", len(results) > 0, f"{len(results)} résultats")
    if results:
        for res in results[:3]:
            print(f"     - {res.get('entity', '-')}: {res.get('type', '-')}")
except Exception as e:
    print_test("Filtrage Avancé", False, str(e))

# TEST 7: Filtrage avec Énergie Max
print("\n📋 Test 7: Filtrage - Énergie max 100 kWh")
try:
    r = requests.post(f"{API_BASE}/advanced/filter", json={"max_energy": 100})
    data = r.json()
    results = data.get('results', [])
    print_test("Filtrage Énergie", len(results) > 0, f"{len(results)} résultats")
    if results:
        for res in results[:3]:
            print(f"     - {res.get('entity', '-')}")
except Exception as e:
    print_test("Filtrage Énergie", False, str(e))

# TEST 8: Recommandations IA
print("\n📋 Test 8: Recommandations IA")
try:
    payload = {
        "max_budget": 2000,
        "eco_profile": "Éco-responsable",
        "preferences": "nature, randonnée"
    }
    r = requests.post(f"{API_BASE}/recommendations/travel-plan", json=payload)
    data = r.json()
    
    has_recommendations = (
        (data.get('destinations') and len(data['destinations']) > 0) or
        (data.get('accommodations') and len(data['accommodations']) > 0) or
        (data.get('activities') and len(data['activities']) > 0)
    )
    
    print_test("Recommandations IA", has_recommendations)
    
    if data.get('destinations'):
        print(f"     Destinations: {len(data['destinations'])}")
        for d in data['destinations'][:2]:
            print(f"       - {d}")
    
    if data.get('accommodations'):
        print(f"     Hébergements: {len(data['accommodations'])}")
        for a in data['accommodations'][:2]:
            print(f"       - {a}")
    
    if data.get('total_eco_score'):
        print(f"     Score Écologique: {data['total_eco_score']}")
    
    if data.get('estimated_carbon_footprint'):
        print(f"     Empreinte Carbone: {data['estimated_carbon_footprint']} kg CO2")
        
except Exception as e:
    print_test("Recommandations IA", False, str(e))

# TEST 9: Liste des requêtes prédéfinies
print("\n📋 Test 9: Requêtes SPARQL Prédéfinies")
try:
    r = requests.get(f"{API_BASE}/sparql/queries")
    data = r.json()
    queries = data.get('queries', [])
    print_test("Liste Requêtes", len(queries) > 0, f"{len(queries)} requêtes")
    if queries:
        for q in queries[:5]:
            print(f"     - {q}")
except Exception as e:
    print_test("Liste Requêtes", False, str(e))

# TEST 10: Exécution requête prédéfinie
print("\n📋 Test 10: Requête Prédéfinie - eco_accommodations")
try:
    r = requests.get(f"{API_BASE}/sparql/predefined/eco_accommodations")
    data = r.json()
    results = data.get('results', [])
    print_test("Requête Prédéfinie", len(results) > 0, f"{len(results)} résultats")
except Exception as e:
    print_test("Requête Prédéfinie", False, str(e))

print("\n" + "="*70)
print("✅ TESTS TERMINÉS")
print("="*70)
