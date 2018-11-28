
from scripts.getPortalsMetadata import getPortalInfo
from scripts.processMetadata import processDatasets

import json
import time

def initProcessing(portal1, typePortal1, portal2, typePortal2):

    start = time.time()

    # Starting data obtaining
    print(portal1, typePortal1, portal2, typePortal2)

    datasets1, discarded1, coincidences1 = getPortalInfo(portal1, typePortal1)

    # TODO Remove coincidences to file
    jsonObject = json.dumps(coincidences1)
    f = open("coincidences1.json", "w")
    f.write(jsonObject)
    f.close()

    datasets2, discarded2, coincidences2 = getPortalInfo(portal2, typePortal2)

    jsonObject = json.dumps(coincidences2)
    f = open("coincidences2.json", "w")
    f.write(jsonObject)
    f.close()

    print("Discarded 1", discarded1)
    print("Discarded 2", discarded2)

    # It takes as first argument the array with less number of datasets, in order to create less sheets on the results file

    if len(datasets1) <= len(datasets2):
        resultsJSON = processDatasets(datasets1, datasets2, coincidences1, coincidences2)
    else:
        resultsJSON = processDatasets(datasets2, datasets1, coincidences1, coincidences2)

    print("Execution finished")

    end = time.time()
    executionTime = end - start
    executionTime = time.strftime('%H:%M:%S', time.gmtime(executionTime))

    return resultsJSON, executionTime
