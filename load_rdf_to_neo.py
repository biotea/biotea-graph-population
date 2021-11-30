from py2neo import Graph
import glob
import logging
import os
import config


FORMAT = "RDF/XML"
PREFIX_DEFINITIONS = {
    "pav": "http://purl.org/pav/",
    "sio": "http://semanticscience.org/resource/",
    "foaf": "http://xmlns.com/foaf/0.1/",
    "aoc": "http://purl.org/ao/core/",
    "aot": "http://purl.org/ao/types/",
    "bibo": "http://purl.org/ontology/bibo/",
    "prov": "http://www.w3.org/ns/prov#",
    "biotea": "https://biotea.github.io/biotea-ontololgy#",
    "doco": "http://purl.org/spar/doco/",
    "wd": "http://www.wikidata.org/entity/",
    "skos": "http://www.w3.org/2004/02/skos/core#",
    "owl": "http://www.w3.org/2002/07/owl#",
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#"
}

MAPPINGS_DEFINITIONS = {
    "http://www.w3.org/2004/02/skos/core#prefLabel": "prefLabel",
    "http://www.w3.org/2004/02/skos/core#altLabel": "altLabel",
    "http://www.w3.org/2004/02/skos/core#definition": "definition"
}

def init_graph(graph: Graph):
    logging.info("Creating index on Resource(uri)")
    create_uri_index(graph)
    logging.info("Done")

    logging.info("Setting initial graph configuration")
    create_initial_graph_configuration(graph)
    logging.info("Done")

    logging.info("Creating custom prefix definitions")
    create_custom_prefixes(graph)
    logging.info("Done")

    logging.info("Creating mappings")
    create_mappings(graph)
    logging.info("Done")



def create_uri_index(graph: Graph):
    graph.run("CREATE CONSTRAINT n10s_unique_uri ON (r:Resource) ASSERT r.uri IS UNIQUE;")


def create_initial_graph_configuration(graph: Graph):
    graph.run(f"call n10s.graphconfig.init( {{ "
              f"handleVocabUris: 'SHORTEN', "
              f"handleMultival: 'ARRAY', "
              f"handleRDFTypes: 'LABELS_AND_NODES', "
              f"classLabel: '{config.ONTOLOGY_CLASS_LABEL}', "
              f"subClassOfRel: '{config.ONTOLOGY_SUB_CLASS_OF_LABEL}', "
              f"dataTypePropertyLabel: '{config.ONTOLOGY_DATA_TYPE_PROPERTY_LABEL}', "
              f"objectPropertyLabel: '{config.ONTOLOGY_OBJECT_PROPERTY_LABEL}', "
              f"subPropertyOfRel: '{config.ONTOLOGY_SUB_PROPERTY_OF_LABEL}', "
              f"domainRel: '{config.ONTOLOGY_DOMAN_LABEL}', "
              f"rangeRel: '{config.ONTOLOGY_RANGE_LABEL}' }});")


def create_custom_prefixes(graph: Graph):
    for prefix, url in PREFIX_DEFINITIONS.items():
        graph.run('CALL n10s.nsprefixes.add("{}","{}")'.format(prefix, url))

def create_mappings(graph: Graph):
    for uri, neo_element in MAPPINGS_DEFINITIONS.items():
        graph.run(f'CALL n10s.mapping.add("{uri}", "{neo_element}")')

def load_rdf_folder(graph: Graph, system_path: str, docker_path: str):
    for file in glob.glob(system_path + "*.rdf"):
        file_in_docker = docker_path + str(os.path.basename(file))
        statement = f'CALL n10s.rdf.import.fetch("file://{file_in_docker}", "{FORMAT}")'
        res = graph.run(statement).to_table()
        if res[0][0] != 'OK':
            logging.warn("{} {} {}.".format(file, res[0][0], res[0][4]))
        else:
            logging.info("{} {} {} triples created.".format(file, res[0][0], res[0][1]))


def load_ontologies_folder(graph: Graph, system_path: str, docker_path: str):
    for file in glob.glob(system_path + "*.owl"):
        file_in_docker = docker_path + str(os.path.basename(file))
        statement = f'CALL n10s.onto.import.fetch("file://{file_in_docker}", "{FORMAT}")'
        res = graph.run(statement).to_table()
        if res[0][0] != 'OK':
            logging.warn("{} {} {}.".format(file, res[0][0], res[0][4]))
        else:
            logging.info("{} {} {} triples created.".format(file, res[0][0], res[0][1]))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    graph = Graph(config.BOLT, auth=(config.USER, config.PASS))

    logging.info("Initializing graph")
    init_graph(graph)
    logging.info("Graph initialized")

    logging.info("Loading RDF files")
    load_rdf_folder(graph, config.INPUT_RDF_FOLDER, config.INPUT_DOCKER_RDF_FOLDER)
    logging.info("Done")

    logging.info("Loading annotation files")
    load_rdf_folder(graph, config.INPUT_ANNOTATIONS_FOLDER, config.INPUT_DOCKER_ANNOTATIONS_FOLDER)
    logging.info("Done")

    logging.info("Loading ontology files")
    load_ontologies_folder(graph, config.INPUT_ONTOLOGIES_FOLDER, config.INPUT_DOCKER_ONTOLOGIES_FOLDER)
    logging.info("Done")
