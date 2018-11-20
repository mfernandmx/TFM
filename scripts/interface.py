#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, flash, request, abort, Response, redirect, url_for, make_response, send_file
from flask import jsonify
from wtforms import Form, validators, StringField, SelectField

from scripts.init import initProcessing

from io import BytesIO
from werkzeug.datastructures import Headers
import mimetypes

app = Flask(__name__)
app.config.from_object(__name__)

# TODO: Cambiar y borrar
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

class ReusableForm(Form):
    portal1 = StringField('URL Portal 1:', validators=[validators.required()], default='http://opendata.caceres.es/api/action/package_list')
    type1 = SelectField('Portal Type 1', choices=[('ckan', 'ckan'), ('socrata', 'socrata')], default='ckan')

    portal2 = StringField('URL Portal 2:', validators=[validators.required()], default='https://data.cityofchicago.org/api/views/metadata/v1')
    type2 = SelectField('Portal Type 2', choices=[('ckan', 'ckan'), ('socrata', 'socrata')], default='socrata')

# TODO Diferenciar entre API e interfaz
@app.errorhandler(404)
def page_not_found():
    return render_template('404.html'), 404

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
            flash('Portal 1: ' + portal1 + ' (' + typePortal1 + ')')
            flash('Portal 2: ' + portal2 + ' (' + typePortal2 + ')')

            # resultsFile = initProcessing(portal1, typePortal1, portal2, typePortal2)

            # TODO Return results

            # return redirect(url_for('.results', messages=resultsFile))
            # return redirect('/results', messages=resultsFile)

        else:
            flash('All the form fields are required. ')

    return render_template("index.html", form=form)

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

            resultsFile = initProcessing(portal1, typePortal1, portal2, typePortal2)

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

            return Response(generate(), headers=h, mimetype=mimetype_tuple[0])

        else:
            return 'Welcome to the API service. Please, do a GET request on this same url, with the following parameters structure: ' \
                   '?portal1=url_portal_1&portal2=url_portal_2{&type1=type_portal_1&type2=type_portal_2}'