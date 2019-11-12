# Configuration for the folders containing the rdf, annotations and ontologies to upload into neo4j.
# If you are using docker version of neo4j, you have to specify the mapped paths in docker in variables INPUT_DOCKER_*
# together with the paths in your file system in the rest of the INPUT_* variables.
# If you are not using neo4j docker, put the file system paths in both INPUT_DOCKER and INPUT variables.
INPUT_ANNOTATIONS_FOLDER = "insert_path_here"
INPUT_DOCKER_ANNOTATIONS_FOLDER = "insert_path_here"
INPUT_RDF_FOLDER = "insert_path_here"
INPUT_DOCKER_RDF_FOLDER = "insert_path_here"
INPUT_ONTOLOGIES_FOLDER = "insert_path_here"
INPUT_DOCKER_ONTOLOGIES_FOLDER = "insert_path_here"

# Configuration for neo4j connection
BOLT = "bolt://localhost:7687"
USER = "neo4j"
PASS = "pass"

# Configuration for the vocabulary used for uploading ontologies
ONTOLOGY_CLASS_LABEL = "Class"
ONTOLOGY_OBJECT_PROPERTY_LABEL = "Relation"
ONTOLOGY_DATA_TYPE_PROPERTY_LABEL = "Property"
ONTOLOGY_SUB_PROPERTY_OF_LABEL = "subPropertyOf"
ONTOLOGY_SUB_CLASS_OF_LABEL = "subClassOf"
ONTOLOGY_DOMAN_LABEL = "domain"
ONTOLOGY_RANGE_LABEL = "range"
