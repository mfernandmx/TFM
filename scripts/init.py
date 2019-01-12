#!/usr/bin/python
# -*- coding: utf-8 -*-

from objects.Exceptions import PortalTypeError, PortalNotWorking
from scripts.getPortalsMetadata import getPortalInfo
from scripts.processMetadata import processDatasets

import time

'''
Given two Open Data portals' API and their corresponding type, it calculates the grade of similarity between all the
datasets, returning a JSON object with the results
'''
def initProcessing(portal1, typePortal1, portal2, typePortal2):

    start = time.time()

    # Starting data obtaining
    print(portal1, typePortal1, portal2, typePortal2)

    try:
        datasets1, discarded1, coincidences1 = getPortalInfo(portal1, typePortal1)
    except PortalTypeError:
        raise
    except PortalNotWorking:
        raise

    try:
        datasets2, discarded2, coincidences2 = getPortalInfo(portal2, typePortal2)
    except PortalTypeError:
        raise
    except PortalNotWorking:
        raise

    # It takes as first argument the array with less number of datasets, in order to create less sheets on the results file

    if ((len(datasets1) <= len(datasets2)) and len(datasets1) != 0) or len(datasets2) == 0:
        resultsJSON = processDatasets(datasets1, datasets2, coincidences1, coincidences2)
        reverse = False
    else:
        resultsJSON = processDatasets(datasets2, datasets1, coincidences2, coincidences1)
        reverse = True

    end = time.time()
    executionTime = end - start
    executionTime = time.strftime('%H:%M:%S', time.gmtime(executionTime))

    return resultsJSON, executionTime, reverse
