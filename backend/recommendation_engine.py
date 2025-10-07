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
        """Recommande des destinations écologiques"""
        query = """
        PREFIX eco: <http://example.org/ecotourisme#>
        SELECT ?destination ?localisation ?biodiversite
               (COUNT(DISTINCT ?hebergement) AS ?nbHebergements)
               (AVG(?energie) AS ?energieMoyenne)
        WHERE {
            ?destination rdf:type eco:Destination .
            ?destination eco:aLocalisation ?localisation .
            OPTIONAL { ?destination eco:aBiodiversité ?biodiversite }
            OPTIONAL {
                ?destination eco:propose ?hebergement .
                ?hebergement eco:aConsommationÉnergie ?energie
            }
        }
        GROUP BY ?destination ?localisation ?biodiversite
        """
        
        results = self.ontology.execute_sparql(query)
        
        recommendations = []
        for result in results:
            # Score basé sur l'efficacité énergétique moyenne
            energy_score = 100
            if 'energieMoyenne' in result and result['energieMoyenne']:
                avg_energy = float(result['energieMoyenne'])
                energy_score = max(0, 100 - avg_energy / 2)
            
            # Score de biodiversité
            biodiversity_score = 80 if result.get('biodiversite') else 50
            
            # Score d'infrastructure
            infrastructure_score = min(100, int(result.get('nbHebergements', 0)) * 20)
            
            # Correspondance avec préférences utilisateur
            preference_score = 100
            if 'preferences' in user_preferences:
                user_prefs = user_preferences['preferences'].lower()
                if result.get('biodiversite'):
                    if 'nature' in user_prefs and 'nature' in result['biodiversite'].lower():
                        preference_score = 120
                    if 'culture' in user_prefs:
                        preference_score = 110
            
            final_score = (
                energy_score * 0.35 +
                biodiversity_score * 0.25 +
                infrastructure_score * 0.20 +
                preference_score * 0.20
            )
            
            recommendations.append({
                **result,
                'energy_score': round(energy_score, 2),
                'biodiversity_score': round(biodiversity_score, 2),
                'infrastructure_score': round(infrastructure_score, 2),
                'final_score': round(final_score, 2)
            })
        
        recommendations.sort(key=lambda x: x['final_score'], reverse=True)
        return recommendations[:limit]
    
    def recommend_activities(self, destination, user_preferences, limit=5):
        """Recommande des activités pour une destination"""
        query = f"""
        PREFIX eco: <http://example.org/ecotourisme#>
        SELECT ?activite ?authenticite ?impact ?communaute ?initiative
        WHERE {{
            ?activite rdf:type eco:ActivitéTouristique .
            OPTIONAL {{ ?activite eco:aAuthenticitéLocale ?authenticite }}
            OPTIONAL {{ ?activite eco:aImpactEnvironnemental ?impact }}
            OPTIONAL {{
                ?activite eco:implique ?communaute .
                ?communaute eco:aInitiativeDurable ?initiative
            }}
        }}
        """
        
        results = self.ontology.execute_sparql(query)
        
        recommendations = []
        for result in results:
            # Score d'impact environnemental
            impact_score = 100
            if 'impact' in result:
                impact_text = result['impact'].lower()
                if 'faible' in impact_text or 'low' in impact_text:
                    impact_score = 100
                elif 'moyen' in impact_text or 'medium' in impact_text:
                    impact_score = 60
                else:
                    impact_score = 30
            
            # Score d'authenticité
            authenticity_score = 90 if result.get('authenticite') else 50
            
            # Score de soutien communautaire
            community_score = 100 if result.get('initiative') else 50
            
            final_score = (
                impact_score * 0.4 +
                authenticity_score * 0.3 +
                community_score * 0.3
            )
            
            recommendations.append({
                **result,
                'impact_score': round(impact_score, 2),
                'authenticity_score': round(authenticity_score, 2),
                'community_score': round(community_score, 2),
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
            
            # Score écologique (inverse de l'empreinte)
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
            
            travel_plan['recommendations']['activities'] = self.recommend_activities(
                top_destination, user_preferences, limit=5
            )
            
            travel_plan['recommendations']['transport'] = self.recommend_transport(
                'Origin', top_destination, user_preferences
            )
            
            # Calculer le score écologique total
            avg_scores = []
            if travel_plan['recommendations']['accommodations']:
                avg_scores.append(np.mean([a['eco_score'] for a in travel_plan['recommendations']['accommodations']]))
            if travel_plan['recommendations']['activities']:
                avg_scores.append(np.mean([a['final_score'] for a in travel_plan['recommendations']['activities']]))
            if travel_plan['recommendations']['transport']:
                avg_scores.append(travel_plan['recommendations']['transport'][0]['eco_score'])
            
            travel_plan['total_eco_score'] = round(np.mean(avg_scores), 2) if avg_scores else 0
            
            # Calculer l'empreinte carbone estimée
            if travel_plan['recommendations']['transport']:
                travel_plan['estimated_carbon_footprint'] = travel_plan['recommendations']['transport'][0].get('estimated_carbon', 0)
        
        return travel_plan
