#!/usr/bin/env python3
"""
Test du dashboard amélioré avec statistiques en temps réel
"""
import requests
import json

API_BASE = "http://localhost:5000/api"

def test_dashboard():
    print("🧪 TEST DU DASHBOARD AMÉLIORÉ")
    print("="*50)

    try:
        # Test de l'endpoint dashboard/statistics
        print("📊 Test de l'endpoint dashboard/statistics...")
        response = requests.get(f"{API_BASE}/dashboard/statistics")
        data = response.json()

        if response.status_code == 200:
            print("✅ Endpoint dashboard/statistics fonctionne")

            # Afficher les statistiques principales
            print("📈 Statistiques principales:")
            print(f"   Total entités: {data.get('total_entities', 0)}")
            print(f"   Total triples: {data.get('total_triples', 0)}")
            print(f"   Score écologique: {data.get('eco_score', 0)}")
            print(f"   Empreinte carbone: {data.get('carbon_footprint', 0)} kg")

            # Afficher les statistiques par classe
            class_stats = data.get('class_statistics', {})
            print("🏗️ Statistiques par classe:")
            for class_name, stats in class_stats.items():
                print(f"   {class_name}: {stats.get('count', 0)} éléments")

                # Afficher quelques détails
                details = stats.get('details', [])
                if details:
                    print(f"     Exemples: {len(details)} éléments")
                    for detail in details[:2]:
                        if class_name == 'Destinations':
                            print(f"       • {detail.get('destination', 'N/A')} ({detail.get('localisation', 'N/A')})")
                        elif class_name == 'Hébergements':
                            print(f"       • {detail.get('hebergement', 'N/A')} ({detail.get('energie', 'N/A')} kWh)")
                        elif class_name == 'Activités':
                            print(f"       • {detail.get('activite', 'N/A')} ({detail.get('impact', 'N/A')})")
                        elif class_name == 'Transports':
                            print(f"       • {detail.get('transport', 'N/A')} ({detail.get('co2', 'N/A')} kg CO2)")
                        elif class_name == 'Certifications':
                            print(f"       • {detail.get('certification', 'N/A')} ({detail.get('niveau', 'N/A')})")

            return True
        else:
            print(f"❌ Erreur HTTP {response.status_code}")
            print(f"   Réponse: {data}")
            return False

    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return False

if __name__ == "__main__":
    success = test_dashboard()

    print("\n" + "="*50)
    if success:
        print("✅ Dashboard fonctionnel - Prêt pour l'interface!")
        print("🌐 Ouvrez http://localhost:5000 pour voir le dashboard en action")
    else:
        print("❌ Problèmes détectés - Vérifiez la configuration")
    print("="*50)
