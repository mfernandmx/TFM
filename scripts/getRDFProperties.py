#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests

# import rdflib
from rdflib import Graph
# from rdflib.plugins.sparql import prepareQuery

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
    properties = []

    try:
        # Download and load RDF resource
        graph.parse(url)

        if len(graph) > 0:
            # Query and store classes
            queryResults = graph.query("""SELECT DISTINCT ?type WHERE{?uri a ?type}""")

            for result in queryResults:
                classes.append(removeOntology(result[0]))
                print(removeOntology(result[0]))

            # TODO
            '''
            # Query and store properties, its datatype and one example value
            query = prepareQuery("""SELECT DISTINCT ?property min(?value) as ?valor datatype(min(?value)) as ?tipo WHERE {?uri ?property ?value}""")
            queryResults = graph.query(query)

            for result in queryResults:
                print(result)
            '''

    except requests.exceptions.RequestException as e:
        print(e)
        return [], []

    return classes, properties
