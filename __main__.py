
import sys

from objects.Exceptions import PortalTypeError, PortalNotWorking
from scripts.interface import app
from scripts.init import initProcessing
from scripts.JSONtoXLS import JSONtoXLS

import argparse
import json

# Downloads nltk packages needed
import nltk
nltk.download('wordnet')
nltk.download('wordnet_ic')
nltk.download('stopwords')

def main():

    # Example parameters for command line
    # https://www.data.act.gov.au/api/views/metadata/v1 https://data.cityofchicago.org/api/views/metadata/v1 socrata socrata --format xls

    # Example GET params for API
    # /api?portal1=https://www.data.act.gov.au/api/views/metadata/v1&portal2=https://data.cityofchicago.org/api/views/metadata/v1&type1=socrata&type2=socrata&format=xls

    if len(sys.argv) < 2:
        print('Two portals are required. Optionally, the open data portal type can be included (ckan, socrata)')
        print('To execute the script: $python ', sys.argv[0], ' url_portal_1 url_portal_2 {ckan | socrata} {ckan | socrata} {--format FORMAT}')
        print('Starting web interface')
        app.run(debug=True)

    else:
        print(u"Initializing program")

        # Getting arguments from command line
        parser = argparse.ArgumentParser()
        parser.add_argument('parameters', type=str, nargs='+', help='Portals APIs and their types')
        parser.add_argument('--format', help='Results format')
        args = parser.parse_args()
        print("Arguments:", args.parameters)
        print("Format:", args.format)

        portal1 = args.parameters[0]
        portal2 = args.parameters[1]

        if len(args.parameters) == 3:
            typePortal1 = args.parameters[2]
            typePortal2 = "ckan"
        elif len(args.parameters) > 3:
            typePortal1 = args.parameters[2]
            typePortal2 = args.parameters[3]
        else:
            typePortal1 = "ckan"
            typePortal2 = "ckan"

        try:
            resultsJSON, executionTime, reverse = initProcessing(portal1, typePortal1, portal2, typePortal2)
        except PortalTypeError as e:
            print(e)
            sys.exit(0)
        except PortalNotWorking as e:
            print(e)
            sys.exit(0)

        if args.format is not None and args.format == "json":
            jsonObject = json.dumps(resultsJSON)
            f = open("results.json", "w")
            f.write(jsonObject)
            f.close()

        elif args.format is None or args.format != "xls":
            print("Formato desconocido. Guardando resultados en XLS")

        resultsFile = JSONtoXLS(resultsJSON)

        # Store results in xls file
        resultsFile.save("results.xls")

        print("Execution finished")


if __name__ == '__main__':
    main()
