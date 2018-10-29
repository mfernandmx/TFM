
from scripts.getPortalsMetadata import getPortalInfo
from scripts.processMetadata import processDatasets

import json

def initProcessing(portal1, typePortal1, portal2, typePortal2):
    # Starting data obtaining

    datasets1, discarded1, coincidences1 = getPortalInfo(portal1, typePortal1)

    print("Coincidences 1", coincidences1)

    jsonObject = json.dumps(coincidences1)
    f = open("coincidences1.json", "w")
    f.write(jsonObject)
    f.close()

    datasets2, discarded2, coincidences2 = getPortalInfo(portal2, typePortal2)

    print("Coincidences 2", coincidences2)
    print("Coincidences 2", coincidences2)

    jsonObject = json.dumps(coincidences2)
    f = open("coincidences2.json", "w")
    f.write(jsonObject)
    f.close()

    print("Discarded 1", discarded1)
    print("Discarded 2", discarded2)

    # TODO: Statistics in new xls
    processDatasets(datasets1, datasets2)
