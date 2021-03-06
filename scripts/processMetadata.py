#!/usr/bin/python
# -*- coding: utf-8 -*-

from scripts.calculateWeights import calculateDatasetWeights
from scripts.calculateSimilarities import calculateLikenessValue

'''
Given all datasets' metadata from two open data portals, it creates a JSON object with the likeness value between all of them
'''
def processDatasets(datasets1, datasets2, coincidences1, coincidences2):

	print("Processing datasets")

	generalId = 0

	results = {}

	# Iterate over all datasets
	for dataset1 in datasets1:

		results[str(generalId)] = {"title": dataset1.title, "rdfs": [], "results": []}

		for RDFResource in dataset1.RDFResources:
			results[str(generalId)]["rdfs"].append(RDFResource)

		if len(coincidences1.keys()) > 2:

			# Calculate words weights for each dataset
			weights1 = calculateDatasetWeights(dataset1.title, coincidences1)

			for dataset2 in datasets2:

				if len(coincidences2.keys()) > 2:

					weights2 = calculateDatasetWeights(dataset2.title, coincidences2)

					# Based on the words weights, calculate the likeness value between two datasets
					likenessValue = calculateLikenessValue(weights1, weights2)

					results[str(generalId)]["results"].append({"title": dataset2.title, "value": likenessValue, "rdfs": []})

					for RDFResource in dataset2.RDFResources:
						results[str(generalId)]["results"][len(results[str(generalId)]["results"]) - 1]["rdfs"].append(RDFResource)

			generalId += 1

	print("Sending results")

	return results
