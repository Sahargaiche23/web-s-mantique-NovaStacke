#!/usr/bin/env python3
"""
Test final des filtres avancés
"""
import requests
import json

API_BASE = "http://localhost:5000/api"

def test_filter(filter_data, name):
    try:
        r = requests.post(f"{API_BASE}/advanced/filter", json=filter_data)
        if r.status_code == 200:
            data = r.json()
            results = data.get('results', [])
            print(f"✅ {name}: {len(results)} résultats")
            if results:
                # Afficher quelques exemples
                for i, res in enumerate(results[:2]):
                    entity = res.get('entity', 'N/A')
                    entity_type = res.get('type', 'N/A')
                    localisation = res.get('localisation', 'N/A')
                    print(f"     - {entity} ({entity_type}) - {localisation}")
            return True
        else:
            print(f"❌ {name}: Status {r.status_code}")
            return False
    except Exception as e:
        print(f"❌ {name}: {str(e)}")
        return False

print("="*60)
print("🧪 TEST FINAL DES FILTRES AVANCÉS")
print("="*60)

# Test 1: Filtre par type - Destinations
test_filter({"entity_type": "Destination"}, "Filtre Destinations")

# Test 2: Filtre par type - Hébergements
test_filter({"entity_type": "Hébergement"}, "Filtre Hébergements")

# Test 3: Filtre par type - Activités
test_filter({"entity_type": "ActivitéTouristique"}, "Filtre Activités")

# Test 4: Filtre par type - Transports
test_filter({"entity_type": "Transport"}, "Filtre Transports")

# Test 5: Filtre par localisation
test_filter({"location": "Tunisie"}, "Filtre Localisation (Tunisie)")

# Test 6: Filtre par énergie max
test_filter({"max_energy": 100}, "Filtre Énergie max (100)")

# Test 7: Combinaison - Type + Localisation
test_filter({"entity_type": "Destination", "location": "Maroc"}, "Filtre Type + Localisation")

# Test 8: Combinaison - Tous les filtres
test_filter({
    "entity_type": "Hébergement",
    "max_energy": 100,
    "location": "Essaouira"
}, "Combinaison Tous Filtres")

print("\n" + "="*60)
print("✅ TESTS TERMINÉS")
print("="*60)
