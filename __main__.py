
import sys

from scripts.interface import app
from scripts.init import initProcessing

def main():

    # Example parameters for command line
    # http://opendata.caceres.es/api/action/package_list https://data.cityofchicago.org/api/views/metadata/v1 ckan socrata

    # Example POST params for API
    # {"portal1": "http://opendata.caceres.es/api/action/package_list", "type1":"ckan", "portal2": "https://data.cityofchicago.org/api/views/metadata/v1", "type2": "socrata"}

    if len(sys.argv) < 3:
        print('Error, two portals are required. Optionally, the open data portal type can be included (ckan, socrata)')
        print('To execute the script: $python ', sys.argv[0], ' url_portal_1 url_portal_2 {ckan | socrata} {ckan | socrata}')
        print('Starting web interface')
        app.run(debug=True)

    else:
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

        resultsFile = initProcessing(portal1, typePortal1, portal2, typePortal2)

        # Store results in xls file
        resultsFile.save("results.xls")


if __name__ == '__main__':
    main()
