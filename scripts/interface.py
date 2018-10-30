#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, flash, request
from wtforms import Form, validators, StringField, SelectField

app = Flask(__name__)
app.config.from_object(__name__)

# TODO: Cambiar y borrar
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

class ReusableForm(Form):
    portal1 = StringField('URL Portal 1:', validators=[validators.required()], default='http://opendata.caceres.es/api/action/package_list')
    type1 = SelectField('Portal Type 1', choices=[('ckan', 'ckan'), ('socrata', 'socrata')], default='ckan')

    portal2 = StringField('URL Portal 2:', validators=[validators.required()], default='https://data.cityofchicago.org/api/views/metadata/v1')
    type2 = SelectField('Portal Type 2', choices=[('ckan', 'ckan'), ('socrata', 'socrata')], default='socrata')

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
        type1 = request.form['type1']
        type2 = request.form['type2']
        print(portal1, portal2, type1, type2)

        if form.validate():
            # Save the comment here.
            flash('Portal 1: ' + portal1 + ' (' + type1 + ')')
            flash('Portal 2: ' + portal2 + ' (' + type2 + ')')

        else:
            flash('All the form fields are required. ')

    return render_template("index.html", form=form)
