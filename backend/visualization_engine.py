"""
Moteur de visualisation pour créer des graphiques et visualisations
"""
import numpy as np
from sparql_queries import SPARQLQueries

class VisualizationEngine:
    """Génère des données pour les visualisations"""
    
    def __init__(self, ontology_manager):
        self.ontology = ontology_manager
    
    def create_carbon_comparison_chart(self):
        """Crée les données pour un graphique de comparaison carbone"""
        results = self.ontology.execute_sparql(SPARQLQueries.QUERY_3_TRANSPORT_COMPARISON)
        
        chart_data = {
            'type': 'bar',
            'title': 'Comparaison des Émissions CO2 par Transport',
            'labels': [],
            'datasets': [{
                'label': 'Émissions CO2 (kg)',
                'data': [],
                'backgroundColor': []
            }]
        }
        
        # Couleurs basées sur l'impact
        colors = {
            'low': 'rgba(75, 192, 192, 0.8)',
            'medium': 'rgba(255, 206, 86, 0.8)',
            'high': 'rgba(255, 99, 132, 0.8)'
        }
        
        for result in results:
            transport_type = result.get('typeTransport', 'Unknown')
            co2 = float(result.get('co2', 0))
            
            chart_data['labels'].append(transport_type)
            chart_data['datasets'][0]['data'].append(co2)
            
            # Déterminer la couleur basée sur l'émission
            if co2 < 50:
                color = colors['low']
            elif co2 < 150:
                color = colors['medium']
            else:
                color = colors['high']
            
            chart_data['datasets'][0]['backgroundColor'].append(color)
        
        return chart_data
    
    def create_eco_scores_chart(self):
        """Crée les données pour un graphique des scores écologiques"""
        results = self.ontology.execute_sparql(SPARQLQueries.QUERY_15_ECO_SCORE)
        
        chart_data = {
            'type': 'radar',
            'title': 'Scores Écologiques des Destinations',
            'labels': ['Score Énergie', 'Score Certification', 'Score Activités', 'Score Total'],
            'datasets': []
        }
        
        colors = [
            'rgba(255, 99, 132, 0.6)',
            'rgba(54, 162, 235, 0.6)',
            'rgba(255, 206, 86, 0.6)',
            'rgba(75, 192, 192, 0.6)',
            'rgba(153, 102, 255, 0.6)'
        ]
        
        for idx, result in enumerate(results[:5]):  # Top 5 destinations
            destination = result.get('destination', f'Destination {idx+1}')
            
            dataset = {
                'label': destination,
                'data': [
                    float(result.get('scoreEnergie', 0)),
                    float(result.get('scoreCertification', 0)) * 10,
                    float(result.get('scoreActivites', 0)) * 5,
                    float(result.get('scoreTotal', 0)) / 10
                ],
                'backgroundColor': colors[idx % len(colors)],
                'borderColor': colors[idx % len(colors)].replace('0.6', '1'),
                'borderWidth': 2
            }
            
            chart_data['datasets'].append(dataset)
        
        return chart_data
    
    def create_destination_analysis_chart(self):
        """Crée les données pour l'analyse des destinations"""
        results = self.ontology.execute_sparql(SPARQLQueries.QUERY_8_DESTINATION_ANALYSIS)
        
        chart_data = {
            'type': 'bubble',
            'title': 'Analyse des Destinations Écologiques',
            'datasets': [{
                'label': 'Destinations',
                'data': []
            }]
        }
        
        for result in results:
            nb_hebergements = int(result.get('nbHebergements', 0))
            energie_moyenne = float(result.get('energieMoyenne', 100))
            nb_evenements = int(result.get('nbEvenements', 0))
            
            # Taille de la bulle basée sur le nombre d'événements
            bubble_size = max(5, nb_evenements * 10)
            
            chart_data['datasets'][0]['data'].append({
                'x': nb_hebergements,
                'y': energie_moyenne,
                'r': bubble_size,
                'label': result.get('destination', 'Unknown')
            })
        
        return chart_data
    
    def create_network_graph(self):
        """Crée un graphe de réseau de l'ontologie"""
        # Récupérer les classes et leurs relations
        classes = self.ontology.get_all_classes()
        properties = self.ontology.get_all_properties()
        
        nodes = []
        edges = []
        
        # Créer les nœuds pour les classes
        for idx, cls in enumerate(classes):
            class_name = cls.get('class', f'Class{idx}')
            nodes.append({
                'id': class_name,
                'label': class_name,
                'group': 'class',
                'size': 20
            })
        
        # Créer les arêtes pour les propriétés
        for prop in properties:
            domain = prop.get('domain', '')
            range_val = prop.get('range', '')
            property_name = prop.get('property', '')
            
            if domain and range_val:
                edges.append({
                    'from': domain,
                    'to': range_val,
                    'label': property_name,
                    'arrows': 'to'
                })
        
        return {
            'nodes': nodes,
            'edges': edges
        }
    
    def create_energy_consumption_chart(self):
        """Crée un graphique de consommation énergétique"""
        results = self.ontology.execute_sparql(SPARQLQueries.QUERY_1_ECO_ACCOMMODATIONS)
        
        chart_data = {
            'type': 'line',
            'title': 'Consommation Énergétique des Hébergements',
            'labels': [],
            'datasets': [{
                'label': 'Consommation Énergie (kWh)',
                'data': [],
                'borderColor': 'rgba(75, 192, 192, 1)',
                'backgroundColor': 'rgba(75, 192, 192, 0.2)',
                'fill': True,
                'tension': 0.4
            }]
        }
        
        for idx, result in enumerate(sorted(results, key=lambda x: float(x.get('energie', 0)))):
            hebergement = result.get('hebergement', f'Hébergement {idx+1}')
            energie = float(result.get('energie', 0))
            
            chart_data['labels'].append(hebergement)
            chart_data['datasets'][0]['data'].append(energie)
        
        return chart_data
    
    def create_certification_distribution(self):
        """Distribution des certifications écologiques"""
        results = self.ontology.execute_sparql(SPARQLQueries.QUERY_9_CERTIFICATIONS)
        
        chart_data = {
            'type': 'pie',
            'title': 'Distribution des Certifications Écologiques',
            'labels': [],
            'datasets': [{
                'data': [],
                'backgroundColor': [
                    'rgba(255, 206, 86, 0.8)',
                    'rgba(75, 192, 192, 0.8)',
                    'rgba(153, 102, 255, 0.8)',
                    'rgba(255, 159, 64, 0.8)'
                ]
            }]
        }
        
        for result in results:
            niveau = result.get('niveau', 'Unknown')
            nb_hebergements = int(result.get('nbHebergements', 0))
            
            chart_data['labels'].append(niveau)
            chart_data['datasets'][0]['data'].append(nb_hebergements)
        
        return chart_data
    
    def create_biodiversity_map_data(self):
        """Données pour une carte de biodiversité"""
        results = self.ontology.execute_sparql(SPARQLQueries.QUERY_2_BIODIVERSITY_DESTINATIONS)
        
        map_data = {
            'type': 'map',
            'title': 'Carte de Biodiversité des Destinations',
            'markers': []
        }
        
        # Coordonnées simulées (en pratique, utiliser une API de géocodage)
        coordinates = {
            'Tunisie': {'lat': 36.8065, 'lng': 10.1815},
            'Maroc': {'lat': 31.7917, 'lng': -7.0926},
            'Algérie': {'lat': 36.7538, 'lng': 3.0588}
        }
        
        for result in results:
            localisation = result.get('localisation', '')
            biodiversite = result.get('biodiversite', '')
            nb_activites = int(result.get('nbActivites', 0))
            
            coords = coordinates.get(localisation, {'lat': 0, 'lng': 0})
            
            map_data['markers'].append({
                'position': coords,
                'title': localisation,
                'description': biodiversite,
                'activities': nb_activites
            })
        
        return map_data
    
    def create_impact_comparison(self):
        """Comparaison d'impact environnemental"""
        results = self.ontology.execute_sparql(SPARQLQueries.QUERY_12_ENVIRONMENTAL_IMPACT)
        
        chart_data = {
            'type': 'horizontalBar',
            'title': 'Comparaison Impact Environnemental',
            'labels': [],
            'datasets': [
                {
                    'label': 'Énergie Moyenne',
                    'data': [],
                    'backgroundColor': 'rgba(255, 99, 132, 0.6)'
                },
                {
                    'label': 'Activités Faible Impact',
                    'data': [],
                    'backgroundColor': 'rgba(75, 192, 192, 0.6)'
                },
                {
                    'label': 'Certifications',
                    'data': [],
                    'backgroundColor': 'rgba(255, 206, 86, 0.6)'
                }
            ]
        }
        
        for result in results:
            destination = result.get('destination', 'Unknown')
            energie_moy = float(result.get('energieMoyenne', 0))
            nb_activites = int(result.get('nbActivitesFaibleImpact', 0))
            nb_certifications = int(result.get('nbCertifications', 0))
            
            chart_data['labels'].append(destination)
            chart_data['datasets'][0]['data'].append(energie_moy)
            chart_data['datasets'][1]['data'].append(nb_activites)
            chart_data['datasets'][2]['data'].append(nb_certifications)
        
        return chart_data
