#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests

from rdflib import Graph
from rdflib.plugins.sparql import prepareQuery

def removeOntology(value):
    if "#" in value:
        newValue = value.split("#")[1]
    else:
        split = value.split("/")
        newValue = split[len(split) - 1]

    return newValue

def processRDF(url):

    graph = Graph()
    classes = []
    properties = {}

    try:
        # Download and load RDF resource
        graph.parse(url)

        if len(graph) > 0:
            # Query and store classes
            queryResults = graph.query("""SELECT DISTINCT ?type WHERE{?uri a ?type}""")

            for result in queryResults:
                classes.append(removeOntology(result[0]))

            # Query and store properties, its datatype and one example value
            query = prepareQuery("""SELECT DISTINCT ?property ?value WHERE {?uri ?property ?value}""")
            queryResults = graph.query(query)

            for result in queryResults:
                prop = removeOntology(result[0])
                value = result[1]

                if hasattr(result[1], "datatype") and result[1].datatype is not None:
                    valueType = removeOntology(result[1].datatype)
                else:
                    valueType = result[1].__class__.__name__

                if prop != "type" and prop not in properties.keys():
                    properties[prop] = {"value": str(value), "type": valueType}

    except requests.exceptions.RequestException as e:
        print(e)
        return [], []

    return classes, properties
