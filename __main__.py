
import sys
import json

from getPortalsMetadata import getPortalInfo

def main():

    if len(sys.argv) < 3:
        print('Error, two portals are required. Optionally, the open data portal type can be included (ckan, socrata)')
        print('To execute the script: $python ', sys.argv[0], ' url_portal_1 url_portal_2 {ckan | socrata} {ckan | socrata}')
        sys.exit(0)

    print(u"Initializing program")

    # Getting arguments from command line

    portal1 = sys.argv[1]
    portal2 = sys.argv[2]

    if len(sys.argv) == 4:
        typePortal1 = sys.argv[3]
        typePortal2 = "ckan"
    elif len(sys.argv) > 4:
        typePortal1 = sys.argv[3]
        typePortal2 = sys.argv[4]
    else:
        typePortal1 = "ckan"
        typePortal2 = "ckan"

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

    # Volcar estadísticas en otro excel

    # processDatasets(datasets1, datasets2)


if __name__ == '__main__':
    main()
