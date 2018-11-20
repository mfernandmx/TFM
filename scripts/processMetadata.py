#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
from random import uniform
import xlwt  # lib to write.

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
Given all datasets' metadata from two open data portals, it creates and XLS file with likeness value between all of them
'''
def processDatasets(datasets1, datasets2):

	print("Processing datasets")
	print("Obtaining words occurrence frequency")

	with open("./coincidences1.json") as jsonData1:
		coincidences1 = json.load(jsonData1)

	with open("./coincidences2.json") as jsonData2:
		coincidences2 = json.load(jsonData2)

	# Create xls file
	wb = xlwt.Workbook(encoding="utf-8")
	generalSheet = wb.add_sheet("General", cell_overwrite_ok=True)
	generalRow = 0

	# Iterate over all datasets
	for dataset1 in datasets1:

		generalColumn = 0

		generalSheet.write(generalRow, generalColumn, generalRow)
		generalColumn += 1
		generalSheet.write(generalRow, generalColumn, dataset1.title)

		for RDFResource in dataset1.RDFResources:
			generalColumn += 1
			generalSheet.write(generalRow, generalColumn, RDFResource)

		sheet = wb.add_sheet(str(generalRow), cell_overwrite_ok=True)

		row = 0

		# Get tokens from metadata
		metadata1 = dataset1.title + " " + dataset1.identifier + " " + str(
			dataset1.keyword) + " " + dataset1.theme + " " + dataset1.description
		tokens1 = getTokens(metadata1, coincidences1)

		for dataset2 in datasets2:

			column = 0

			# Get tokens from metadata
			metadata2 = dataset2.title + " " + dataset2.identifier + " " + str(
				dataset2.keyword) + " " + dataset2.theme + " " + dataset2.description
			tokens2 = getTokens(metadata2, coincidences2)

			# TODO: Where magic will happen
			# likenessValue = getLikenessValue(tokens1, tokens2)
			likenessValue = uniform(0.0, 1.0)

			# Write in xls file
			sheet.write(row, column, dataset2.title)
			column += 1
			sheet.write(row, column, likenessValue)

			for RDFResource in dataset2.RDFResources:
				column += 1
				sheet.write(row, column, RDFResource)

			row += 1

		generalRow += 1

	print("Saving results")

	return wb
