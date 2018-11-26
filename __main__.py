
import sys

from scripts.interface import app
from scripts.init import initProcessing

def main():

    # Example parameters for command line
    # http://opendata.caceres.es/api/action/package_list https://data.cityofchicago.org/api/views/metadata/v1 ckan socrata

    # Example GET params for API
    # /api?portal1=http%3A%2F%2Fopendata.caceres.es%2Fapi%2Faction%2Fpackage_list&portal2=https%3A%2F%2Fdata.cityofchicago.org%2Fapi%2Fviews%2Fmetadata%2Fv1&type1=ckan&type2=socrata

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

        resultsFile, executionTime = initProcessing(portal1, typePortal1, portal2, typePortal2)

        # Store results in xls file
        resultsFile.save("results.xls")


if __name__ == '__main__':
    main()
