#!/usr/bin/python
# -*- coding: utf-8 -*-

from nltk.corpus import wordnet as wn
from nltk.corpus import wordnet_ic

comb1 = "LOGA-IGFF-COSN"
comb2 = "FREQ-IDFB-COSN"

minRatio = 0.25

semcor_ic = wordnet_ic.ic('ic-semcor.dat')

# TODO Comentar

def processSimilarities(similarities):

	values = []
	valuesEqualtsToOne = 0

	keys1 = len(similarities.keys())
	keys2 = len(similarities[list(similarities.keys())[0]].keys())

	if keys1 <= keys2:

		for word1 in similarities.keys():

			maxValue = 0

			for word2 in similarities[word1].keys():
				if similarities[word1][word2] > maxValue:
					maxValue = similarities[word1][word2]

			if maxValue == 1:
				valuesEqualtsToOne += 1

			values.append(maxValue)

	else:

		for word2 in similarities[list(similarities.keys())[0]].keys():

			maxValue = 0

			for word1 in similarities.keys():
				if similarities[word1][word2] > maxValue:
					maxValue = similarities[word1][word2]

			if maxValue == 1:
				valuesEqualtsToOne += 1

			values.append(maxValue)

	numWords = len(values)
	percentage = float(1/numWords)

	print("VALUES", values)

	likenessValue = 0

	for value in values:
		if value == 1:
			aux = (percentage + (float(percentage/numWords) * (numWords - valuesEqualtsToOne))) * value
		else:
			aux = (percentage - (float(percentage/numWords) * valuesEqualtsToOne)) * value

		print(aux)

		likenessValue += aux

	return likenessValue

def calculateSimilarity(synset1, synset2):

	lin = synset1.lin_similarity(synset2, semcor_ic)
	path = synset1.path_similarity(synset2)

	return (lin + path) / 2

def calculateLikenessValue(weights1, weights2):

	print("WEIGHTS")
	print(weights1)
	print(weights2)

	similarities = {}

	for word1 in weights1[comb1].keys():

		if ((weights1[comb1][word1] > minRatio) and (weights1[comb2][word1] > 0)) or ((weights1[comb1][word1] * weights1[comb2][word1]) > 0.1):

			print("1.", word1, weights1[comb1][word1], weights1[comb2][word1], weights1[comb1][word1] * weights1[comb2][word1])
			synset1 = wn.synsets(word1, pos=wn.NOUN)

			if len(synset1) > 0:

				similarities[word1] = {}

				for word2 in weights2[comb1].keys():

					if ((weights2[comb1][word2] > minRatio) and (weights2[comb2][word2] > 0)) or ((weights2[comb1][word2] * weights2[comb2][word2]) > 0.1):

						print("2.", word2, weights2[comb1][word2], weights2[comb2][word2], weights2[comb1][word2] * weights2[comb2][word2])
						synset2 = wn.synsets(word2, pos=wn.NOUN)

						if len(synset2) > 0:

							similarity = calculateSimilarity(synset1[0], synset2[0])
							similarities[word1][word2] = similarity

	print(similarities)
	return processSimilarities(similarities)
