
# Class to store all relevant information about a dataset

class Dataset:
	title = ""
	identifier = ""

	description = ""
	keyword = []
	language = ""
	theme = ""
	RDFResources = []
	RDFschema = {"classes": [], "properties": []}
	DCATformat = True
	resourceFormats = []

	def __init__(self):
		self.keyword = []
		self.resourceFormats = []
		self.RDFResources = []
