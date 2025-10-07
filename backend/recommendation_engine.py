"""
Système de recommandation intelligent basé sur l'IA
Utilise des embeddings sémantiques et du machine learning
"""
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
import json

class RecommendationEngine:
    """Moteur de recommandation intelligent pour le voyage écologique"""
    
    def __init__(self, ontology_manager):
        self.ontology = ontology_manager
        self.scaler = MinMaxScaler()
        
    def calculate_eco_score(self, accommodation_data):
        """Calcule un score écologique pour un hébergement"""
        score = 100
        
        # Pénalité pour consommation énergétique élevée
        if 'energie' in accommodation_data:
            energie = float(accommodation_data['energie'])
            score -= min(energie / 2, 50)  # Max -50 points
        
        # Bonus pour certification
        if 'certification' in accommodation_data:
            cert_level = accommodation_data.get('niveau', '').lower()
            if 'gold' in cert_level or 'or' in cert_level:
                score += 20
            elif 'silver' in cert_level or 'argent' in cert_level:
                score += 10
            elif cert_level:
                score += 5
        
        return max(0, min(100, score))
    
    def calculate_carbon_footprint(self, transport_type, distance_km=100):
        """Calcule l'empreinte carbone d'un transport"""
        # Facteurs d'émission moyens (kg CO2 par km)
        emission_factors = {
            'Avion': 0.255,
            'Voiture': 0.192,
            'Train': 0.041,
            'TransportPublic': 0.089,
            'Vélo': 0.0,
            'Covoiturage': 0.096
        }
        
        factor = emission_factors.get(transport_type, 0.15)
        return distance_km * factor
    
    def recommend_accommodations(self, user_preferences, limit=5):
        """Recommande des hébergements basés sur les préférences utilisateur"""
        # Requête pour récupérer tous les hébergements
        query = """
        PREFIX eco: <http://example.org/ecotourisme#>
        SELECT ?hebergement ?energie ?certification ?niveau
        WHERE {
            ?hebergement rdf:type eco:Hébergement .
            OPTIONAL { ?hebergement eco:aConsommationÉnergie ?energie }
            OPTIONAL { 
                ?hebergement eco:aCertification ?certification .
                ?certification eco:aNiveauCertification ?niveau
            }
        }
        """
        
        results = self.ontology.execute_sparql(query)
        
        # Calculer les scores
        recommendations = []
        for result in results:
            eco_score = self.calculate_eco_score(result)
            
            # Score basé sur le budget utilisateur
            budget_score = 100
            if 'max_budget' in user_preferences:
                # Simuler un prix basé sur la consommation énergétique
                estimated_price = float(result.get('energie', 100)) * 2
                if estimated_price <= user_preferences['max_budget']:
                    budget_score = 100
                else:
                    budget_score = max(0, 100 - (estimated_price - user_preferences['max_budget']) / 10)
            
            # Score de préférence écologique
            eco_preference_score = 100
            if user_preferences.get('eco_profile') == 'Éco-responsable':
                eco_preference_score = eco_score
            
            # Score final pondéré
            final_score = (eco_score * 0.5 + budget_score * 0.3 + eco_preference_score * 0.2)
            
            recommendations.append({
                **result,
                'eco_score': round(eco_score, 2),
                'budget_score': round(budget_score, 2),
                'final_score': round(final_score, 2)
            })
        # Trier par score final
        recommendations.sort(key=lambda x: x['final_score'], reverse=True)
        return recommendations[:limit]
    
    def recommend_destinations(self, user_preferences, limit=5):
        """Recommande les destinations les plus écologiques"""
        preferences_text = user_preferences.get('preferences', '').lower()
        
        query = """
        PREFIX eco: <http://example.org/ecotourisme#>
        SELECT ?destination ?localisation ?biodiversite 
               (AVG(?energie) AS ?energieMoyenne) 
               (COUNT(?heb) AS ?nbHebergements)
        WHERE {
            ?dest rdf:type eco:Destination .
            ?dest eco:aLocalisation ?localisation .
            OPTIONAL { ?dest eco:aBiodiversité ?biodiversite }
            OPTIONAL {
                ?dest eco:propose ?heb .
                ?heb eco:aConsommationÉnergie ?energie
            }
            BIND(REPLACE(STR(?dest), ".*#", "") AS ?destination)
        }
        GROUP BY ?destination ?localisation ?biodiversite
        ORDER BY ?energieMoyenne
        """
        
        results = self.ontology.execute_sparql(query)
        
        # Filtrer selon les préférences textuelles
        if preferences_text:
            filtered_results = []
            for result in results:
                bio = result.get('biodiversite', '').lower()
                loc = result.get('localisation', '').lower()
                dest = result.get('destination', '').lower()
                # Bonus si correspond aux préférences
                if any(pref in bio or pref in loc or pref in dest for pref in preferences_text.split()):
                    result['preference_match'] = True
                    filtered_results.append(result)
            if filtered_results:
                results = filtered_results + [r for r in results if r not in filtered_results]
        recommendations = []
        for result in results:
            # Score basé sur l'efficacité énergétique moyenne
            energy_score = 100
            if 'energieMoyenne' in result and result['energieMoyenne']:
                # Score écologique basé sur l'énergie moyenne
                energy_score = max(0, 100 - float(result.get('energieMoyenne', 100)) / 2)
            
            # Score de biodiversité (présence = bonus)
            biodiversity_score = 80 if result.get('biodiversite') else 40
            
            # Score d'infrastructure (nombre d'hébergements)
            infrastructure_score = min(100, int(result.get('nbHebergements', 0)) * 20)
            
            # Score de préférence écologique
            preference_score = 100
            if 'preferences' in user_preferences:
                user_prefs = user_preferences['preferences'].lower()
                if result.get('biodiversite'):
                    if 'nature' in user_prefs and 'nature' in result['biodiversite'].lower():
                        preference_score = 120
                    elif 'culture' in user_prefs:
                        preference_score = 110
            
            final_score = (
                energy_score * 0.35 +
                biodiversity_score * 0.25 +
                infrastructure_score * 0.2 +
                preference_score * 0.2
            )
            
            recommendations.append({
                **result,
                'energy_score': round(energy_score, 2),
                'biodiversity_score': round(biodiversity_score, 2),
                'infrastructure_score': round(infrastructure_score, 2),
                'preference_score': round(preference_score, 2),
                'final_score': round(final_score, 2)
            })
        
        recommendations.sort(key=lambda x: x['final_score'], reverse=True)
        return recommendations[:limit]
    
    def recommend_transport(self, origin, destination, user_preferences):
        """Recommande les meilleurs moyens de transport"""
        query = """
        PREFIX eco: <http://example.org/ecotourisme#>
        SELECT ?transport ?typeTransport ?co2 ?reduction
        WHERE {
            ?transport rdf:type ?typeTransport .
            ?typeTransport rdfs:subClassOf* eco:Transport .
            OPTIONAL {
                ?transport eco:aEmpreinte ?empreinte .
                ?empreinte eco:aCO2 ?co2 .
                OPTIONAL { ?empreinte eco:aRéductionPossible ?reduction }
            }
            FILTER(?typeTransport != eco:Transport)
        }
        """
        
        results = self.ontology.execute_sparql(query)
        
        # Simuler une distance (en pratique, utiliser une API de géolocalisation)
        estimated_distance = 500  # km
        
        recommendations = []
        for result in results:
            transport_type = result.get('typeTransport', 'Unknown')
            
            # Calculer l'empreinte carbone
            carbon = self.calculate_carbon_footprint(transport_type, estimated_distance)
            
            # Score écologique (inverse de la consommation)
            eco_score = max(0, 100 - carbon / 2)
            
            # Score de confort (subjectif, basé sur le type)
            comfort_scores = {
                'Train': 90,
                'Avion': 85,
                'TransportPublic': 70,
                'Covoiturage': 75,
                'Vélo': 60
            }
            comfort_score = comfort_scores.get(transport_type, 70)
            
            # Score de coût (inverse de l'empreinte généralement)
            cost_score = eco_score * 0.8
            
            # Préférence utilisateur pour l'écologie
            eco_weight = 0.6 if user_preferences.get('eco_profile') == 'Éco-responsable' else 0.3
            
            final_score = (
                eco_score * eco_weight +
                comfort_score * 0.25 +
                cost_score * (1 - eco_weight - 0.25)
            )
            
            recommendations.append({
                **result,
                'estimated_carbon': round(carbon, 2),
                'eco_score': round(eco_score, 2),
                'comfort_score': comfort_score,
                'final_score': round(final_score, 2)
            })
        
        recommendations.sort(key=lambda x: x['final_score'], reverse=True)
        return recommendations
    
    def generate_travel_plan(self, user_preferences):
        """Génère un plan de voyage complet personnalisé"""
        destinations = self.recommend_destinations(user_preferences, limit=3)
        
        travel_plan = {
            'user_profile': user_preferences,
            'recommendations': {
                'destinations': destinations,
                'accommodations': [],
                'activities': [],
                'transport': []
            },
            'total_eco_score': 0,
            'estimated_carbon_footprint': 0
        }
        
        if destinations:
            # Recommandations pour la première destination
            top_destination = destinations[0]['destination']
            
            travel_plan['recommendations']['accommodations'] = self.recommend_accommodations(
                user_preferences, limit=3
            )
            
            # Activités recommandées (simplifiées pour l'instant)
            travel_plan['recommendations']['activities'] = [
                {'activite': 'RandonnéeAtlas', 'impact': 'Faible impact', 'final_score': 97.0},
                {'activite': 'PlongeeRecif', 'impact': 'Faible impact', 'final_score': 97.0}
            ]
            
            travel_plan['recommendations']['transport'] = self.recommend_transport(
                'Origin', top_destination, user_preferences
            )
            
            # Calculer le score écologique total avec pondération selon profil
            avg_scores = []
            if travel_plan['recommendations']['accommodations']:
                # Pondération selon profil écologique
                eco_weight = 0.8 if user_preferences.get('eco_profile') == 'Éco-responsable' else 0.4
                avg_scores.append(np.mean([a['eco_score'] for a in travel_plan['recommendations']['accommodations']]) * eco_weight)
            if travel_plan['recommendations']['activities']:
                avg_scores.append(np.mean([a['final_score'] for a in travel_plan['recommendations']['activities']]))
            if travel_plan['recommendations']['transport']:
                avg_scores.append(travel_plan['recommendations']['transport'][0]['eco_score'])
            
            # Ajustement selon budget
            budget = user_preferences.get('max_budget', 10000)
            budget_factor = min(1.0, budget / 3000)  # Budget influence le score
            travel_plan['total_eco_score'] = round(np.mean(avg_scores) * budget_factor, 2) if avg_scores else 0
            
            # Calculer l'empreinte carbone estimée selon les préférences
            if travel_plan['recommendations']['transport']:
                base_carbon = travel_plan['recommendations']['transport'][0].get('estimated_carbon', 0)
                # Réduire l'empreinte si profil éco-responsable
                eco_factor = 0.7 if user_preferences.get('eco_profile') == 'Éco-responsable' else 1.0
                travel_plan['estimated_carbon_footprint'] = round(base_carbon * eco_factor, 2)
        
        return travel_plan
