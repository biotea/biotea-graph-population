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
}



def create_uri_index(graph: Graph):
    graph.run("CREATE INDEX ON :Resource(uri)")


def create_custom_prefixes(graph: Graph):
    for prefix, url in PREFIX_DEFINITIONS.items():
        graph.run('CALL semantics.addNamespacePrefix("{}","{}")'.format(prefix, url))


def load_rdf_folder(graph: Graph, system_path: str, docker_path: str):
    for file in glob.glob(system_path + "*.rdf"):
        file_in_docker = docker_path + str(os.path.basename(file))
        res = graph.run(
            'CALL semantics.importRDF("file://' + file_in_docker + '","' + FORMAT + '", { shortenUrls: false, typesToLabels: true, commitSize: 9000 })').to_table()
        if res[0][0] != 'OK':
            logging.warn("{} {} {}.".format(file, res[0][0], res[0][4]))
        else:
            logging.info("{} {} {} triples created.".format(file, res[0][0], res[0][1]))


def load_ontologies_folder(graph: Graph, system_path: str, docker_path: str):
    for file in glob.glob(system_path + "*.owl"):
        file_in_docker = docker_path + str(os.path.basename(file))
        statement = 'CALL semantics.importOntology("file://' + file_in_docker + '","' + FORMAT + '", { ' + 'classLabel: "{}", subClassOfRel: "{}", dataTypePropertyLabel: "{}", objectPropertyLabel: "{}", subPropertyOfRel: "{}", domainRel: "{}", rangeRel: "{}"'.format(
            config.ONTOLOGY_CLASS_LABEL, config.ONTOLOGY_SUB_CLASS_OF_LABEL, config.ONTOLOGY_DATA_TYPE_PROPERTY_LABEL,
            config.ONTOLOGY_OBJECT_PROPERTY_LABEL, config.ONTOLOGY_SUB_PROPERTY_OF_LABEL, config.ONTOLOGY_DOMAN_LABEL,
            config.ONTOLOGY_RANGE_LABEL) + ' })'
        res = graph.run(statement).to_table()
        if res[0][0] != 'OK':
            logging.warn("{} {} {}.".format(file, res[0][0], res[0][4]))
        else:
            logging.info("{} {} {} triples created.".format(file, res[0][0], res[0][1]))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    graph = Graph(config.BOLT, auth=(config.USER, config.PASS))
    logging.info("Creating index on Resource(uri)")
    create_uri_index(graph)
    logging.info("Done")
    logging.info("Creating custom prefix definitions")
    create_custom_prefixes(graph)
    logging.info("Done")
    logging.info("Loading RDF files")
    load_rdf_folder(graph, config.INPUT_RDF_FOLDER, config.INPUT_DOCKER_RDF_FOLDER)
    logging.info("Done")
    logging.info("Loading annotation files")
    load_rdf_folder(graph, config.INPUT_ANNOTATIONS_FOLDER, config.INPUT_DOCKER_ANNOTATIONS_FOLDER)
    logging.info("Done")
    logging.info("Loading ontology files")
    load_ontologies_folder(graph, config.INPUT_ONTOLOGIES_FOLDER, config.INPUT_DOCKER_ONTOLOGIES_FOLDER)
    logging.info("Done")
