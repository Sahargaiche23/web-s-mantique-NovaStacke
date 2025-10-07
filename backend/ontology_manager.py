"""
Gestionnaire d'ontologie RDF avec rdflib
"""
from rdflib import Graph, Namespace, RDF, RDFS, OWL, Literal, URIRef
from rdflib.namespace import XSD
import os

class OntologyManager:
    """Gère le chargement et les requêtes sur l'ontologie"""
    
    def __init__(self, ontology_path):
        self.graph = Graph()
        self.ontology_path = ontology_path
        self.eco = Namespace("http://example.org/ecotourisme#")
        self.graph.bind("eco", self.eco)
        self.graph.bind("rdf", RDF)
        self.graph.bind("rdfs", RDFS)
        self.graph.bind("owl", OWL)
        self.graph.bind("xsd", XSD)
        
    def load_ontology(self):
        """Charge l'ontologie depuis le fichier OWL"""
        try:
            self.graph.parse(self.ontology_path, format="xml")
            print(f"✓ Ontologie chargée: {len(self.graph)} triples")
            return True
        except Exception as e:
            print(f"✗ Erreur chargement ontologie: {e}")
            return False
    
    def execute_sparql(self, query):
        """Exécute une requête SPARQL"""
        try:
            results = self.graph.query(query)
            return self._format_results(results)
        except Exception as e:
            print(f"Erreur SPARQL: {e}")
            return []
    
    def _format_results(self, results):
        """Formate les résultats SPARQL en liste de dictionnaires"""
        formatted = []
        for row in results:
            result_dict = {}
            for var in results.vars:
                value = row[var]
                if value:
                    result_dict[str(var)] = self._format_value(value)
            formatted.append(result_dict)
        return formatted
    
    def _format_value(self, value):
        """Formate une valeur RDF"""
        if isinstance(value, Literal):
            return str(value)
        elif isinstance(value, URIRef):
            # Extraire le nom local de l'URI
            return str(value).split('#')[-1].split('/')[-1]
        return str(value)
    
    def get_all_classes(self):
        """Récupère toutes les classes de l'ontologie"""
        query = """
        SELECT DISTINCT ?class ?label
        WHERE {
            ?class rdf:type owl:Class .
            OPTIONAL { ?class rdfs:label ?label }
        }
        ORDER BY ?class
        """
        return self.execute_sparql(query)
    
    def get_all_properties(self):
        """Récupère toutes les propriétés"""
        query = """
        SELECT DISTINCT ?property ?type ?domain ?range
        WHERE {
            {
                ?property rdf:type owl:ObjectProperty .
                BIND("ObjectProperty" AS ?type)
            } UNION {
                ?property rdf:type owl:DatatypeProperty .
                BIND("DatatypeProperty" AS ?type)
            }
            OPTIONAL { ?property rdfs:domain ?domain }
            OPTIONAL { ?property rdfs:range ?range }
        }
        ORDER BY ?property
        """
        return self.execute_sparql(query)
    
    def get_all_individuals(self):
        """Récupère tous les individus"""
        query = """
        SELECT DISTINCT ?individual ?type
        WHERE {
            ?individual rdf:type ?type .
            ?type rdf:type owl:Class .
        }
        ORDER BY ?individual
        """
        return self.execute_sparql(query)
    
    def get_individuals_by_class(self, class_name):
        """Récupère les individus d'une classe spécifique"""
        query = f"""
        PREFIX eco: <http://example.org/ecotourisme#>
        SELECT ?individual ?property ?value
        WHERE {{
            ?individual rdf:type eco:{class_name} .
            ?individual ?property ?value .
        }}
        """
        return self.execute_sparql(query)
    
    def add_individual(self, class_name, individual_name, properties):
        """Ajoute un nouvel individu à l'ontologie"""
        try:
            individual_uri = self.eco[individual_name]
            class_uri = self.eco[class_name]
            
            # Ajouter le type
            self.graph.add((individual_uri, RDF.type, class_uri))
            
            # Ajouter les propriétés
            for prop_name, value in properties.items():
                prop_uri = self.eco[prop_name]
                
                if isinstance(value, str) and value.startswith('http://'):
                    # C'est une référence à un autre individu
                    self.graph.add((individual_uri, prop_uri, URIRef(value)))
                elif isinstance(value, bool):
                    self.graph.add((individual_uri, prop_uri, Literal(value, datatype=XSD.boolean)))
                elif isinstance(value, (int, float)):
                    self.graph.add((individual_uri, prop_uri, Literal(value, datatype=XSD.decimal)))
                else:
                    self.graph.add((individual_uri, prop_uri, Literal(value, datatype=XSD.string)))
            
            return True
        except Exception as e:
            print(f"Erreur ajout individu: {e}")
            return False
    
    def save_ontology(self, output_path=None):
        """Sauvegarde l'ontologie modifiée"""
        try:
            path = output_path or self.ontology_path
            self.graph.serialize(destination=path, format='xml')
            print(f"✓ Ontologie sauvegardée: {path}")
            return True
        except Exception as e:
            print(f"✗ Erreur sauvegarde: {e}")
            return False
    
    def get_statistics(self):
        """Retourne des statistiques sur l'ontologie"""
        # Compte des individus: ne dépend pas de owl:NamedIndividual qui n'est pas toujours déclaré
        try:
            individuals_list = self.get_all_individuals()
            individuals_count = len(individuals_list)
        except Exception:
            individuals_count = 0

        stats = {
            'total_triples': len(self.graph),
            'classes': len(list(self.graph.subjects(RDF.type, OWL.Class))),
            'object_properties': len(list(self.graph.subjects(RDF.type, OWL.ObjectProperty))),
            'datatype_properties': len(list(self.graph.subjects(RDF.type, OWL.DatatypeProperty))),
            'individuals': individuals_count
        }
        return stats
    
    def search_by_text(self, search_text):
        """Recherche textuelle dans l'ontologie"""
        search_text = search_text.lower()
        query = f"""
        SELECT DISTINCT ?subject ?predicate ?object
        WHERE {{
            ?subject ?predicate ?object .
            FILTER(
                CONTAINS(LCASE(STR(?subject)), "{search_text}") ||
                CONTAINS(LCASE(STR(?object)), "{search_text}")
            )
        }}
        LIMIT 100
        """
        return self.execute_sparql(query)
    
    def get_related_entities(self, entity_name):
        """Récupère toutes les entités liées à une entité donnée"""
        query = f"""
        PREFIX eco: <http://example.org/ecotourisme#>
        SELECT DISTINCT ?relation ?relatedEntity
        WHERE {{
            {{
                eco:{entity_name} ?relation ?relatedEntity .
                FILTER(isURI(?relatedEntity))
            }} UNION {{
                ?relatedEntity ?relation eco:{entity_name} .
            }}
        }}
        """
        return self.execute_sparql(query)
