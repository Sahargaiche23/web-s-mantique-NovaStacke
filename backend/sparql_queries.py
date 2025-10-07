"""
Module contenant 11+ requêtes SPARQL complexes et avancées
pour interroger l'ontologie écotourisme
"""

class SPARQLQueries:
    """Collection de requêtes SPARQL avancées"""
    
    PREFIX = """
    PREFIX eco: <http://example.org/ecotourisme#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    """
    
    # Requête 1: Hébergements écologiques avec faible empreinte carbone
    QUERY_1_ECO_ACCOMMODATIONS = PREFIX + """
    SELECT ?hebergement ?energie ?certification ?niveau
    WHERE {
        ?hebergement rdf:type eco:Hébergement .
        ?hebergement eco:aConsommationÉnergie ?energie .
        ?hebergement eco:aCertification ?certification .
        ?certification eco:aNiveauCertification ?niveau .
        FILTER(?energie < 150)
    }
    ORDER BY ?energie
    """
    
    # Requête 2: Destinations avec biodiversité riche et activités locales
    QUERY_2_BIODIVERSITY_DESTINATIONS = PREFIX + """
    SELECT ?destination ?localisation ?biodiversite (COUNT(?activite) AS ?nbActivites)
    WHERE {
        ?destination rdf:type eco:Destination .
        ?destination eco:aLocalisation ?localisation .
        ?destination eco:aBiodiversité ?biodiversite .
        OPTIONAL {
            ?destination eco:propose ?hebergement .
            ?activite eco:implique ?communaute .
        }
    }
    GROUP BY ?destination ?localisation ?biodiversite
    HAVING (COUNT(?activite) > 0)
    """
    
    # Requête 3: Comparaison empreintes carbone des transports
    QUERY_3_TRANSPORT_COMPARISON = PREFIX + """
    SELECT ?transport ?typeTransport ?co2 ?reduction
    WHERE {
        ?transport rdf:type ?typeTransport .
        ?typeTransport rdfs:subClassOf* eco:Transport .
        ?transport eco:aEmpreinte ?empreinte .
        ?empreinte eco:aCO2 ?co2 .
        OPTIONAL { ?empreinte eco:aRéductionPossible ?reduction }
        FILTER(?typeTransport != eco:Transport)
    }
    ORDER BY ?co2
    """
    
    # Requête 4: Voyageurs éco-responsables et leurs préférences
    QUERY_4_ECO_TRAVELERS = PREFIX + """
    SELECT ?voyageur ?budget ?profil ?preference ?destination
    WHERE {
        ?voyageur rdf:type eco:Voyageur .
        ?voyageur eco:aBudget ?budget .
        ?voyageur eco:aProfilÉcologique ?profil .
        ?voyageur eco:aPréférence ?preference .
        ?voyageur eco:choisit ?destination .
        FILTER(CONTAINS(LCASE(?profil), "éco"))
    }
    ORDER BY DESC(?budget)
    """
    
    # Requête 5: Activités touristiques à faible impact environnemental
    QUERY_5_LOW_IMPACT_ACTIVITIES = PREFIX + """
    SELECT ?activite ?authenticite ?impact ?communaute ?initiative
    WHERE {
        ?activite rdf:type eco:ActivitéTouristique .
        ?activite eco:aAuthenticitéLocale ?authenticite .
        ?activite eco:aImpactEnvironnemental ?impact .
        ?activite eco:implique ?communaute .
        ?communaute eco:aInitiativeDurable ?initiative .
        FILTER(CONTAINS(LCASE(?impact), "faible"))
    }
    """
    
    # Requête 6: Gastronomie locale utilisant ressources durables
    QUERY_6_LOCAL_GASTRONOMY = PREFIX + """
    SELECT ?gastronomie ?produitLocal ?ressource ?fragilite
    WHERE {
        ?gastronomie rdf:type eco:GastronomieLocale .
        ?gastronomie eco:aProduitLocal ?produitLocal .
        ?gastronomie eco:utilise ?ressource .
        ?ressource eco:aFragilité ?fragilite .
        FILTER(?produitLocal = true)
    }
    """
    
    # Requête 7: Événements culturels par saison et destination
    QUERY_7_CULTURAL_EVENTS = PREFIX + """
    SELECT ?evenement ?saison ?destination ?localisation
    WHERE {
        ?destination rdf:type eco:Destination .
        ?destination eco:organise ?evenement .
        ?destination eco:aLocalisation ?localisation .
        ?evenement rdf:type eco:ÉvénementCulturel .
        ?evenement eco:aSaison ?saison .
    }
    ORDER BY ?saison
    """
    
    # Requête 8: Analyse complète d'une destination écologique
    QUERY_8_DESTINATION_ANALYSIS = PREFIX + """
    SELECT ?destination ?localisation ?biodiversite 
           (COUNT(DISTINCT ?hebergement) AS ?nbHebergements)
           (AVG(?energie) AS ?energieMoyenne)
           (COUNT(DISTINCT ?evenement) AS ?nbEvenements)
    WHERE {
        ?destination rdf:type eco:Destination .
        ?destination eco:aLocalisation ?localisation .
        OPTIONAL { ?destination eco:aBiodiversité ?biodiversite }
        OPTIONAL {
            ?destination eco:propose ?hebergement .
            ?hebergement eco:aConsommationÉnergie ?energie
        }
        OPTIONAL { ?destination eco:organise ?evenement }
    }
    GROUP BY ?destination ?localisation ?biodiversite
    """
    
    # Requête 9: Certifications écologiques et critères respectés
    QUERY_9_CERTIFICATIONS = PREFIX + """
    SELECT ?certification ?niveau ?criteres (COUNT(?hebergement) AS ?nbHebergements)
    WHERE {
        ?certification rdf:type eco:CertificationÉcologique .
        ?certification eco:aNiveauCertification ?niveau .
        ?certification eco:aCritèreRespecté ?criteres .
        ?hebergement eco:aCertification ?certification .
    }
    GROUP BY ?certification ?niveau ?criteres
    ORDER BY DESC(?nbHebergements)
    """
    
    # Requête 10: Hiérarchie des types de transport et leurs empreintes
    QUERY_10_TRANSPORT_HIERARCHY = PREFIX + """
    SELECT ?typeTransport ?superClasse (AVG(?co2) AS ?co2Moyen) (COUNT(?transport) AS ?nbTransports)
    WHERE {
        ?transport rdf:type ?typeTransport .
        ?typeTransport rdfs:subClassOf ?superClasse .
        ?transport eco:aEmpreinte ?empreinte .
        ?empreinte eco:aCO2 ?co2 .
        FILTER(?typeTransport != owl:Thing && ?typeTransport != eco:Transport)
    }
    GROUP BY ?typeTransport ?superClasse
    ORDER BY ?co2Moyen
    """
    
    # Requête 11: Recommandations personnalisées par profil voyageur
    QUERY_11_PERSONALIZED_RECOMMENDATIONS = PREFIX + """
    SELECT ?voyageur ?budget ?profil ?destination ?hebergement ?energie ?certification
    WHERE {
        ?voyageur rdf:type eco:Voyageur .
        ?voyageur eco:aBudget ?budget .
        ?voyageur eco:aProfilÉcologique ?profil .
        ?voyageur eco:choisit ?destination .
        ?destination eco:propose ?hebergement .
        ?hebergement eco:aConsommationÉnergie ?energie .
        ?hebergement eco:aCertification ?certification .
        FILTER(?energie < 200)
    }
    ORDER BY ?energie
    """
    
    # Requête 12: Analyse d'impact environnemental global
    QUERY_12_ENVIRONMENTAL_IMPACT = PREFIX + """
    SELECT ?destination 
           (AVG(?energie) AS ?energieMoyenne)
           (COUNT(DISTINCT ?activite) AS ?nbActivitesFaibleImpact)
           (COUNT(DISTINCT ?certification) AS ?nbCertifications)
    WHERE {
        ?destination rdf:type eco:Destination .
        OPTIONAL {
            ?destination eco:propose ?hebergement .
            ?hebergement eco:aConsommationÉnergie ?energie .
            ?hebergement eco:aCertification ?certification
        }
        OPTIONAL {
            ?activite rdf:type eco:ActivitéTouristique .
            ?activite eco:aImpactEnvironnemental ?impact .
            FILTER(CONTAINS(LCASE(?impact), "faible"))
        }
    }
    GROUP BY ?destination
    ORDER BY DESC(?nbCertifications) DESC(?nbActivitesFaibleImpact) ?energieMoyenne
    """
    
    # Requête 13: Communautés locales et initiatives durables
    QUERY_13_LOCAL_COMMUNITIES = PREFIX + """
    SELECT ?communaute ?initiative (COUNT(?activite) AS ?nbActivites)
    WHERE {
        ?communaute rdf:type eco:CommunautéLocale .
        ?communaute eco:aInitiativeDurable ?initiative .
        ?activite eco:implique ?communaute .
    }
    GROUP BY ?communaute ?initiative
    ORDER BY DESC(?nbActivites)
    """
    
    # Requête 14: Ressources naturelles fragiles et leur utilisation
    QUERY_14_NATURAL_RESOURCES = PREFIX + """
    SELECT ?ressource ?fragilite (COUNT(?gastronomie) AS ?utilisations)
    WHERE {
        ?ressource rdf:type eco:RessourceNaturelle .
        ?ressource eco:aFragilité ?fragilite .
        ?gastronomie eco:utilise ?ressource .
    }
    GROUP BY ?ressource ?fragilite
    ORDER BY DESC(?utilisations)
    """
    
    # Requête 15: Score écologique composite par destination
    QUERY_15_ECO_SCORE = PREFIX + """
    SELECT ?destination ?localisation
           (AVG(?energie) AS ?scoreEnergie)
           (COUNT(DISTINCT ?certification) AS ?scoreCertification)
           (COUNT(DISTINCT ?activiteFaible) AS ?scoreActivites)
           ((100 - AVG(?energie)) + (COUNT(DISTINCT ?certification) * 10) + 
            (COUNT(DISTINCT ?activiteFaible) * 5) AS ?scoreTotal)
    WHERE {
        ?destination rdf:type eco:Destination .
        ?destination eco:aLocalisation ?localisation .
        OPTIONAL {
            ?destination eco:propose ?hebergement .
            ?hebergement eco:aConsommationÉnergie ?energie .
            ?hebergement eco:aCertification ?certification
        }
        OPTIONAL {
            ?activiteFaible rdf:type eco:ActivitéTouristique .
            ?activiteFaible eco:aImpactEnvironnemental ?impact .
            FILTER(CONTAINS(LCASE(?impact), "faible"))
        }
    }
    GROUP BY ?destination ?localisation
    ORDER BY DESC(?scoreTotal)
    """

    @staticmethod
    def get_all_queries():
        """Retourne toutes les requêtes disponibles"""
        return {
            'eco_accommodations': SPARQLQueries.QUERY_1_ECO_ACCOMMODATIONS,
            'biodiversity_destinations': SPARQLQueries.QUERY_2_BIODIVERSITY_DESTINATIONS,
            'transport_comparison': SPARQLQueries.QUERY_3_TRANSPORT_COMPARISON,
            'eco_travelers': SPARQLQueries.QUERY_4_ECO_TRAVELERS,
            'low_impact_activities': SPARQLQueries.QUERY_5_LOW_IMPACT_ACTIVITIES,
            'local_gastronomy': SPARQLQueries.QUERY_6_LOCAL_GASTRONOMY,
            'cultural_events': SPARQLQueries.QUERY_7_CULTURAL_EVENTS,
            'destination_analysis': SPARQLQueries.QUERY_8_DESTINATION_ANALYSIS,
            'certifications': SPARQLQueries.QUERY_9_CERTIFICATIONS,
            'transport_hierarchy': SPARQLQueries.QUERY_10_TRANSPORT_HIERARCHY,
            'personalized_recommendations': SPARQLQueries.QUERY_11_PERSONALIZED_RECOMMENDATIONS,
            'environmental_impact': SPARQLQueries.QUERY_12_ENVIRONMENTAL_IMPACT,
            'local_communities': SPARQLQueries.QUERY_13_LOCAL_COMMUNITIES,
            'natural_resources': SPARQLQueries.QUERY_14_NATURAL_RESOURCES,
            'eco_score': SPARQLQueries.QUERY_15_ECO_SCORE
        }
