#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
from random import uniform

from scripts.tokenizer import tokenize

'''
Given all the metadata from a dataset, this method tokenize it with a series of process,
including removing gender, number, urls, queries, etc.
It is also necessary the coincidences array in order to discard those who appears more than a threshold
'''
# TODO Revisar
def getTokens(metadata, coincidences):

	# Get tokens from all metadata
	tokenized = tokenize(metadata)

	# Repeated words are removed
	tokens_without_duplicates = list(set(tokenized))

	# Remove those words which occurrence frequency is over 50%
	key_words = [i for i in tokens_without_duplicates if (i in coincidences and coincidences[i] < 0.5)]

	# Iterate over every token checking if it is contained in another, removing the longest one
	end_tokens = list(key_words)
	'''
	for i in end_tokens:
		aux = list(end_tokens)
		aux.remove(i)
		for j in aux:
			if i in j:
				end_tokens.remove(j)
				print("Removing", j, "from", i)
	'''
	return end_tokens


'''
Given all datasets' metadata from two open data portals, it creates and JSON object with likeness value between all of them
'''
def processDatasets(datasets1, datasets2):

	print("Processing datasets")
	print("Obtaining words occurrence frequency")

	with open("./coincidences1.json") as jsonData1:
		coincidences1 = json.load(jsonData1)

	with open("./coincidences2.json") as jsonData2:
		coincidences2 = json.load(jsonData2)

	generalId = 0

	results = {}

	# Iterate over all datasets
	for dataset1 in datasets1:

		results[str(generalId)] = {"title": dataset1.title, "rdfs": [], "results": []}

		for RDFResource in dataset1.RDFResources:
			results[str(generalId)]["rdfs"].append(RDFResource)

		# Get tokens from metadata
		metadata1 = dataset1.title + " " + dataset1.identifier + " " + str(
			dataset1.keyword) + " " + dataset1.theme + " " + dataset1.description
		tokens1 = getTokens(metadata1, coincidences1)

		for dataset2 in datasets2:

			# Get tokens from metadata
			metadata2 = dataset2.title + " " + dataset2.identifier + " " + str(
				dataset2.keyword) + " " + dataset2.theme + " " + dataset2.description
			tokens2 = getTokens(metadata2, coincidences2)

			# TODO: Where magic will happen
			# likenessValue = getLikenessValue(tokens1, tokens2)
			likenessValue = uniform(0.0, 1.0)

			results[str(generalId)]["results"].append({"title": dataset2.title, "value": likenessValue, "rdfs": []})

			for RDFResource in dataset2.RDFResources:
				results[str(generalId)]["results"][len(results[str(generalId)]["results"]) - 1]["rdfs"].append(RDFResource)

		generalId += 1

	print("Sending results")

	return results
