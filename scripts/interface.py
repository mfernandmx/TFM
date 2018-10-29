#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, flash, request
from wtforms import Form, validators, StringField

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

class ReusableForm(Form):
    name = StringField('Name:', validators=[validators.required()])

@app.errorhandler(404)
def page_not_found():
    return render_template('404.html'), 404

@app.route("/", methods=['GET', 'POST'])
def home():
    form = ReusableForm(request.form)

    print(form.errors)

    if request.method == 'POST':
        name = request.form['name']
        print(name)

        if form.validate():
            # Save the comment here.
            flash('Hello ' + name)
        else:
            flash('All the form fields are required. ')

    return render_template("index.html", form=form)