from flask import Flask
from flask import render_template, redirect, request, flash, url_for
#for windows
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
import pymysql
import secrets
import datetime


conn = "mysql+pymysql://{0}:{1}@{2}/{3}".format(secrets.dbuser, secrets.dbpass, secrets.dbhost, secrets.dbname)
app = Flask(__name__)

app = Flask(__name__)
app.config['SECRET_KEY']='SuperSecretKey'
app.config['SQLALCHEMY_DATABASE_URI'] = conn
db = SQLAlchemy(app)

class group7_materials(db.Model):
    #__tablename__ = 'results'
    materialId = db.Column(db.Integer, primary_key=True)
    materialClass = db.Column(db.String(25))
    callNumber = db.Column(db.String(255))
    title = db.Column(db.String(255))
    author = db.Column(db.String(255))
    publisher = db.Column(db.String(255))
    copyright = db.Column(db.Integer)
    ISBN = db.Column(db.Integer)
    dateAdded = db.Column(db.DateTime)
    lastModified = db.Column(db.DateTime)

    def __repr__(self):
        return "id: {0} | material class: {1} | call number: {2} | title: {3} | author: {4} | publisher: {5} | copyright: {6} | ISBN: {7} | date added: {8} | date modified: {9}".format(self.materialId, self.materialClass, self.callNumber, self.title, self.author, self.publisher, self.copyright, self.ISBN, self.dateAdded, self.lastModified)

class MaterialForm(FlaskForm):
    materialId = IntegerField('Material ID: ')
    materialClass = StringField('Material Class:', validators=[DataRequired()])
    callNumber = StringField('Call Number:', validators=[DataRequired()])
    title = StringField('Title:', validators=[DataRequired()])
    author = StringField('Author:')
    publisher = StringField('Publisher:', validators=[DataRequired()])
    copyright = StringField('Copyright:')
    ISBN = IntegerField('ISBN:', validators=[DataRequired()])
    dateAdded = DateField('Date Added: ')
    lastModified = DateField('Date Last Modified: ')


@app.route('/')
def index():
    all_materials = group7_materials.query.all()
    return render_template('index.html', materials=all_materials, pageTitle='SLPL Materials')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method =='POST':
        form = request.form
        search_value = form['search_string']
        search = "%{0}%".format(search_value)
        results = group7_materials.query.filter( or_(group7_materials.title.like(search), group7_materials.author.like(search))).all()
        return render_template('index.html', materials=results, pageTitle='Materials', legend='Search Results')
    else:
        return redirect('/')

@app.route('/material/new', methods=['GET', 'POST'])
def add_material():
    form = MaterialForm()
    if form.validate_on_submit():
        material = group7_materials(materialClass=form.materialClass.data, callNumber=form.callNumber.data, title=form.title.data, author=form.author.data, publisher=form.publisher.data, copyright=form.copyright.data, ISBN=form.ISBN.data, dateAdded=datetime.datetime.now(),lastModified=datetime.datetime.now())
        db.session.add(material)
        db.session.commit()
        return redirect('/')

    return render_template('add_material.html', form=form, pageTitle='Add A New Material', legend="Add A New Material")


@app.route('/material/<int:materialId>', methods=['GET','POST'])
def material(materialId):
    material = group7_materials.query.get_or_404(materialId)
    return render_template('material.html', form=material, pageTitle='Material Details')

@app.route('/material/<int:materialId>/update', methods=['GET','POST'])
def update_material(materialId):
    material = group7_materials.query.get_or_404(materialId)
    form = MaterialForm()

    if form.validate_on_submit():
        material.materialId = form.materialId.data
        material.materialClass = form.materialClass.data
        material.callNumber = form.callNumber.data
        material.title = form.title.data
        material.author = form.author.data
        material.publisher = form.publisher.data
        material.copyright = form.copyright.data
        material.ISBN = form.ISBN.data
        material.dateAdded = form.dateAdded.data
        material.lastModified = datetime.datetime.now()
        db.session.commit()
        return redirect('/')

    form.materialId.data = material.materialId
    form.materialClass.data = material.materialClass
    form.callNumber.data = material.callNumber
    form.title.data = material.title
    form.author.data = material.author
    form.publisher.data = material.publisher
    form.copyright.data = material.copyright
    form.ISBN.data = material.ISBN
    form.dateAdded.data = material.dateAdded
    form.lastModified.data = material.lastModified
    return render_template('update_material.html', form=form, pageTitle='Update Material',legend="Update A Material")

@app.route('/material/<int:materialId>/delete', methods=['POST'])
def delete_material(materialId):
    if request.method == 'POST': #if it's a POST request, delete the material from the database
        material = group7_materials.query.get_or_404(materialId)
        db.session.delete(material)
        db.session.commit()
        flash('Material was successfully deleted!')
        return redirect("/")
    else: #if it's a GET request, send them to the home page
        return redirect("/")


if __name__ == '__main__':
    app.run(debug=True)

app.config['DEBUG'] = True
