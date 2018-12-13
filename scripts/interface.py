#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, flash, request, Response, redirect, url_for, session, jsonify
from wtforms import Form, validators, StringField, SelectField

import json

from objects.Exceptions import PortalTypeError, PortalNotWorking
from scripts.init import initProcessing
from scripts.JSONtoXLS import JSONtoXLS

from io import BytesIO
from werkzeug.datastructures import Headers
import mimetypes

app = Flask(__name__)
app.config.from_object(__name__)

# TODO Unificar idioma plantillas y mensajes

# TODO: Cambiar y borrar
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

class ReusableForm(Form):
    portal1 = StringField('URL Portal 1:', validators=[validators.required()], default='http://opendata.caceres.es/api/action/package_list')
    type1 = SelectField('Portal Type 1', choices=[('ckan', 'ckan'), ('socrata', 'socrata')], default='ckan')

    portal2 = StringField('URL Portal 2:', validators=[validators.required()], default='https://data.cityofchicago.org/api/views/metadata/v1')
    type2 = SelectField('Portal Type 2', choices=[('ckan', 'ckan'), ('socrata', 'socrata')], default='socrata')

@app.errorhandler(404)
def page_not_found(arg):
    return render_template('error.html', error="La página solicitada no existe. Revisa que has introducido una url correcta"), 404

@app.route("/", methods=['GET', 'POST'])
def home():
    form = ReusableForm(request.form)

    print("Errors:", form.errors)

    if request.method == 'POST':
        portal1 = request.form['portal1']
        portal2 = request.form['portal2']
        typePortal1 = request.form['type1']
        typePortal2 = request.form['type2']
        print("Params:", portal1, portal2, typePortal1, typePortal2)

        if form.validate():
            params = json.dumps({"portal1": portal1, "portal2": portal2, "type1": typePortal1, "type2": typePortal2})
            return redirect(url_for('.results', params=params))

        else:
            flash('All the form fields are required.')

    return render_template("index.html", form=form)


@app.route("/results", methods=['GET'])
def results():
    if request.method == 'GET':
        params = request.args['params']
        params = json.loads(params)
        print(params)

        resultsJSON = {}

        try:
            resultsJSON, executionTime = initProcessing(params["portal1"], params["type1"], params["portal2"], params["type2"])
            response = render_template("results.html", time=executionTime)
        except PortalTypeError as e:
            response = render_template('error.html', error=str(e)), 400
        except PortalNotWorking as e:
            response = render_template('error.html', error=str(e)), 400

        session['resultsJSON'] = resultsJSON

        return response

@app.route("/download", methods=['GET'])
def download():

    response = None

    if "resultsJSON" in session:
        resultsJSON = session["resultsJSON"]

        fileFormat = request.args.get('format')

        if fileFormat == "json":
            response = jsonify(resultsJSON)
        else:
            resultsFile = JSONtoXLS(resultsJSON)

            # Create an in-memory output file for the workbook.
            output = BytesIO()
            resultsFile.save(output)

            # Rewind the buffer.
            output.seek(0)

            # Set filname and mimetype
            fileName = 'results.xls'
            mimetype_tuple = mimetypes.guess_type(fileName)

            h = Headers()
            h.add('Content-Disposition', 'attachment', filename=fileName)

            def generate():
                yield output.read()

            response = Response(generate(), headers=h, mimetype=mimetype_tuple[0])

    else:
        # TODO ¿Excepción?
        print()

    return response

@app.route('/api', methods=['GET'])
def api():

    if request.method == 'GET':
        portal1 = request.args.get('portal1')
        portal2 = request.args.get('portal2')

        if portal1 is not None and portal1 != "" and portal2 is not None and portal2 != "":

            typePortal1 = "ckan"
            typePortal2 = "ckan"

            if request.args.get('type1') is not None and request.args.get('portal1') != "":
                typePortal1 = request.args.get('type1')

            if request.args.get('type2') is not None and request.args.get('type2') != "":
                typePortal2 = request.args.get('type2')

            response = None
            resultsJSON = {}

            try:
                resultsJSON, executionTime = initProcessing(portal1, typePortal1, portal2, typePortal2)

                if request.args.get('format') is not None and request.args.get('format') != "":
                    resultsFormat = request.args.get('format')

                    if resultsFormat == "json":
                        response = jsonify(resultsJSON)

            except PortalTypeError as e:
                response = str(e), 400
            except PortalNotWorking as e:
                response = str(e), 400

            if response is None:
                resultsFile = JSONtoXLS(resultsJSON)

                # Create an in-memory output file for the workbook.
                output = BytesIO()
                resultsFile.save(output)

                # Rewind the buffer.
                output.seek(0)

                # Set filname and mimetype
                fileName = 'results.xls'
                mimetype_tuple = mimetypes.guess_type(fileName)

                h = Headers()
                h.add('Content-Disposition', 'attachment', filename=fileName)

                def generate():
                    yield output.read()

                response = Response(generate(), headers=h, mimetype=mimetype_tuple[0])

            return response

        else:
            return 'Welcome to the API service. Please, do a GET request on this same url, with the following parameters structure: ' \
                   '?portal1=url_portal_1&portal2=url_portal_2 {&type1=type_portal_1} {&type2=type_portal_2} {&format=(xls|json)}'
