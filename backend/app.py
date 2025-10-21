"""
Application Flask principale - API REST pour l'écotourisme sémantique
"""
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import os
import sys
from dotenv import load_dotenv
from datetime import timedelta, datetime
from sqlalchemy import func

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ontology_manager import OntologyManager
from sparql_queries import SPARQLQueries
from recommendation_engine import RecommendationEngine
from visualization_engine import VisualizationEngine
from ai_chatbot import EcoTravelChatbot
from openai import OpenAI

# Import authentication modules
from models import db, bcrypt, User, UserActivity, Recommendation, DestinationView, SPARQLQuery
from auth import register_user, login_user, token_required, admin_required, get_current_user, log_activity
from admin_routes import admin_bp

app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)

# Initialize extensions
db.init_app(app)
bcrypt.init_app(app)
jwt = JWTManager(app)

# Register admin blueprint
app.register_blueprint(admin_bp)

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
    return app.send_static_file('index.html')

@app.route('/api/health', methods=['GET'])
def health_check():
    """Vérification de l'état de l'API"""
    stats = ontology.get_statistics()
    return jsonify({
        'status': 'healthy',
        'ontology_loaded': len(ontology.graph) > 0,
        'statistics': stats
    })

# ==================== AUTHENTICATION ROUTES ====================

@app.route('/api/auth/register', methods=['POST'])
def register():
    """Register a new user"""
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role', 'voyageur')
    
    if not all([username, email, password]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    return register_user(username, email, password, role)

@app.route('/api/auth/login', methods=['POST'])
def login():
    """Login user"""
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if not all([username, password]):
        return jsonify({'error': 'Missing username or password'}), 400
    
    return login_user(username, password)

@app.route('/api/auth/me', methods=['GET'])
@token_required
def get_current_user_info(current_user_id):
    """Get current user information"""
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({
        'success': True,
        'user': user.to_dict()
    })

@app.route('/api/auth/logout', methods=['POST'])
@token_required
def logout(current_user_id):
    """Logout user (client should delete token)"""
    log_activity(current_user_id, 'logout', {})
    return jsonify({
        'success': True,
        'message': 'Logged out successfully'
    })

# ==================== SPARQL QUERIES ====================

@app.route('/api/sparql/execute', methods=['POST'])
def execute_sparql():
    """Exécute une requête SPARQL personnalisée et track dans la base de données"""
    import time
    
    data = request.json
    query = data.get('query', '')
    
    if not query:
        return jsonify({'error': 'Query is required'}), 400
    
    # Déterminer l'utilisateur
    user_id = None
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith('Bearer '):
        try:
            from flask_jwt_extended import decode_token
            token = auth_header.split(' ')[1]
            decoded = decode_token(token)
            user_id = decoded.get('sub')
        except:
            pass
    
    # Déterminer le type de requête
    query_upper = query.strip().upper()
    if query_upper.startswith('SELECT'):
        query_type = 'SELECT'
    elif query_upper.startswith('INSERT'):
        query_type = 'INSERT'
    elif query_upper.startswith('DELETE'):
        query_type = 'DELETE'
    elif 'DELETE' in query_upper and 'INSERT' in query_upper:
        query_type = 'UPDATE'
    else:
        query_type = 'OTHER'
    
    start_time = time.time()
    success = True
    error_msg = None
    results = []
    
    try:
        results = ontology.execute_sparql(query)
        execution_time = time.time() - start_time
        
        # Enregistrer dans la base de données
        sparql_query = SPARQLQuery(
            user_id=user_id,
            query_text=query,
            query_type=query_type,
            results_count=len(results) if results else 0,
            success=True,
            execution_time=execution_time
        )
        db.session.add(sparql_query)
        
        # Logger l'activité si l'utilisateur est connecté
        if user_id:
            log_activity(user_id, 'sparql_query', {
                'query_type': query_type,
                'results_count': len(results) if results else 0
            })
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'results': results,
            'count': len(results) if results else 0,
            'query_executed': query,
            'triple_count': len(ontology.graph),
            'execution_time': round(execution_time, 3)
        })
        
    except Exception as e:
        success = False
        error_msg = str(e)
        execution_time = time.time() - start_time
        
        # Enregistrer l'échec
        try:
            sparql_query = SPARQLQuery(
                user_id=user_id,
                query_text=query,
                query_type=query_type,
                results_count=0,
                success=False,
                error_message=error_msg,
                execution_time=execution_time
            )
            db.session.add(sparql_query)
            db.session.commit()
        except:
            pass
        
        return jsonify({'error': error_msg, 'query_executed': query}), 500

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

@app.route('/api/sparql/count', methods=['GET'])
def get_sparql_count():
    """Récupère le nombre total de requêtes SPARQL exécutées"""
    try:
        # Compter toutes les requêtes
        total_queries = SPARQLQuery.query.count()
        
        # Récupérer la dernière requête
        last_query = SPARQLQuery.query.order_by(SPARQLQuery.created_at.desc()).first()
        
        # Statistiques par type
        select_count = SPARQLQuery.query.filter_by(query_type='SELECT').count()
        insert_count = SPARQLQuery.query.filter_by(query_type='INSERT').count()
        delete_count = SPARQLQuery.query.filter_by(query_type='DELETE').count()
        update_count = SPARQLQuery.query.filter_by(query_type='UPDATE').count()
        
        return jsonify({
            'success': True,
            'total_queries': total_queries,
            'last_query_time': last_query.created_at.isoformat() if last_query else None,
            'by_type': {
                'SELECT': select_count,
                'INSERT': insert_count,
                'DELETE': delete_count,
                'UPDATE': update_count
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'total_queries': 0
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

def generate_smart_recommendations(destination, preferences):
    """
    Génère des recommandations intelligentes pour n'importe quel pays
    Utilise une base de connaissances géographiques + génération dynamique
    """
    import random
    
    # Base de données de pays avec leurs caractéristiques et alias
    country_data = {
        'france': {
            'aliases': ['france', 'french', 'français'],
            'name': 'France',
            'cities': ['Paris', 'Lyon', 'Marseille', 'Bordeaux', 'Nice', 'Toulouse'],
            'eco_features': ['Vignobles bio', 'Parcs nationaux', 'Architecture durable', 'Jardins urbains'],
            'transports': ['TGV', 'Métro', 'Vélib', 'Covoiturage BlaBlaCar'],
            'activities': ['Visite musées à vélo', 'Randonnée dans les Alpes', 'Dégustation vins bio', 'Marchés locaux']
        },
        'pays-bas': {
            'aliases': ['pays-bas', 'netherlands', 'holland', 'dutch', 'hollande', 'néerlandais'],
            'name': 'Pays-Bas',
            'cities': ['Amsterdam', 'Rotterdam', 'La Haye', 'Utrecht', 'Eindhoven'],
            'eco_features': ['Pistes cyclables', 'Moulins à vent', 'Canaux écologiques', 'Jardins de tulipes'],
            'transports': ['Vélo', 'Train NS', 'Tram électrique', 'Bateau électrique'],
            'activities': ['Vélo dans les polders', 'Visite moulins', 'Croisière canaux', 'Marchés de fleurs']
        },
        'japon': {
            'aliases': ['japon', 'japan', 'japanese', 'japonais'],
            'name': 'Japon',
            'cities': ['Tokyo', 'Kyoto', 'Osaka', 'Nara', 'Hiroshima'],
            'eco_features': ['Temples zen', 'Jardins japonais', 'Forêts de bambou', 'Onsens naturels'],
            'transports': ['Shinkansen', 'Métro', 'Vélo', 'Train local'],
            'activities': ['Cérémonie du thé', 'Randonnée Mont Fuji', 'Visite temples', 'Jardins zen']
        },
        'bresil': {
            'aliases': ['brésil', 'bresil', 'brazil', 'brazilian'],
            'name': 'Brésil',
            'cities': ['Rio de Janeiro', 'São Paulo', 'Salvador', 'Brasilia', 'Florianopolis'],
            'eco_features': ['Forêt amazonienne', 'Plages préservées', 'Biodiversité unique', 'Réserves naturelles'],
            'transports': ['Métro', 'Bus électrique', 'Vélo', 'Bateau écologique'],
            'activities': ['Randonnée en forêt', 'Snorkeling', 'Observation faune', 'Eco-tourisme']
        },
        'canada': {
            'aliases': ['canada', 'canadian', 'canadien'],
            'name': 'Canada',
            'cities': ['Vancouver', 'Toronto', 'Montréal', 'Québec', 'Calgary'],
            'eco_features': ['Parcs nationaux', 'Lacs glaciaires', 'Forêts boréales', 'Montagnes Rocheuses'],
            'transports': ['Train VIA', 'Métro', 'Vélo', 'Covoiturage'],
            'activities': ['Randonnée montagnes', 'Kayak', 'Observation ours', 'Ski écologique']
        },
        'espagne': {
            'aliases': ['espagne', 'spain', 'spanish', 'español'],
            'name': 'Espagne',
            'cities': ['Barcelona', 'Madrid', 'Seville', 'Valencia', 'Bilbao'],
            'eco_features': ['Architecture Gaudí', 'Plages méditerranée', 'Parcs urbains', 'Vignobles'],
            'transports': ['AVE', 'Métro', 'Bicing', 'Tram'],
            'activities': ['Visite Sagrada Familia', 'Tapas bio', 'Randonnée côtière', 'Flamenco']
        },
        'italie': {
            'aliases': ['italie', 'italy', 'italian', 'italien'],
            'name': 'Italie',
            'cities': ['Rome', 'Florence', 'Venise', 'Milan', 'Naples'],
            'eco_features': ['Patrimoine UNESCO', 'Vignobles toscans', 'Côte Amalfitaine', 'Parcs naturels'],
            'transports': ['Train Trenitalia', 'Métro', 'Vélo', 'Vaporetto'],
            'activities': ['Visite sites historiques', 'Dégustation huile olive', 'Randonnée Cinque Terre', 'Marchés locaux']
        },
        'allemagne': {
            'aliases': ['allemagne', 'germany', 'german', 'deutsch'],
            'name': 'Allemagne',
            'cities': ['Berlin', 'Munich', 'Hambourg', 'Cologne', 'Frankfurt'],
            'eco_features': ['Forêt Noire', 'Énergies renouvelables', 'Villes vertes', 'Châteaux écologiques'],
            'transports': ['ICE', 'U-Bahn', 'Vélo', 'Tram'],
            'activities': ['Visite châteaux', 'Fêtes de la bière bio', 'Randonnée Forêt Noire', 'Marchés de Noël']
        },
        'royaume-uni': {
            'aliases': ['royaume-uni', 'uk', 'united kingdom', 'england', 'angleterre', 'britain'],
            'name': 'Royaume-Uni',
            'cities': ['Londres', 'Édimbourg', 'Manchester', 'Liverpool', 'Oxford'],
            'eco_features': ['Parcs royaux', 'Campagne anglaise', 'Highlands écossaises', 'Côtes préservées'],
            'transports': ['Train', 'Underground', 'Bus hybride', 'Vélo'],
            'activities': ['Visite musées', 'Randonnée Highlands', 'Pubs traditionnels', 'Châteaux historiques']
        }
    }
    
    # Normaliser le nom du pays
    dest_lower = destination.lower().strip()
    
    # Détection intelligente du pays avec aliases
    country_key = None
    country_name = destination
    
    for key, data in country_data.items():
        for alias in data['aliases']:
            if alias in dest_lower or dest_lower in alias:
                country_key = key
                country_name = data['name']
                break
        if country_key:
            break
    
    # Si pays non trouvé, générer dynamiquement
    if not country_key:
        # Générer des recommandations génériques intelligentes
        cities = [f"{destination} Centre", f"{destination} Sud", f"{destination} Nord"]
        eco_features = ['Biodiversité locale', 'Espaces verts', 'Patrimoine naturel', 'Culture durable']
        transports = ['Transport local', 'Vélo', 'Transports publics', 'Covoiturage']
        activities = [f'Découverte de {destination}', 'Randonnée locale', 'Marchés traditionnels', 'Visites culturelles']
    else:
        data = country_data[country_key]
        cities = data['cities']
        eco_features = data['eco_features']
        transports = data['transports']
        activities = data['activities']
    
    # Générer les recommandations
    recommendations = {
        'destinations': [],
        'accommodations': [],
        'activities': [],
        'transport': []
    }
    
    # Destinations (3)
    for i, city in enumerate(random.sample(cities, min(3, len(cities)))):
        recommendations['destinations'].append({
            'destination': city,
            'localisation': country_name,
            'biodiversite': random.choice(eco_features),
            'final_score': random.randint(75, 95)
        })
    
    # Hébergements (3)
    hotel_types = ['Eco Hotel', 'Green Lodge', 'Bio Hostel', 'Sustainable Inn', 'Nature Resort']
    cert_levels = ['Gold', 'Silver', 'Platinum']
    for i in range(3):
        city = random.choice(cities[:3])
        recommendations['accommodations'].append({
            'hebergement': f"{random.choice(hotel_types)} {city}",
            'energie': str(random.randint(50, 120)),
            'niveau': random.choice(cert_levels),
            'final_score': random.randint(80, 98)
        })
    
    # Activités (3)
    impacts = ['Très faible impact', 'Faible impact', 'Impact minimal']
    for i, activity in enumerate(random.sample(activities, min(3, len(activities)))):
        recommendations['activities'].append({
            'activite': activity,
            'impact': random.choice(impacts),
            'final_score': random.randint(85, 98)
        })
    
    # Transports (3)
    for i, transport in enumerate(random.sample(transports, min(3, len(transports)))):
        co2_values = {'vélo': 0, 'train': random.randint(10, 25), 'métro': random.randint(5, 15), 
                     'bus': random.randint(20, 40), 'covoiturage': random.randint(15, 30)}
        
        # Déterminer CO2
        co2 = 20  # Défaut
        for key in co2_values:
            if key in transport.lower():
                co2 = co2_values[key]
                break
        
        descriptions = [
            'Transport écologique et durable',
            'Zéro émission, 100% vert',
            'Solution de mobilité douce',
            'Transport public électrique',
            'Partage de trajet éco-responsable'
        ]
        
        if co2 == 0:
            desc = 'Zéro émission, transport 100% écologique'
        elif co2 < 15:
            desc = 'Très faible émission, excellent choix écologique'
        else:
            desc = random.choice(descriptions)
        
        recommendations['transport'].append({
            'transport': f"{transport} vers {country_name}",
            'co2': str(co2),
            'description': desc,
            'final_score': random.randint(85, 99)
        })
    
    return recommendations

def generate_ai_recommendations(preferences):
    """
    Wrapper pour générer des recommandations
    Essaie OpenAI d'abord, sinon utilise le générateur smart
    """
    import openai
    
    api_key = os.getenv('OPENAI_API_KEY')
    
    # Si OpenAI disponible, l'utiliser
    if api_key:
        try:
            openai.api_key = api_key
            
            prompt = f"""Tu es un expert en voyage écologique. Génère des recommandations détaillées pour :

Destination: {preferences['destination']}
Budget: {preferences['budget']}€
Type de voyage: {preferences['type_voyage']}
Durée: {preferences['duree']}
Priorité écologique: {preferences['priorite_eco']}/10

Réponds UNIQUEMENT avec un JSON valide."""

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Tu es un expert en tourisme écologique."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1500
            )
            
            content = response.choices[0].message.content.strip()
            if '```json' in content:
                content = content.split('```json')[1].split('```')[0].strip()
            elif '```' in content:
                content = content.split('```')[1].split('```')[0].strip()
            
            recommendations = json.loads(content)
            return recommendations
        except Exception as e:
            print(f"Erreur OpenAI: {e}, utilisation du générateur smart")
    
    # Sinon, utiliser le générateur smart
    return generate_smart_recommendations(preferences['destination'], preferences)

@app.route('/api/recommendations-advanced', methods=['POST'])
def recommendations_advanced():
    """
    Génère des recommandations avancées avec tracking utilisateur
    Utilise l'IA si la destination n'est pas dans l'ontologie
    Accessible avec ou sans authentification
    """
    from flask import request
    from datetime import datetime
    import json
    
    try:
        data = request.json
        
        # Extraire les préférences
        preferences = {
            'destination': data.get('destination', ''),
            'budget': float(data.get('budget', 1000)),
            'type_voyage': data.get('type_voyage', 'Aventure'),
            'duree': data.get('duree', 'Weekend'),
            'priorite_eco': int(data.get('priorite_ecologique', 5))
        }
        
        # Déterminer l'utilisateur (connecté ou anonyme)
        user_id = None
        username = 'Anonymous'
        
        # Vérifier si l'utilisateur est connecté
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            try:
                from flask_jwt_extended import decode_token
                token = auth_header.split(' ')[1]
                decoded = decode_token(token)
                user_id = decoded.get('sub')
                
                user = User.query.get(user_id)
                if user:
                    username = user.username
            except:
                pass  # Utilisateur anonyme si le token est invalide
        
        # TOUJOURS utiliser l'IA Smart pour générer des recommandations intelligentes
        # Cela garantit des recommandations pour n'importe quel pays du monde
        
        ai_recommendations = generate_ai_recommendations(preferences)
        if ai_recommendations:
            recommendations = ai_recommendations
            # Calculer un score écologique basé sur la priorité
            eco_score = min(100, 50 + (preferences['priorite_eco'] * 5))
        else:
            # Fallback très rare (si erreur dans le générateur)
            recommendations = {
                'destinations': [],
                'accommodations': [],
                'activities': [],
                'transport': []
            }
            eco_score = 50
        
        # Enregistrer dans la base de données
        recommendation = Recommendation(
            user_id=user_id,
            recommendation_type='advanced',
            recommendation_data=json.dumps({
                'preferences': preferences,
                'destinations': recommendations.get('destinations', []),
                'accommodations': recommendations.get('accommodations', []),
                'activities': recommendations.get('activities', []),
                'transport': recommendations.get('transport', [])
            }),
            eco_score=eco_score,
            created_at=datetime.utcnow()
        )
        db.session.add(recommendation)
        
        # Logger l'activité si l'utilisateur est connecté
        if user_id:
            log_activity(user_id, 'recommendation_advanced', {
                'destination': preferences['destination'],
                'budget': preferences['budget'],
                'eco_score': eco_score
            })
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'recommendations': recommendations,
            'eco_score': eco_score,
            'user': username,
            'timestamp': datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/recommendations-advanced/history', methods=['GET'])
def recommendations_advanced_history():
    """
    Récupère l'historique des recommandations
    Si l'utilisateur est connecté, retourne son historique
    Sinon, retourne les dernières recommandations publiques
    """
    try:
        user_id = None
        
        # Vérifier si l'utilisateur est connecté
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            try:
                from flask_jwt_extended import decode_token
                token = auth_header.split(' ')[1]
                decoded = decode_token(token)
                user_id = decoded.get('sub')
            except:
                pass
        
        # Récupérer l'historique
        if user_id:
            # Historique de l'utilisateur connecté
            recommendations = Recommendation.query.filter_by(
                user_id=user_id,
                recommendation_type='advanced'
            ).order_by(Recommendation.created_at.desc()).limit(10).all()
        else:
            # Dernières recommandations publiques
            recommendations = Recommendation.query.filter_by(
                recommendation_type='advanced'
            ).order_by(Recommendation.created_at.desc()).limit(5).all()
        
        return jsonify({
            'success': True,
            'history': [rec.to_dict() for rec in recommendations]
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

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

# ==================== DASHBOARD STATISTICS ====================

@app.route('/api/dashboard/statistics', methods=['GET'])
def get_dashboard_statistics():
    """Récupère les statistiques détaillées de l'ontologie et système en temps réel"""
    try:
        # Statistiques des classes principales (ontologie)
        class_queries = {
            'Destinations': {
                'count': "SELECT (COUNT(?s) AS ?count) WHERE { ?s rdf:type eco:Destination }",
                'details': "SELECT ?destination ?localisation WHERE { ?destination rdf:type eco:Destination . OPTIONAL { ?destination eco:aLocalisation ?localisation } }"
            },
            'Hébergements': {
                'count': "SELECT (COUNT(?s) AS ?count) WHERE { ?s rdf:type eco:Hébergement }",
                'details': "SELECT ?hebergement ?energie WHERE { ?hebergement rdf:type eco:Hébergement . OPTIONAL { ?hebergement eco:aConsommationÉnergie ?energie } }"
            },
            'Activités': {
                'count': "SELECT (COUNT(?s) AS ?count) WHERE { ?s rdf:type eco:ActivitéTouristique }",
                'details': "SELECT ?activite ?impact WHERE { ?activite rdf:type eco:ActivitéTouristique . OPTIONAL { ?activite eco:aImpactEnvironnemental ?impact } }"
            },
            'Transports': {
                'count': "SELECT (COUNT(?s) AS ?count) WHERE { ?s rdf:type ?type . ?type rdfs:subClassOf* eco:Transport . FILTER(?type != eco:Transport) }",
                'details': "SELECT ?transport ?type ?co2 WHERE { ?transport rdf:type ?type . ?type rdfs:subClassOf* eco:Transport . OPTIONAL { ?transport eco:aEmpreinte ?empreinte . ?empreinte eco:aCO2 ?co2 } }"
            },
            'Certifications': {
                'count': "SELECT (COUNT(?s) AS ?count) WHERE { ?s rdf:type eco:CertificationÉcologique }",
                'details': "SELECT ?certification ?niveau WHERE { ?certification rdf:type eco:CertificationÉcologique . OPTIONAL { ?certification eco:aNiveauCertification ?niveau } }"
            }
        }

        statistics = {}
        total_entities = 0

        for class_name, queries in class_queries.items():
            # Compter les instances
            count_result = ontology.execute_sparql(queries['count'])
            count = int(count_result[0]['count']) if count_result else 0
            statistics[class_name] = {'count': count, 'details': []}
            total_entities += count

            # Récupérer les détails (max 5 exemples)
            if count > 0:
                details_result = ontology.execute_sparql(queries['details'])
                statistics[class_name]['details'] = details_result[:5]

        # Statistiques globales
        total_triples = len(ontology.graph)

        # Statistiques énergétiques (pour le score écologique)
        energy_query = """
        PREFIX eco: <http://example.org/ecotourisme#>
        SELECT (AVG(?energie) AS ?energieMoyenne) (MIN(?energie) AS ?energieMin) (MAX(?energie) AS ?energieMax)
        WHERE {
            ?hebergement rdf:type eco:Hébergement .
            ?hebergement eco:aConsommationÉnergie ?energie .
        }
        """
        energy_stats = ontology.execute_sparql(energy_query)
        energy_avg = float(energy_stats[0]['energieMoyenne']) if energy_stats and energy_stats[0].get('energieMoyenne') else 0

        # Calculer le score écologique basé sur l'énergie moyenne
        eco_score = max(0, 100 - (energy_avg / 2)) if energy_avg > 0 else 85

        # Empreinte carbone moyenne (basée sur les transports)
        carbon_query = """
        PREFIX eco: <http://example.org/ecotourisme#>
        SELECT (AVG(?co2) AS ?co2Moyen)
        WHERE {
            ?transport rdf:type ?type .
            ?type rdfs:subClassOf* eco:Transport .
            ?transport eco:aEmpreinte ?empreinte .
            ?empreinte eco:aCO2 ?co2 .
        }
        """
        carbon_stats = ontology.execute_sparql(carbon_query)
        carbon_avg = float(carbon_stats[0]['co2Moyen']) if carbon_stats and carbon_stats[0].get('co2Moyen') else 45
        
        # Statistiques système (utilisateurs, requêtes, recommandations)
        from datetime import datetime, timedelta
        total_users = User.query.count()
        total_sparql = UserActivity.query.filter_by(activity_type='sparql_query').count()
        total_recommendations = Recommendation.query.count()
        
        # Calcul du score moyen des recommandations
        avg_recommendation_score = db.session.query(func.avg(Recommendation.eco_score))\
            .filter(Recommendation.eco_score.isnot(None)).scalar() or 0
        
        # Nouveaux utilisateurs ce mois
        first_day_of_month = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        new_users_this_month = User.query.filter(User.created_at >= first_day_of_month).count()

        return jsonify({
            'timestamp': datetime.utcnow().isoformat(),
            'total_entities': total_entities,
            'total_triples': total_triples,
            'eco_score': round(eco_score, 2),
            'carbon_footprint': round(carbon_avg, 2),
            'class_statistics': statistics,
            'last_updated': datetime.utcnow().isoformat(),
            # Statistiques système
            'system_stats': {
                'total_users': total_users,
                'new_users_this_month': new_users_this_month,
                'total_sparql_queries': total_sparql,
                'total_recommendations': total_recommendations,
                'avg_recommendation_score': round(float(avg_recommendation_score), 2)
            }
        })

    except Exception as e:
        return jsonify({
            'error': str(e),
            'total_entities': 0,
            'total_triples': 0,
            'eco_score': 0,
            'carbon_footprint': 0,
            'class_statistics': {},
            'system_stats': {
                'total_users': 0,
                'new_users_this_month': 0,
                'total_sparql_queries': 0,
                'total_recommendations': 0,
                'avg_recommendation_score': 0
            }
        }), 500

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

# ==================== MAIN ====================

def init_database():
    """Initialize database and create default admin user"""
    with app.app_context():
        db.create_all()
        
        # Create default admin user if not exists
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@ecotravel.com',
                role='admin'
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("✓ Default admin user created (username: admin, password: admin123)")
        
        print(f"✓ Database initialized ({User.query.count()} users)")

# ==================== SEARCH ENDPOINT ====================

@app.route('/api/search', methods=['POST'])
def search_entities():
    """Recherche avancée dans l'ontologie"""
    try:
        data = request.json or {}
        text_query = data.get('text', '').lower()
        energy_max = data.get('energy')
        location_filter = data.get('location', '').lower()
        entity_type = data.get('type', '')
        
        results = []
        
        # Recherche selon le type
        if entity_type in ['', 'destination']:
            destinations = ontology.get_all_destinations()
            for dest in destinations:
                match = True
                if text_query and text_query not in str(dest).lower():
                    match = False
                if location_filter and location_filter not in str(dest.get('localisation', '')).lower():
                    match = False
                if match:
                    results.append({
                        'type': 'destination',
                        'name': dest.get('destination', dest),
                        'localisation': dest.get('localisation', ''),
                        'score': dest.get('final_score', 0)
                    })
        
        if entity_type in ['', 'accommodation']:
            accommodations = ontology.get_all_accommodations()
            for acc in accommodations:
                match = True
                if text_query and text_query not in str(acc).lower():
                    match = False
                if energy_max and float(acc.get('energie', 999)) > float(energy_max):
                    match = False
                if match:
                    results.append({
                        'type': 'accommodation',
                        'name': acc.get('hebergement', acc),
                        'energie': acc.get('energie', ''),
                        'niveau': acc.get('niveau', '')
                    })
        
        return jsonify({
            'success': True,
            'results': results,
            'count': len(results)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ==================== CHATBOT ENDPOINT ====================

@app.route('/api/chatbot/chat', methods=['POST'])
def chat_with_bot():
    """Chat avec l'assistant IA"""
    try:
        data = request.json or {}
        message = data.get('message', '')
        use_llm = data.get('use_llm', False)
        
        if not message:
            return jsonify({
                'success': False,
                'error': 'Message requis'
            }), 400
        
        # Utiliser le chatbot existant
        response = chatbot.process_message(message, use_llm=use_llm)
        
        return jsonify({
            'success': True,
            'response': response.get('response', ''),
            'suggestions': response.get('suggestions', []),
            'data': response.get('data', [])
        })
    except Exception as e:
        # Réponse fallback si erreur
        return jsonify({
            'success': True,
            'response': f"Je suis désolé, je rencontre une difficulté technique. Voici quelques suggestions : Quelles sont les meilleures destinations écologiques ? Quels hébergements certifiés à Tunis ?",
            'suggestions': [
                "Quelles sont les meilleures destinations écologiques?",
                "Quels hébergements certifiés à Tunis?",
                "Comparer train et avion en CO2",
                "Activités à faible impact à Djerba"
            ],
            'data': []
        })

if __name__ == '__main__':
    print("=" * 60)
    print("🌍 Eco Travel Semantic Application")
    print("=" * 60)
    
    # Initialize database
    init_database()
    
    print(f"✓ Ontology loaded: {len(ontology.graph)} triples")
    print(f"✓ Statistics: {ontology.get_statistics()}")
    print("=" * 60)
    print("🚀 Starting Flask server...")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5000)
