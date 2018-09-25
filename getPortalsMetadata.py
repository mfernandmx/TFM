#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import requests
import json

from processMetadata import processDatasets, Dataset
from nltk.tokenize import RegexpTokenizer
import re
import normalize

rdfFormats = ["rdf"]
# socrataFormat = ["csv", "geojson", "json", "rdf", "xml"]

'''
Given a list of datasets from an open data portal, it is obtained all the metadata from each dataset
'''
def getDatasetsInfoFromList(portal, datasets):
	data = []

	# Iterate over the list of datasets, and query on each of them
	for dataset in datasets["result"]:
		print(dataset)
		try:
			response = requests.get(portal.replace("package_list", "package_show?id=" + str(dataset)), timeout=5)
			dataJson = json.loads(response.content)
		except Exception as e:
			print(e)
			pass
			dataJson = json.loads({'result': ""})
		data.append(dataJson["result"])

	return data


'''
Given the metadata from a specific dataset, it tokenizes and filter its information, and count the frequency of
the words resulted
'''
def getNumCoincidences(metadata, coincidences):
	# function to test if something is a noun
	# is_noun = lambda pos: pos[:2] == 'NN'
	# do the nlp stuff
	# tokenized = nltk.word_tokenize(metadata)

	text = re.sub(r'http.+', '', metadata)
	text = re.sub(r'\w+:\w+', '', text)
	text = re.sub(r'\?\w+', '', text)

	# \w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*
	# print(text)
	tokenizer = RegexpTokenizer(r'\w+')
	# raw = normalizar.normalizar(text)
	# print(raw)
	tokenized = text.split(" ")

	aux = [normalize.normalizar(token) for token in tokenized]

	tokenized = tokenizer.tokenize(str(aux))

	# pos = [(word, pos) for (word, pos) in nltk.pos_tag(tokenized)]
	# print poss
	# print(aux)

	# nouns = [word for (word, pos) in nltk.pos_tag(tokenized) if len(word) > 2]
	# print(nouns)
	# print(tokenized)

	for noun in tokenized:
		noun = noun.lower()
		if noun not in coincidences.keys():
			coincidences[noun] = 0

		coincidences[noun] += 1


'''
Given the url of an Open Data Portal and its type (ckan or socrata),
all datasets' metadata is downloaded and returned to the main program
'''
def getPortalInfo(portal, typePortal):

	# Number of discarded datasets, for two reasons: not RDF information available or not DCAT format en its metadata
	discarded = {"noDCAT": 0, "noRDF": 0}

	# Map with the frequency of the words from all datasets, in order to discard those who appears several times
	coincidences = {}

	# Datasets metadata
	datasets = []

	print(u"Initializing metadata obtaining process", portal)

	# Preparing the variables in order to iterate the response
	identifier = "id"
	keyword = "tags"

	if typePortal == "ckan":  # or typePortal == "dkan":
		title = "title"
		description = "notes"
		language = "language"
		theme = ""
		resources = "resources"

	elif typePortal == "socrata":
		title = "name"
		description = "description"
		language = ""
		theme = "category"
		resources = ""
	else:
		print("Error, portal type not recognized - " + typePortal)
		sys.exit(0)

	print("Variables: ", title, identifier, description, language, keyword, theme)

	totalDatasets = 0
	page = 1
	finished = False

	'''
	This loop is made specially for socrata open data portals, which API has a maximum of 1000 results, aiming to
	have the metadata from all datasets. CKAN open data portal will work correctly as well
	'''
	while not finished:

		print("Downloading metadata. Page " + str(page))

		# Doing the request
		try:
			payload = {'page': page}
			response = requests.get(portal, params=payload)
			dataJson = json.loads(response.content)
			print("Metadata downloaded")
		except Exception as e:
			print(e)
			print("Error, portal \"" + portal + "\" does not work. ", sys.exc_info()[0])
			sys.exit(0)

		'''
		CKAN open data portals returns a list with the identifiers of all datasets, and it is needed to do a request
		for each of the datasets in order to obtain its metadata
		'''
		if typePortal == "ckan":  # or typePortal == "dkan":
			dataJson = getDatasetsInfoFromList(portal, dataJson)

		# Get info from json object array
		numDatasets = len(dataJson)
		totalDatasets += numDatasets
		print(numDatasets)

		index = 0

		# Once the metadata is downloaded, we iterate it to get the information we want to process
		for element in dataJson:
			print(index)
			dataset = Dataset()
	
			if title in element.keys() and element[title] is not None:
				dataset.title = element[title]
				print(element[title].encode("utf-8"))
	
			else:
				dataset.DCATformat = False
	
			if identifier in element.keys() and element[identifier] is not None:
				dataset.identifier = element[identifier]
	
			if description in element.keys() and element[description] is not None:
				dataset.description = element[description]
			else:
				dataset.DCATformat = False
	
			if keyword in element.keys() and element[keyword] is not None:
				for key in element[keyword]:
					if type(key) is str:
						dataset.keyword.append(key)
					elif type(key) is dict:
						dataset.keyword.append(key["name"])
	
			if language != "" and language in element.keys() and element[language] is not None:
				dataset.language = element[language]
	
			if theme != "" and theme in element.keys() and element[theme] is not None:
				dataset.theme = element[theme]
	
			if resources != "" and resources in element.keys():
				for resource in element[resources]:
					resourceFormat = resource["format"]
					if resourceFormat not in dataset.resourceFormats:
						dataset.resourceFormats.append(resourceFormat)
	
					if resourceFormat.lower() in rdfFormats:
						dataset.RDFResources.append(resource["url"])
	
			elif "dataUri" in element:
				urlData = element["dataUri"]
				for resourceFormat in rdfFormats:
					urlResource = urlData + "." + resourceFormat
					response = requests.get(urlResource)
					if response.status_code == 200:
						dataset.resourceFormats.append(resourceFormat)
						dataset.RDFResources.append(urlResource)

			# Tokenize all metadata, save only the nouns and store their appearance frequency
			metadata = dataset.title + " " + dataset.description + " " + str(dataset.keyword) + " " + dataset.theme
			getNumCoincidences(metadata, coincidences)

			# The datasets that do not have resources in RDF formats or do not follow the DCAT specification are discarded
			if len(dataset.RDFResources) > 0 and dataset.DCATformat is True:
				datasets.append(dataset)
			else:
				if len(dataset.RDFResources) == 0:
					discarded["noRDF"] += 1
	
				if dataset.DCATformat is False:
					discarded["noDCAT"] += 1
	
			index += 1

			# TODO Just for test, delete for production
			if index == 20:
				break

		if numDatasets < 1000:
			finished = True
		else:
			page += 1

	# The frequency of words is prorated considering the total number of datasets
	for key in coincidences:
		coincidences[key] = float(coincidences[key])/float(totalDatasets)

	return datasets, discarded, coincidences
