"""
Chatbot IA pour EcoTravel - Utilise l'ontologie pour répondre aux questions
"""
import re
from ontology_manager import OntologyManager
import os
try:
    from llm_bridge import LLMAssistant
except Exception:
    LLMAssistant = None

class EcoTravelChatbot:
    """Chatbot intelligent basé sur l'ontologie"""
    
    def __init__(self, ontology_manager, api_key: str = None, model_name: str = None):
        # api_key et model_name sont acceptés pour compatibilité; la lecture se fait via variables d'environnement
        self.ontology = ontology_manager
        self.conversation_history = []
        self._api_key = api_key
        self._model_name = model_name
        
    def process_message(self, user_message, use_llm: bool = False):
        """Traite un message utilisateur et génère une réponse"""
        user_message_lower = user_message.lower()
        
        # Ajouter à l'historique
        self.conversation_history.append({
            'role': 'user',
            'message': user_message
        })
        
        # Détection d'intention
        # Si LLM demandé et disponible, créer un contexte et déléguer au modèle
        if use_llm and LLMAssistant and os.getenv('OPENAI_API_KEY'):
            response = self._generate_llm_response(user_message)
        else:
            response = self._generate_response(user_message_lower)
        
        # Ajouter la réponse à l'historique
        self.conversation_history.append({
            'role': 'assistant',
            'message': response
        })
        
        return {
            'response': response,
            'suggestions': self._get_suggestions(user_message_lower),
            'data': self._get_relevant_data(user_message_lower)
        }

    def _generate_llm_response(self, message: str) -> str:
        """Construit un contexte depuis l'ontologie et demande une réponse au LLM"""
        # 1) Récupérer des données pertinentes (RAG simple)
        related_snippets = []
        # Destinations / hébergements / transports / activités
        for block in [
            self._get_destinations(),
            self._get_eco_accommodations(),
            self._get_transports(),
            self._get_activities(),
        ]:
            for r in block[:5]:
                parts = []
                if 'destination' in r: parts.append(f"dest={r.get('destination')}")
                if 'localisation' in r: parts.append(f"loc={r.get('localisation')}")
                if 'biodiversite' in r: parts.append(f"biodiv={r.get('biodiversite')}")
                if 'hebergement' in r: parts.append(f"heb={r.get('hebergement')}")
                if 'energie' in r: parts.append(f"energie={r.get('energie')}")
                if 'niveau' in r: parts.append(f"cert={r.get('niveau')}")
                if 'typeTransport' in r: parts.append(f"transport={r.get('typeTransport')}")
                if 'co2' in r: parts.append(f"co2={r.get('co2')}")
                if 'activite' in r: parts.append(f"act={r.get('activite')}")
                if 'impact' in r: parts.append(f"impact={r.get('impact')}")
                if parts:
                    related_snippets.append(" | ".join(parts))
        context_text = "\n".join(related_snippets[:20])

        prompt = f"""
        Tu es un assistant de voyage écologique. Réponds précisément et concrètement en français.
        Utilise le contexte RDF/OWL suivant si pertinent et cite les éléments clés (destination, certifs, énergie, CO2):
        CONTEXTE:\n{context_text}
        QUESTION UTILISATEUR: {message}
        INSTRUCTIONS:
        - Donne des recommandations concrètes (destinations, hébergements certifiés, transports bas-carbone, activités à faible impact).
        - Justifie brièvement avec les données (ex: énergie, niveau de certification, CO2).
        - Termine par 1 à 3 conseils d'éco-conduite.
        """

        llm = LLMAssistant()
        return llm.complete(prompt)
    
    def _generate_response(self, message):
        """Génère une réponse basée sur le message"""
        
        # Salutations
        if any(word in message for word in ['bonjour', 'salut', 'hello', 'hi']):
            return "🌍 Bonjour! Je suis votre assistant de voyage écologique. Comment puis-je vous aider à planifier un voyage durable?"
        
        # Questions sur destinations
        if any(word in message for word in ['destination', 'où', 'voyage', 'aller']):
            destinations = self._get_destinations()
            if destinations:
                dest_list = ', '.join([d['destination'] for d in destinations[:3]])
                return f"✈️ Je vous recommande ces destinations écologiques: {dest_list}. Voulez-vous plus de détails sur l'une d'elles?"
            return "Je peux vous aider à trouver des destinations écologiques. Quelles sont vos préférences?"
        
        # Questions sur hébergements
        if any(word in message for word in ['hôtel', 'hébergement', 'dormir', 'loger']):
            accommodations = self._get_eco_accommodations()
            if accommodations:
                acc_list = ', '.join([a['hebergement'] for a in accommodations[:3]])
                return f"🏨 Voici des hébergements écologiques: {acc_list}. Tous ont une faible consommation énergétique!"
            return "Je peux vous trouver des hébergements certifiés écologiques. Quelle est votre destination?"
        
        # Questions sur transport
        if any(word in message for word in ['transport', 'train', 'avion', 'voiture', 'comment']):
            return "🚆 Pour un voyage écologique, je recommande: 1) Train (45 kg CO2), 2) Bus électrique (25 kg CO2), 3) Covoiturage (35 kg CO2). L'avion émet 250 kg CO2!"
        
        # Questions sur activités
        if any(word in message for word in ['activité', 'faire', 'visiter', 'voir']):
            activities = self._get_activities()
            if activities:
                act_list = ', '.join([a['activite'] for a in activities[:3]])
                return f"🎯 Activités à faible impact: {act_list}. Toutes respectent l'environnement local!"
            return "Je peux vous suggérer des activités écologiques. Dans quelle région voyagez-vous?"
        
        # Questions sur empreinte carbone
        if any(word in message for word in ['carbone', 'co2', 'émission', 'pollution']):
            return "🌱 L'empreinte carbone varie selon le transport: Vélo (0 kg), Train (45 kg), Bus (25 kg), Avion (250 kg). Choisissez le train pour réduire de 70%!"
        
        # Questions sur budget
        if any(word in message for word in ['prix', 'coût', 'budget', 'cher']):
            return "💰 Les voyages écologiques peuvent être économiques! Les hébergements certifiés ont des prix variés. Quel est votre budget approximatif?"
        
        # Questions sur certifications
        if any(word in message for word in ['certification', 'label', 'écologique', 'vert']):
            return "🏆 Nous utilisons 3 niveaux de certification: Gold (100% renouvelable), Silver (gestion eau), Bronze (recyclage). Tous garantissent un impact réduit!"
        
        # Aide générale
        if any(word in message for word in ['aide', 'help', 'comment', 'quoi']):
            return "💡 Je peux vous aider avec: destinations écologiques, hébergements certifiés, activités durables, calcul d'empreinte carbone, et conseils de voyage responsable. Que souhaitez-vous savoir?"
        
        # Recommandations personnalisées
        if any(word in message for word in ['recommand', 'conseil', 'suggér']):
            return "⭐ Pour des recommandations personnalisées, dites-moi: votre budget, vos préférences (nature/culture), et votre profil écologique. Je créerai un plan sur mesure!"
        
        # Réponse par défaut avec recherche dans l'ontologie
        search_results = self.ontology.search_by_text(message)
        if search_results:
            return f"🔍 J'ai trouvé {len(search_results)} résultats dans notre base de données. Voulez-vous que je vous donne plus de détails?"
        
        return "🤔 Je n'ai pas bien compris. Pouvez-vous reformuler? Je peux vous aider avec: destinations, hébergements, transports, activités, ou empreinte carbone."
    
    def _get_suggestions(self, message):
        """Génère des suggestions de questions"""
        suggestions = [
            "Quelles sont les meilleures destinations écologiques?",
            "Comment réduire mon empreinte carbone en voyage?",
            "Quels hébergements sont certifiés écologiques?",
            "Quelles activités respectent l'environnement?"
        ]
        
        # Suggestions contextuelles
        if 'destination' in message:
            suggestions = [
                "Parle-moi de la Tunisie",
                "Quels sont les hébergements à Marrakech?",
                "Quelle est la biodiversité au Sahara?",
                "Comment aller à Djerba en train?"
            ]
        elif 'transport' in message:
            suggestions = [
                "Compare train vs avion",
                "Quel transport émet le moins de CO2?",
                "Le covoiturage est-il écologique?",
                "Comment compenser mes émissions?"
            ]
        
        return suggestions
    
    def _get_relevant_data(self, message):
        """Récupère des données pertinentes de l'ontologie"""
        data = {}
        
        if 'destination' in message:
            data['destinations'] = self._get_destinations()
        
        if 'hébergement' in message or 'hôtel' in message:
            data['accommodations'] = self._get_eco_accommodations()
        
        if 'transport' in message:
            data['transports'] = self._get_transports()
        
        if 'activité' in message:
            data['activities'] = self._get_activities()
        
        return data
    
    def _get_destinations(self):
        """Récupère les destinations de l'ontologie"""
        query = """
        PREFIX eco: <http://example.org/ecotourisme#>
        SELECT ?destination ?localisation ?biodiversite
        WHERE {
            ?destination rdf:type eco:Destination .
            OPTIONAL { ?destination eco:aLocalisation ?localisation }
            OPTIONAL { ?destination eco:aBiodiversité ?biodiversite }
        }
        LIMIT 10
        """
        return self.ontology.execute_sparql(query)
    
    def _get_eco_accommodations(self):
        """Récupère les hébergements écologiques"""
        query = """
        PREFIX eco: <http://example.org/ecotourisme#>
        SELECT ?hebergement ?energie ?certification
        WHERE {
            ?hebergement rdf:type eco:Hébergement .
            OPTIONAL { ?hebergement eco:aConsommationÉnergie ?energie }
            OPTIONAL { ?hebergement eco:aCertification ?certification }
            FILTER(?energie < 150)
        }
        ORDER BY ?energie
        LIMIT 10
        """
        return self.ontology.execute_sparql(query)
    
    def _get_transports(self):
        """Récupère les transports et leurs émissions"""
        query = """
        PREFIX eco: <http://example.org/ecotourisme#>
        SELECT ?transport ?typeTransport ?co2
        WHERE {
            ?transport rdf:type ?typeTransport .
            ?typeTransport rdfs:subClassOf* eco:Transport .
            OPTIONAL {
                ?transport eco:aEmpreinte ?empreinte .
                ?empreinte eco:aCO2 ?co2
            }
            FILTER(?typeTransport != eco:Transport)
        }
        ORDER BY ?co2
        """
        return self.ontology.execute_sparql(query)
    
    def _get_activities(self):
        """Récupère les activités à faible impact"""
        query = """
        PREFIX eco: <http://example.org/ecotourisme#>
        SELECT ?activite ?impact ?authenticite
        WHERE {
            ?activite rdf:type eco:ActivitéTouristique .
            OPTIONAL { ?activite eco:aImpactEnvironnemental ?impact }
            OPTIONAL { ?activite eco:aAuthenticitéLocale ?authenticite }
            FILTER(CONTAINS(LCASE(?impact), "faible"))
        }
        LIMIT 10
        """
        return self.ontology.execute_sparql(query)
    
    def get_conversation_history(self):
        """Retourne l'historique de conversation"""
        return self.conversation_history
    
    def clear_history(self):
        """Efface l'historique"""
        self.conversation_history = []