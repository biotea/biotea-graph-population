# biotea-graph-population
Scripts for Neo4j graph population from Biotea RDF output files.

Biotea produces RDF files describing:
* Article metadata, such as authors, references, journal and publisher.
* Article contents, providing information about sections, subsections, paragraphs and the content of the paragraphs.
* Annotations, including information about how part of the content of the paragraphs is identified by ontology concepts.

This script takes these files and load them into a Neo4j database through [neosemantics Neo4j plugin](https://github.com/neo4j-labs/neosemantics).

Ontologies used for annotation can be loaded into the database as well, providing a semantic context for each annotation.

## Usage
python load_rdf_to_file.py

The script does not have parameters. Options are read from config.py file, described below.

## Configuration
The configuration is set in config.py file. This file contains a set of parameters that are used by the script. These parameters are the following:
* **INPUT_ANNOTATIONS_FOLDER**. This parameter specifies the folder in which annotation RDF files are.
* **INPUT_DOCKER_ANNOTATIONS_FOLDER**. If you are using the docker version of Neo4j, this parameter should contain the folder mapped to INPUT_ANNOTATIONS_FOLDER in the docker container. If you are not using docker, this parameter should have the same value than INPUT_ANNOTATIONS_FOLDER.
* **INPUT_RDF_FOLDER**. This parameter specifies the folder in which metadata and content RDF files are stored.
* **INPUT_DOCKER_RDF_FOLDER**. If you are using the docker version of Neo4j, this parameter should contain the folder to mapped INPUT_RDF_FOLDER in the docker container. If you are not using docker, this parameter should have the same value than INPUT_RDF_FOLDER.
* **INPUT_ONTOLOGIES_FOLDER**. This parameter specifies the folder that contains the ontologies used in the annotation process. They should be in RDF/XML format.
* **INPUT_DOCKER_ONTOLOGIES_FOLDER**. If you are using the docker version of Neo4j, this parameter should contain the folder mapped to INPUT_ONTOLOGIES_FOLDER in the docker container. If you are not using docker, this parameter should have the same value than INPUT_ONTOLOGIES_FOLDER.

* **BOLT**. Contains the bolt connection address to the graph database; e.g. "bolt://localhost:7687".
* **USER**. Username to stablish the connection with the database.
* **PASS**. Password to stablish the connection with the database.

* **ONTOLOGY_CLASS_LABEL**. This parameter specifies the label for ontology classes when loading ontologies.
* **ONTOLOGY_OBJECT_PROPERTY_LABEL**. This parameter specifies the label for object properties when loading ontologies.
* **ONTOLOGY_DATA_TYPE_PROPERTY_LABEL**. This parameter specifies the label for data type properties when loading ontologies.
* **ONTOLOGY_SUB_PROPERTY_OF_LABEL**. This parameter specifies the label for sub property of relations when loading ontologies.
* **ONTOLOGY_SUB_CLASS_OF_LABEL**. This parameter specifies the label for sub class of relations when loading ontologies.
* **ONTOLOGY_DOMAN_LABEL**. This parameter specifies the label for domain relations when loading ontologies.
* **ONTOLOGY_RANGE_LABEL**. This parameter specifies the label for range relations when loading ontologies.

## Python Requirements
* [python 3.6](https://www.python.org/downloads/release/python-368/)
* [py2neo 4.3.0](https://py2neo.org/v4/)

## Neo4j requirements
Tested on [Neo4j 3.5.7 Community Edition](https://neo4j.com/release-notes/neo4j-3-5-7/) with the following plugins:
* [apoc-3.5.0.4](https://github.com/neo4j-contrib/neo4j-apoc-procedures/releases/tag/3.5.0.4)
* [neosemantics-3.5.0.3](https://github.com/neo4j-labs/neosemantics/releases/tag/3.5.0.3)

