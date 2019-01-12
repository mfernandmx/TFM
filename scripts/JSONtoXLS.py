#!/usr/bin/python
# -*- coding: utf-8 -*-

import xlwt

'''
Given the results' JSON object, it converts it into a XLS file
'''
def JSONtoXLS(data):

	# Create xls file
	wb = xlwt.Workbook(encoding="utf-8")
	generalSheet = wb.add_sheet("General", cell_overwrite_ok=True)
	generalRow = 0

	# Iterate over the first portal's datasets
	for datasetId in data.keys():

		generalColumn = 0

		generalSheet.write(generalRow, generalColumn, generalRow)
		generalColumn += 1
		generalSheet.write(generalRow, generalColumn, data[datasetId]["title"])

		for RDFResource in data[datasetId]["rdfs"]:
			generalColumn += 1
			generalSheet.write(generalRow, generalColumn, RDFResource)

		sheet = wb.add_sheet(str(generalRow), cell_overwrite_ok=True)

		row = 0

		# Iterate over the second portal's datasets
		for dataset in data[datasetId]["results"]:

			column = 0

			# Write in xls file
			sheet.write(row, column, dataset["title"])
			column += 1
			sheet.write(row, column, dataset["value"])

			for RDFResource in dataset["rdfs"]:
				column += 1
				sheet.write(row, column, RDFResource)

			row += 1

		generalRow += 1

	return wb
