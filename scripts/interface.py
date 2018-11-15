#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, flash, request, abort, jsonify
from wtforms import Form, validators, StringField, SelectField

from scripts.init import initProcessing

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

    print(form.errors)

    if request.method == 'POST':
        portal1 = request.form['portal1']
        portal2 = request.form['portal2']
        typePortal1 = request.form['type1']
        typePortal2 = request.form['type2']
        print(portal1, portal2, typePortal1, typePortal2)

        if form.validate():
            flash('Portal 1: ' + portal1 + ' (' + typePortal1 + ')')
            flash('Portal 2: ' + portal2 + ' (' + typePortal2 + ')')

            # resultsFile = initProcessing(request.json["portal1"], typePortal1, request.json["portal2"], typePortal2)

            # TODO Return results
        else:
            flash('All the form fields are required. ')

    return render_template("index.html", form=form)

@app.route('/api', methods=['GET', 'POST'])
def hello():
    if request.method == 'POST':
        if not request.json or 'portal1' not in request.json or 'portal2' not in request.json:
            abort(400)

        typePortal1 = "ckan"
        typePortal2 = "ckan"

        if "type1" in request.json:
            typePortal1 = request.json["type1"]

        if "type2" in request.json:
            typePortal2 = request.json["type1"]

        # resultsFile = initProcessing(request.json["portal1"], typePortal1, request.json["portal2"], typePortal2)

        # TODO Return results
        return jsonify(request.json)

    elif request.method == 'GET':
        return 'Welcome to the API service. Please, do a POST request on this same url, with the following parameters structure: ' \
               '{"portal1": "url_portal_1", "type1":"type_portal_1", "portal2": "url_portal_2", "type2": "type_portal_2"}'
