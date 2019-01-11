#!/usr/bin/python
# -*- coding: utf-8 -*-

def filterDataset(portal, dataset):

	filtered = True
	portals = {
		"https://www.data.act.gov.au/api/views/metadata/v1": [
			"ACT School Locations 2017 - archived",
			"Schools in the ACT - archived",
			"ACT Police Station Locations",
			"Library Locations",
			"University of Canberra WiFi Usage",
			"Hospitals in the ACT",
			"ACT Crime Statistics",
			"ABS - Census",
			"ABS Census - Percentage of people aged 15 years and older participating in active transport for work, 2016"
		],
		"https://data.cityofchicago.org/api/views/metadata/v1": [
			"Parks - Public Art",
			"Police Stations",
			"Libraries - Popular Kids Titles at the Chicago Public Library",
			"Libraries - WiFi Usage (2011-2014)",
			"Crimes - 2001 to present",
			"Crimes - Map",
			"Crimes - 2015",
			"Performance Metrics - Chicago Park District - Natural Resources Trees and Shrubs",
			"Boundaries - Census Tracts - 2000"
		],
		"https://data.cityofnewyork.us/api/views": [
			"Colleges and Universities",
			"Parks Zones",
			"Open Space (Parks)",
			"NYCHA PSA (Police Service Areas)",
			"Queens Library Branches",
			"Queens Libraries (Map)",
			"Health and Hospitals Corporation (HHC) Facilities",
			"NYC Park Crime Data",
			"1995 Street Tree Census",
			"2005 Street Tree Census",
			"2015 Street Tree Census - Tree Data",
			"2010 Census Blocks",
			"2010 Census Tracts"
		],
		"https://data.sfgov.org/api/views": [
			"Schools",
			"Map of Schools",
			"College Locations and Boundaries in San Francisco (2011)",
			"Park Lands - Recreation and Parks Department",
			"Recreation and Parks Facilities",
			"Police Stations (2011)",
			"Police Department Incident Reports: Historical 2003 to May 2018",
			"Street Tree List",
			"Street Tree Map",
			"US Census Bureau Data"
		],
		"https://data.code4sa.org/api/views/metadata/v1": [
			"Closed and pending schools",
			"South African Hospitals Survey 2011-2012",
			"Police Statistics | 2005 - 2018",
			"Age in Completed Years (Census 2011)",
			"Census 2011 - Boundaries - Small Area Layer"
			# "Police Station Coordinates",
			# "Police Station Boundaries"

		],
		"https://data.cambridgema.gov/api/views": [
			"Cambridge Public School Locations",
			"Waterplay Park Locations",
			"Police Station",
			"Cambridge Public Library Locations",
			"Crime Reports",
			"Crime Reports by Type",
			"Street Trees",
			"2010 Census Data by Neighborhood",
			"1980 - 2010 Census Data by Neighborhood"
		]
	}

	if portal in portals.keys():
		if dataset not in portals[portal]:
			filtered = False

	return filtered
