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
            query = prepareQuery("""SELECT DISTINCT ?property WHERE {?uri ?property ?value}""")
            queryResults = graph.query(query)

            # Iterate over properties
            for result in queryResults:

                prop = removeOntology(result[0])

                if prop != "type":

                    # Get one example value from each property
                    query = prepareQuery("""SELECT DISTINCT ?value WHERE {?uri ?property ?value} limit 1""")
                    queryResults2 = graph.query(query, initBindings={'property': result[0]})

                    exampleValue = ""
                    for row in queryResults2:
                        exampleValue = row
                        break

                    value = exampleValue[0]

                    if hasattr(value, "datatype") and value.datatype is not None:
                        valueType = removeOntology(value.datatype)
                    else:
                        valueType = value.__class__.__name__

                    if prop not in properties.keys():
                        properties[prop] = {"value": str(value), "type": valueType}

    except requests.exceptions.RequestException as e:
        print(e)
        return [], []

    return classes, properties
