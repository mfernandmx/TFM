#!/usr/bin/python
# -*- coding: utf-8 -*-

import math

'''
Given the set of words from a dataset and their frequency of appearance, it returns the average frequency of appearance of any word
'''
def calculateWordsAvgFrequency(words):

	totalFrequency = 0

	for word in list(words):
		totalFrequency += words[word]

	return float(totalFrequency) / float(len(list(words)))


'''
Given the set of words from a dataset, it returns the local weights for all those words in the dataset

The different local modes are the following:
BNRY (Binary)
FREQ (Wuthin-document frequency)
LOGA (Log)
LOGN (Normalized log)
ATF1 (Augmented normalized term frequency)
'''
def localWeight(words):

	datasetLocalWeights = {}

	# Maximum frequency of appearance for any word in the dataset
	maximumFrequency = 0

	avgFrequency = calculateWordsAvgFrequency(words)

	for word in list(words):
		if words[word] > maximumFrequency:
			maximumFrequency = words[word]

	for word in list(words):

		datasetLocalWeights[word] = {
			"BNRY": 1,
			"FREQ": words[word],
			"LOGA": 1 + math.log(words[word]),
			"LOGN": (1 + math.log(words[word])) / (1 + math.log(avgFrequency)),
			"ATF1": 0.5 + 0.5 * (words[word] / maximumFrequency)
		}

	return datasetLocalWeights


'''
Auxiliary method to calculate the entropy property for a concrete word in a dataset
'''
def globalWeightEntropy(coincidences, word):

	datasetGlobalWeightEntropy = 1
	numberOfDatasets = len(list(coincidences)) - 2

	for dataset in list(coincidences):
		if dataset != 'totalCoincidences' and dataset != 'datasetCoincidences':
			if word in coincidences[dataset]:

				datasetGlobalWeightEntropy += (
					(
						float(coincidences[dataset][word]) / float(coincidences['totalCoincidences'][word])
					)
					*
					(
						float(
							math.log((float(coincidences[dataset][word]) / float(coincidences['totalCoincidences'][word])))
						)
						/ math.log(numberOfDatasets)
					)
				)

	return datasetGlobalWeightEntropy


'''
Given the set of words from a dataset, it returns the global weights for all those words considering all the datasets

The different global modes are the following:
IDFB (Inverse document frequency)
IDFP (Probabilistic inverse)
ENPY (Entropy)
IGFF (Global frequency IDF)
NONE (No glonal weight)
'''
def globalWeight(coincidences):

	datasetGlobalWeights = {}

	numberOfDatasets = len(list(coincidences)) - 2
	totalCoincidences = coincidences['totalCoincidences']
	datasetCoincidences = coincidences['datasetCoincidences']

	for word in list(totalCoincidences):

		# If the word appears in all datasets
		if numberOfDatasets == datasetCoincidences[word]:
			datasetGlobalWeights[word] = {
				"IDFB": math.log(numberOfDatasets / datasetCoincidences[word]),
				"IDFP": 0,
				"ENPY": globalWeightEntropy(coincidences, word),
				"IGFF": totalCoincidences[word] / datasetCoincidences[word],
				"NONE": 1
			}

		else:
			datasetGlobalWeights[word] = {
				"IDFB": math.log(numberOfDatasets / datasetCoincidences[word]),
				"IDFP": math.log(float(numberOfDatasets - datasetCoincidences[word]) / float(datasetCoincidences[word])),
				"ENPY": globalWeightEntropy(coincidences, word),
				"IGFF": totalCoincidences[word] / datasetCoincidences[word],
				"NONE": 1
			}

	return datasetGlobalWeights


'''
Given the set of words from a dataset, as well as their weights calculated previously and other factors,
it returns the normalization factor for the dataset

The different normalization factor modes are the following:
COSN (Cosine normalization)
PUQN (Pivoted unique normalization)
NONE (none)
'''
def normalizationFactor(words, datasetGlobalWeight, globalMode, datasetLocalWeight, localMode, slope, pivot):

	aux = 0
	for word in list(words):
		aux += math.pow((datasetGlobalWeight[word][globalMode]*datasetLocalWeight[word][localMode]), 2)

	datasetNormalizationFactor = {
		'COSN': float(1)/float(math.sqrt(aux)),
		'PUQN': float(1)/float((1-slope)*pivot + slope*len(words)),
		'NONE': 1
	}

	return datasetNormalizationFactor


'''
Given the title of a dataset, and the coincidences object of the portal where the dataset came from, it returns an object
with the final weight of each of its words
'''
def calculateDatasetWeights(title, coincidences):

	datasetLocalWeight = localWeight(coincidences[title])
	datasetGlobalWeight = globalWeight(coincidences)

	# Constant value
	slope = 0.2

	# Average number of ditinct terms por dataset in the entire collection
	pivot = 0

	for word in list(coincidences):
		if word != 'datasetCoincidences' and word != 'totalCoincidences':
			pivot += len(coincidences[word])

	pivot = pivot / (len(coincidences) - 2)

	combinations = [
		{"localMode": "LOGA", "globalMode": "IGFF", "normalizationMode": "COSN"},
		{"localMode": "FREQ", "globalMode": "IDFB", "normalizationMode": "COSN"}
	]

	datasetWeights = []

	for comb in combinations:

		localMode = comb["localMode"]
		globalMode = comb["globalMode"]
		normalizationMode = comb["normalizationMode"]

		datasetNormalizationFactor = normalizationFactor(coincidences[title], datasetGlobalWeight, globalMode, datasetLocalWeight, localMode, slope, pivot)

		weights = {}

		for word in coincidences[title]:
			weights[word] = (datasetLocalWeight[word][localMode] * datasetGlobalWeight[word][globalMode] * datasetNormalizationFactor[normalizationMode])

		datasetWeights.append({"modes": comb, "weights": weights})

	return datasetWeights
