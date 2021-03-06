#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import json

from objects.Dataset import Dataset
from objects.Exceptions import PortalTypeError, PortalNotWorking
from scripts.getRDFProperties import processRDF
from scripts.tokenizer import tokenize

from scripts.filter import filterDataset

rdfFormats = ["rdf"]

'''
Given a list of datasets from an open data portal, it is obtained all the metadata from each dataset
'''
def getDatasetsInfoFromList(portal, datasets):

	data = []

	# Iterate over the list of datasets, and query on each of them
	for dataset in datasets["result"]:
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
def getNumCoincidences(title, metadata, coincidences):

	coincidences[title] = {}

	# Get tokens from all metadata
	tokenized = tokenize(metadata)

	for noun in tokenized:
		noun = noun.lower()
		if noun not in coincidences[title].keys():
			coincidences[title][noun] = 0

		coincidences[title][noun] += 1


'''
Given the frequency of appearance of all words, it calculates the total frequency around all datasets and the
number of dataset where each word appears
'''
def getTotalCoincidences(coincidences):

	coincidences["totalCoincidences"] = {}
	coincidences["datasetCoincidences"] = {}

	for dataset in coincidences.keys():
		if dataset != "totalCoincidences" and dataset != "datasetCoincidences":
			for word in coincidences[dataset].keys():
				if word not in coincidences["totalCoincidences"].keys():
					coincidences["totalCoincidences"][word] = 0

				if word not in coincidences["datasetCoincidences"].keys():
					coincidences["datasetCoincidences"][word] = 0

				coincidences["totalCoincidences"][word] += coincidences[dataset][word]
				coincidences["datasetCoincidences"][word] += 1


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

	if typePortal == "ckan":
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
		raise PortalTypeError("Error, portal (" + portal + ") type not recognized: " + typePortal)

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
			raise PortalNotWorking("Error, portal \"" + portal + "\" does not work. ")

		'''
		CKAN open data portals returns a list with the identifiers of all datasets, and it is needed to do a request
		for each of the datasets in order to obtain its metadata
		'''
		if typePortal == "ckan":
			print("Downloading resources")
			try:
				dataJson = getDatasetsInfoFromList(portal, dataJson)
			except Exception as e:
				print(e)
				raise PortalTypeError("Error, portal (" + portal + ") type not recognized: " + typePortal)

		# Get info from json object array
		numDatasets = len(dataJson)
		totalDatasets += numDatasets

		index = 0

		# Once the metadata is downloaded, we iterate it to get the information we want to process
		for element in dataJson:

			dataset = Dataset()

			filtered = True
	
			if title in element.keys() and element[title] is not None:
				dataset.title = element[title]
				print(element[title].encode("utf-8"))

				# Comment to iterate over all the datasets
				filtered = filterDataset(portal, dataset.title)
			else:
				dataset.DCATformat = False

			# Set filtered to True to omit filter test function
			# filtered = True

			if filtered:

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

				# After obtaining the metadata, it looks for rdf resources
				if resources != "" and resources in element.keys():
					for resource in element[resources]:
						resourceFormat = resource["format"]
						if resourceFormat not in dataset.resourceFormats:
							dataset.resourceFormats.append(resourceFormat)

						if resourceFormat.lower() in rdfFormats:
							dataset.RDFResources.append(resource["url"])
							RDFClasses, RDFProperties = processRDF(resource["url"])

							for RDFClass in RDFClasses:
								if RDFClass not in dataset.RDFschema["classes"]:
									dataset.RDFschema["classes"].append(RDFClass)

							for RDFProperty in RDFProperties:
								if RDFProperty not in dataset.RDFschema["properties"]:
									dataset.RDFschema["properties"].append(RDFProperty)

				else:
					urls = []

					if "dataUri" in element:
						urls.append(element["dataUri"])

					elif "childViews" in element:
						for child in element["childViews"]:
							urlData = portal
							if not urlData.endswith("/"):
								urlData += "/"

							urlData += child + "/rows"
							urls.append(urlData)
					else:
						urlData = portal
						if not urlData.endswith("/"):
							urlData += "/"

						if "id" in element.keys() and element["id"] is not None:
							urlData += element["id"] + "/rows"
							urls.append(urlData)

					for urlData in urls:

						for resourceFormat in rdfFormats:
							urlResource = urlData + "." + resourceFormat
							response = requests.get(urlResource)
							if response.status_code == 200:
								dataset.resourceFormats.append(resourceFormat)
								dataset.RDFResources.append(urlResource)
								RDFClasses, RDFProperties = processRDF(urlResource)
								dataset.RDFschema["classes"].append(RDFClasses)
								dataset.RDFschema["properties"].append(RDFProperties)

				# Tokenize all metadata, save only the nouns and store their appearance frequency
				metadata = dataset.title + " " + dataset.description + " " + str(dataset.keyword) + " " + dataset.theme
				getNumCoincidences(dataset.title, metadata, coincidences)

				# The datasets that do not have resources in RDF formats or do not follow the DCAT specification are discarded
				if len(dataset.RDFResources) > 0 and dataset.DCATformat is True:
					datasets.append(dataset)
				else:
					if len(dataset.RDFResources) == 0:
						discarded["noRDF"] += 1

					if dataset.DCATformat is False:
						discarded["noDCAT"] += 1

				index += 1

				# Uncomment for test
				# if index == 2:
				# finished = True
				# break

		if numDatasets < 1000:
			finished = True
		else:
			page += 1

	getTotalCoincidences(coincidences)

	return datasets, discarded, coincidences
