#!/usr/bin/env python3
"""
Test des recommandations avec différents paramètres
"""
import requests
import json

API_BASE = "http://localhost:5000/api"

def test_recommendations(params, name):
    try:
        r = requests.post(f"{API_BASE}/recommendations/travel-plan", json=params)
        if r.status_code == 200:
            data = r.json()
            score = data.get('total_eco_score', 0)
            carbon = data.get('estimated_carbon_footprint', 0)
            print(f"✅ {name}: Score={score}, CO2={carbon}kg")
            return True
        else:
            print(f"❌ {name}: Status {r.status_code}")
            return False
    except Exception as e:
        print(f"❌ {name}: {str(e)}")
        return False

print("="*60)
print("🧪 TEST DES RECOMMANDATIONS PERSONNALISÉES")
print("="*60)

# Test 1: Profil Éco-responsable, budget élevé, préférences nature
test_recommendations({
    "max_budget": 3000,
    "eco_profile": "Éco-responsable",
    "preferences": "nature"
}, "Éco-responsable + Nature + Budget élevé")

# Test 2: Profil Modéré, budget faible, préférences culture
test_recommendations({
    "max_budget": 1000,
    "eco_profile": "Modéré",
    "preferences": "culture"
}, "Modéré + Culture + Budget faible")

# Test 3: Profil Flexible, budget moyen, préférences plage
test_recommendations({
    "max_budget": 2000,
    "eco_profile": "Flexible",
    "preferences": "plage"
}, "Flexible + Plage + Budget moyen")

# Test 4: Sans préférences
test_recommendations({
    "max_budget": 2500,
    "eco_profile": "Éco-responsable",
    "preferences": ""
}, "Éco-responsable + Sans préférences")

print("\n" + "="*60)
print("✅ TESTS TERMINÉS")
print("="*60)
