#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
from random import uniform
import xlwt  # lib to write.

import re
import normalize

# LDA proccess
from nltk.tokenize import RegexpTokenizer
from nltk.stem import SnowballStemmer

# import nltk
from nltk.corpus import stopwords
# nltk.download('stopwords')
stop_words = stopwords.words('spanish')

class Dataset:
	title = ""
	identifier = ""

	description = ""
	keyword = []
	language = ""
	theme = ""
	RDFResources = []
	DCATformat = True
	resourceFormats = []

	def __init__(self):
		self.keyword = []
		self.resourceFormats = []
		self.RDFResources = []


def hasNumbers(inputString):
	# return any(char.isdigit() for char in inputString)
	return bool(re.search(r'\d', inputString))


# TODO: Revisar, traducir comentarios
def getTokens(metadata, data):
	# eliminamos urls
	text = re.sub(r'http.+', '', metadata)
	# eliminamos propiedades y valores de consultas sparql
	text = re.sub(r'\w+:\w+', '', text)
	text = re.sub(r'\?\w+', '', text)

	# tokeinizamos
	tokenizer = RegexpTokenizer(r'\w+')
	tokenized = text.split(" ")

	aux = [normalize.normalizar(token) for token in tokenized]

	tokenized = tokenizer.tokenize(str(aux))

	# if dataset1.language == "es":

	# d = enchant.Dict('es_ANY')
	# else:
	# stop_words = get_stop_words('en')
	# d = enchant.Dict('en_GB')

	# eliminamos palabras repetidas
	tokens_without_duplicates = list(set(tokenized))

	# eliminamos stop words
	# stop_words = get_stop_words('es')
	stopped_tokens = [i for i in tokens_without_duplicates if i not in stop_words]

	# print("stopped_tokens: ",stopped_tokens)
	# eliminamos aquello que no sea una palabra, por ejemplo: códigos
	# words_tokens = [i for i in stopped_tokens if i in words.words()]
	# words_tokens = [i for i in stopped_tokens if d.check(i)]

	# print("words_tokens: ",words_tokens)

	# eliminar números
	words_without_numbers = [i for i in stopped_tokens if not hasNumbers(str(i))]

	# print("words_without_numbers: ",words_without_numbers)

	# eliminamos aquellas palabras cuya frecuencia de ocurencia en los metadatos del total de datasets sea superior al 50%
	key_words = [i for i in words_without_numbers if (i in data and data[i] < 0.5)]
	# key_tokens = [i for i in words_without_numbers if not i in key_words]
	# print("---------")

	print("key_words: ", key_words)
	print("---------")

	# eliminamos género y número de las palabras
	# p_stemmer = PorterStemmer()
	# stemmers = [p_stemmer.stem(i) for i in key_words]
	# languages = ('arabic', 'danish', 'dutch', 'english', 'finnish', 'french', 'german', 'hungarian', 'italian', 'norwegian', 'porter', 'portuguese', 'romanian', 'russian', 'spanish', 'swedish')
	p_stemmer = SnowballStemmer('spanish')
	texts = [p_stemmer.stem(i) for i in key_words]
	print("stemmers: ", texts)

	# obtenemos el lexema de las palabras
	# lemmatizer = WordNetLemmatizer()
	# texts = [lemmatizer.lemmatize(i) for i in key_words]
	# print("lemmas: ", texts)

	# comprobamos si cada uno de los tokens está contenido en otro, eliminando en este caso, el de mayor longitud
	end_tokens = list(texts)
	for i in end_tokens:
		aux = list(end_tokens)
		aux.remove(i)
		for j in aux:
			if i in j:
				end_tokens.remove(j)
				print("remove: ", i, j)

	print("end_tokens: ", end_tokens)

	return end_tokens

def processDatasets(datasets1, datasets2):
	print("Generating coincidences")

	print("Obtaining words occurrence frequency")

	with open("./coincidences1.json") as jsonData1:
		data1 = json.load(jsonData1)

	with open("./coincidences2.json") as jsonData2:
		data2 = json.load(jsonData2)

	wb = xlwt.Workbook(encoding="utf-8")

	generalSheet = wb.add_sheet("General", cell_overwrite_ok=True)
	generalRow = 0

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

		metadata1 = dataset1.title + " " + dataset1.identifier + " " + str(
			dataset1.keyword) + " " + dataset1.theme + " " + dataset1.description
		tokens1 = getTokens(metadata1, data1)

		for dataset2 in datasets2:

			column = 0

			metadata2 = dataset2.title + " " + dataset2.identifier + " " + str(
				dataset2.keyword) + " " + dataset2.theme + " " + dataset2.description
			tokens2 = getTokens(metadata2, data2)

			# Where magic will happen
			# likenessValue = getLikenessValue(tokens1, tokens2)
			likenessValue = uniform(0.0, 1.0)

			# Write in excel
			sheet.write(row, column, dataset2.title)
			column += 1
			sheet.write(row, column, likenessValue)

			for RDFResource in dataset2.RDFResources:
				column += 1
				sheet.write(row, column, RDFResource)

			row += 1

		generalRow += 1

	wb.save("results.xls")
