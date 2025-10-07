"""
Application Flask principale - API REST pour l'écotourisme sémantique
"""
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import os
import sys
from dotenv import load_dotenv

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ontology_manager import OntologyManager
from sparql_queries import SPARQLQueries
from recommendation_engine import RecommendationEngine
from visualization_engine import VisualizationEngine
from ai_chatbot import EcoTravelChatbot
from openai import OpenAI

app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)

# Configuration
# Charger les variables d'environnement depuis .env à la racine du projet
project_root_env = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.env'))
if os.path.exists(project_root_env):
    load_dotenv(project_root_env)
else:
    # Fallback: charge depuis le cwd si présent
    load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
model_name = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

ONTOLOGY_PATH = os.path.join(os.path.dirname(__file__), '..', 'ontology', 'ecotourisme.owl')

# Initialisation
ontology = OntologyManager(ONTOLOGY_PATH)
ontology.load_ontology()
recommender = RecommendationEngine(ontology)
visualizer = VisualizationEngine(ontology)
chatbot = EcoTravelChatbot(ontology, api_key, model_name)

# ==================== ROUTES API ====================

@app.route('/')
def index():
    """Page d'accueil"""
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/health', methods=['GET'])
def health_check():
    """Vérification de l'état de l'API"""
    stats = ontology.get_statistics()
    return jsonify({
        'status': 'healthy',
        'ontology_loaded': len(ontology.graph) > 0,
        'statistics': stats
    })

# ==================== SPARQL QUERIES ====================

@app.route('/api/sparql/execute', methods=['POST'])
def execute_sparql():
    """Exécute une requête SPARQL personnalisée"""
    data = request.json
    query = data.get('query', '')
    
    if not query:
        return jsonify({'error': 'Query is required'}), 400
    
    try:
        results = ontology.execute_sparql(query)
        return jsonify({
            'success': True,
            'results': results,
            'count': len(results),
            'query_executed': query,
            'triple_count': len(ontology.graph)
        })
    except Exception as e:
        return jsonify({'error': str(e), 'query_executed': query}), 500

@app.route('/api/sparql/predefined/<query_name>', methods=['GET'])
def execute_predefined_query(query_name):
    """Exécute une requête SPARQL prédéfinie"""
    queries = SPARQLQueries.get_all_queries()
    
    if query_name not in queries:
        return jsonify({'error': 'Query not found'}), 404
    
    try:
        query_text = queries[query_name]
        results = ontology.execute_sparql(query_text)
        return jsonify({
            'success': True,
            'query_name': query_name,
            'query': query_text,
            'results': results,
            'count': len(results)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/sparql/queries', methods=['GET'])
def list_queries():
    """Liste toutes les requêtes SPARQL disponibles"""
    queries = SPARQLQueries.get_all_queries()
    return jsonify({
        'queries': list(queries.keys()),
        'count': len(queries)
    })

# ==================== ONTOLOGY EXPLORATION ====================

@app.route('/api/ontology/classes', methods=['GET'])
def get_classes():
    """Récupère toutes les classes de l'ontologie"""
    classes = ontology.get_all_classes()
    return jsonify({
        'classes': classes,
        'count': len(classes)
    })

@app.route('/api/ontology/properties', methods=['GET'])
def get_properties():
    """Récupère toutes les propriétés"""
    properties = ontology.get_all_properties()
    return jsonify({
        'properties': properties,
        'count': len(properties)
    })

@app.route('/api/ontology/individuals', methods=['GET'])
def get_individuals():
    """Récupère tous les individus"""
    individuals = ontology.get_all_individuals()
    return jsonify({
        'individuals': individuals,
        'count': len(individuals)
    })

@app.route('/api/ontology/individuals/<class_name>', methods=['GET'])
def get_individuals_by_class(class_name):
    """Récupère les individus d'une classe spécifique"""
    individuals = ontology.get_individuals_by_class(class_name)
    return jsonify({
        'class': class_name,
        'individuals': individuals,
        'count': len(individuals)
    })

@app.route('/api/ontology/search', methods=['POST'])
def search_ontology():
    """Recherche textuelle dans l'ontologie"""
    data = request.json
    search_text = data.get('text', '')
    
    if not search_text:
        return jsonify({'error': 'Search text is required'}), 400
    
    results = ontology.search_by_text(search_text)
    return jsonify({
        'search_text': search_text,
        'results': results,
        'count': len(results)
    })

@app.route('/api/ontology/related/<entity_name>', methods=['GET'])
def get_related_entities(entity_name):
    """Récupère les entités liées"""
    related = ontology.get_related_entities(entity_name)
    return jsonify({
        'entity': entity_name,
        'related': related,
        'count': len(related)
    })

@app.route('/api/ontology/statistics', methods=['GET'])
def get_statistics():
    """Statistiques de l'ontologie"""
    stats = ontology.get_statistics()
    return jsonify(stats)

@app.route('/api/ontology/summary', methods=['GET'])
def ontology_summary():
    """Retourne des compteurs détaillés par type d'entité"""
    query = """
    PREFIX eco: <http://example.org/ecotourisme#>
    SELECT (COUNT(DISTINCT ?dest) AS ?nbDestinations)
           (COUNT(DISTINCT ?heb) AS ?nbHebergements)
           (COUNT(DISTINCT ?act) AS ?nbActivites)
           (COUNT(DISTINCT ?trans) AS ?nbTransports)
    WHERE {
      OPTIONAL { ?dest rdf:type eco:Destination }
      OPTIONAL { ?heb rdf:type eco:Hébergement }
      OPTIONAL { ?act rdf:type eco:ActivitéTouristique }
      OPTIONAL { ?trans rdf:type ?t . ?t rdfs:subClassOf* eco:Transport }
    }
    """
    results = ontology.execute_sparql("""
    PREFIX eco: <http://example.org/ecotourisme#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    SELECT (COUNT(DISTINCT ?dest) AS ?nbDestinations)
           (COUNT(DISTINCT ?heb) AS ?nbHebergements)
           (COUNT(DISTINCT ?act) AS ?nbActivites)
           (COUNT(DISTINCT ?trans) AS ?nbTransports)
    WHERE {
      OPTIONAL { ?dest rdf:type eco:Destination }
      OPTIONAL { ?heb rdf:type eco:Hébergement }
      OPTIONAL { ?act rdf:type eco:ActivitéTouristique }
      OPTIONAL { ?trans rdf:type ?t . ?t rdfs:subClassOf* eco:Transport }
    }
    """)
    return jsonify(results[0] if results else {})

# ==================== RECOMMENDATIONS ====================

@app.route('/api/recommendations/accommodations', methods=['POST'])
def recommend_accommodations():
    """Recommande des hébergements"""
    user_prefs = request.json
    recommendations = recommender.recommend_accommodations(user_prefs)
    return jsonify({
        'recommendations': recommendations,
        'count': len(recommendations)
    })

@app.route('/api/recommendations/destinations', methods=['POST'])
def recommend_destinations():
    """Recommande des destinations"""
    user_prefs = request.json
    recommendations = recommender.recommend_destinations(user_prefs)
    return jsonify({
        'recommendations': recommendations,
        'count': len(recommendations)
    })

@app.route('/api/recommendations/activities', methods=['POST'])
def recommend_activities():
    """Recommande des activités"""
    data = request.json
    destination = data.get('destination', '')
    user_prefs = data.get('preferences', {})
    
    recommendations = recommender.recommend_activities(destination, user_prefs)
    return jsonify({
        'destination': destination,
        'recommendations': recommendations,
        'count': len(recommendations)
    })

@app.route('/api/recommendations/transport', methods=['POST'])
def recommend_transport():
    """Recommande des moyens de transport"""
    data = request.json
    origin = data.get('origin', '')
    destination = data.get('destination', '')
    user_prefs = data.get('preferences', {})
    
    recommendations = recommender.recommend_transport(origin, destination, user_prefs)
    return jsonify({
        'origin': origin,
        'destination': destination,
        'recommendations': recommendations,
        'count': len(recommendations)
    })

@app.route('/api/recommendations/travel-plan', methods=['POST'])
def generate_travel_plan():
    """Génère un plan de voyage complet"""
    user_prefs = request.json
    travel_plan = recommender.generate_travel_plan(user_prefs)
    return jsonify(travel_plan)

# ==================== VISUALIZATIONS ====================

@app.route('/api/visualizations/carbon-comparison', methods=['GET'])
def carbon_comparison():
    """Graphique de comparaison des émissions carbone"""
    chart_data = visualizer.create_carbon_comparison_chart()
    return jsonify(chart_data)

@app.route('/api/visualizations/eco-scores', methods=['GET'])
def eco_scores():
    """Graphique des scores écologiques"""
    chart_data = visualizer.create_eco_scores_chart()
    return jsonify(chart_data)

@app.route('/api/visualizations/destination-analysis', methods=['GET'])
def destination_analysis():
    """Analyse visuelle des destinations"""
    chart_data = visualizer.create_destination_analysis_chart()
    return jsonify(chart_data)

@app.route('/api/visualizations/network-graph', methods=['GET'])
def network_graph():
    """Graphe de réseau de l'ontologie"""
    graph_data = visualizer.create_network_graph()
    return jsonify(graph_data)

@app.route('/api/visualizations/energy-consumption', methods=['GET'])
def energy_consumption():
    """Graphique de consommation énergétique"""
    chart_data = visualizer.create_energy_consumption_chart()
    return jsonify(chart_data)

# ==================== ADVANCED FEATURES ====================

@app.route('/api/advanced/filter', methods=['POST'])
def advanced_filter():
    """Filtrage avancé avec critères multiples"""
    filters = request.json
    
    # Construire une requête SPARQL dynamique basée sur les filtres
    conditions = []
    
    if 'max_energy' in filters:
        conditions.append(f"FILTER(?energie <= {filters['max_energy']})")
    
    if 'min_certification_level' in filters:
        conditions.append(f"FILTER(CONTAINS(LCASE(?niveau), LCASE('{filters['min_certification_level']}')))\n")
    
    if 'location' in filters:
        conditions.append(f"FILTER(CONTAINS(LCASE(?localisation), LCASE('{filters['location']}')))\n")

    # Nouveau: filtrage texte global (subject/property/value)
    if 'text' in filters and str(filters['text']).strip():
        text = str(filters['text']).replace("'", "\\'")
        conditions.append(
            """
            FILTER(
                CONTAINS(LCASE(STR(?entity)), LCASE('""" + text.lower() + """')) ||
                CONTAINS(LCASE(STR(?property)), LCASE('""" + text.lower() + """')) ||
                CONTAINS(LCASE(STR(?value)), LCASE('""" + text.lower() + """')) ||
                CONTAINS(LCASE(STR(?type)), LCASE('""" + text.lower() + """'))
            )
            """
        )
    
    # Nouveau: filtrage par type d'entité
    if 'entity_type' in filters and str(filters['entity_type']).strip():
        entity_type = str(filters['entity_type'])
        if entity_type == 'Destination':
            conditions.append("FILTER(?type = eco:Destination)")
        elif entity_type == 'Hébergement':
            conditions.append("FILTER(?type = eco:Hébergement)")
        elif entity_type == 'ActivitéTouristique':
            conditions.append("FILTER(?type = eco:ActivitéTouristique)")
        elif entity_type == 'Transport':
            conditions.append("FILTER(EXISTS { ?type rdfs:subClassOf* eco:Transport })")
        elif entity_type == 'CertificationÉcologique':
            conditions.append("FILTER(?type = eco:CertificationÉcologique)")
    
    filter_clause = "\n".join(conditions)
    
    # Requête: on se limite aux classes d'intérêt pour de meilleurs résultats
    query = f"""
    PREFIX eco: <http://example.org/ecotourisme#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    SELECT DISTINCT ?entity ?type ?localisation ?energie ?niveau
    WHERE {{
        ?entity rdf:type ?type .
        FILTER(
            ?type IN (eco:Destination, eco:Hébergement, eco:ActivitéTouristique, eco:CertificationÉcologique) ||
            EXISTS {{ ?type rdfs:subClassOf* eco:Transport }}
        )
        OPTIONAL {{ ?entity eco:aConsommationÉnergie ?energie }}
        OPTIONAL {{ ?entity eco:aLocalisation ?localisation }}
        OPTIONAL {{ ?entity eco:aCertification ?cert . ?cert eco:aNiveauCertification ?niveau }}
        {filter_clause}
    }}
    LIMIT 200
    """
    
    results = ontology.execute_sparql(query)
    return jsonify({
        'filters': filters,
        'results': results,
        'count': len(results)
    })

@app.route('/api/advanced/compare', methods=['POST'])
def compare_entities():
    """Compare plusieurs entités"""
    data = request.json
    entities = data.get('entities', [])
    
    if len(entities) < 2:
        return jsonify({'error': 'At least 2 entities required'}), 400
    
    comparisons = []
    for entity in entities:
        related = ontology.get_related_entities(entity)
        comparisons.append({
            'entity': entity,
            'properties': related
        })
    
    return jsonify({
        'comparisons': comparisons,
        'count': len(comparisons)
    })

@app.route('/api/advanced/eco-score/<entity_name>', methods=['GET'])
def calculate_eco_score(entity_name):
    """Calcule le score écologique d'une entité"""
    # Récupérer les informations de l'entité
    related = ontology.get_related_entities(entity_name)
    
    # Extraire les données pertinentes
    entity_data = {}
    for rel in related:
        if 'aConsommationÉnergie' in str(rel.get('relation', '')):
            entity_data['energie'] = rel.get('relatedEntity', 0)
        if 'aCertification' in str(rel.get('relation', '')):
            entity_data['certification'] = rel.get('relatedEntity', '')
    
    eco_score = recommender.calculate_eco_score(entity_data)
    
    return jsonify({
        'entity': entity_name,
        'eco_score': eco_score,
        'data': entity_data
    })

# ==================== ERROR HANDLERS ====================

# ==================== CHATBOT IA ====================

@app.route('/api/chatbot/message', methods=['POST'])
def chatbot_message():
    """Envoyer un message au chatbot"""
    data = request.json
    user_message = data.get('message', '')
    use_llm = bool(data.get('use_llm', False))
    
    if not user_message:
        return jsonify({'error': 'Message is required'}), 400
    
    try:
        # Validation des variables pour le mode LLM
        if use_llm:
            api_key_env = os.getenv('OPENAI_API_KEY')
            if not api_key_env:
                return jsonify({'error': 'OPENAI_API_KEY non défini. Ajoutez-le dans votre .env ou exportez-le dans le terminal.'}), 400
            # Remarque: avec les clés sk-proj- le Project ID est recommandé (OPENAI_PROJECT),
            # mais on ne bloque plus. Le SDK tentera l'appel en utilisant les variables disponibles.
        response = chatbot.process_message(user_message, use_llm=use_llm)
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/chatbot/history', methods=['GET'])
def chatbot_history():
    """Récupérer l'historique de conversation"""
    history = chatbot.get_conversation_history()
    return jsonify({
        'history': history,
        'count': len(history)
    })

@app.route('/api/chatbot/clear', methods=['POST'])
def chatbot_clear():
    """Effacer l'historique"""
    chatbot.clear_history()
    return jsonify({'success': True, 'message': 'History cleared'})

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

# ==================== MAIN ====================

if __name__ == '__main__':
    print("=" * 60)
    print("🌍 Eco Travel Semantic Application")
    print("=" * 60)
    print(f"✓ Ontology loaded: {len(ontology.graph)} triples")
    print(f"✓ Statistics: {ontology.get_statistics()}")
    print("=" * 60)
    print("🚀 Starting Flask server...")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5000)
