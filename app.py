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

class group7_patron(db.Model):
    patronId = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(255))
    lastName = db.Column(db.String(255))
    birthdate = db.Column(db.DateTime)
    address1 = db.Column(db.String(255))
    address2 = db.Column(db.String(255))
    city = db.Column(db.String(255))
    state = db.Column(db.String(2))
    zip = db.Column(db.Integer)
    phoneNumber1= db.Column(db.Integer)
    phoneNumber2= db.Column(db.Integer)
    email = db.Column(db.String(255))
    dateAdded = db.Column(db.DateTime)
    lastModified = db.Column(db.DateTime)
    def __repr__(self):
        return "id: {0} | first name: {1} | last name: {2} | birthdate: {3} | address1: {4} | address2: {5} | city: {6} | state: {7} | zip: {8} | phoneNumber1: {9} | phoneNumber2: {10} | email: {11} | dateAdded: {12} | lastModified: {13}".format(self.patronId, self.firstName, self.lastName, self.birthdate, self.address1, self.address2, self.city, self.state, self.zip, self.phoneNumber1, self.phoneNumber2, self.email, self.dateAdded, self.lastModified)

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

class PatronForm(FlaskForm):
    patronId = IntegerField('Patron ID: ')
    firstName = StringField('First Name:', validators=[DataRequired()])
    lastName = StringField('Last Name: ', validators=[DataRequired()])
    birthdate = DateField('Birthdate: ')
    address1 = StringField('Address1: ')
    address2 = StringField('Address2: ')
    city = StringField('City: ')
    state = StringField('State: ')
    zip = IntegerField('Zip: ')
    phoneNumber1 = IntegerField('Phone Number 1: ')
    phoneNumber2 = IntegerField('Phone Number 2: ')
    email = StringField('Email: ')
    dateAdded = DateField('Date Added: ')
    lastModified = DateField('Date Last Modified: ')


@app.route('/')
def index():
    all_materials = group7_materials.query.all()
    all_patrons = group7_patron.query.all()
    return render_template('index.html', materials=all_materials, patrons=all_patrons, pageTitle='South Liberty Public Library')

@app.route('/materials')
def materials():
    all_materials = group7_materials.query.all()
    return render_template('materials.html', materials=all_materials, pageTitle='Materials')

@app.route('/patrons')
def patrons():
    all_patrons = group7_patron.query.all()
    return render_template('patrons.html', patrons= all_patrons, pageTitle = 'Patrons')


@app.route('/searchmaterials', methods=['GET', 'POST'])
def search_materials():
    if request.method =='POST':
        form = request.form
        search_value = form['search_materials']
        search = "%{0}%".format(search_value)
        results = group7_materials.query.filter( or_(group7_materials.title.like(search), group7_materials.author.like(search))).all()
        return render_template('materials.html', materials=results, pageTitle='Materials', legend='Search Results')
    else:
        return redirect('/')

@app.route('/searchpatrons', methods=['GET', 'POST'])
def search_patrons():
    if request.method =='POST':
        form = request.form
        search_value = form['search_patrons']
        search = "%{0}%".format(search_value)
        results = group7_patron.query.filter( or_(group7_patron.lastName.like(search), group7_patron.phoneNumber1, group7_patron.phoneNumber2, group7_patron.email.like(search))).all()
        return render_template('patrons.html', patrons=results, pageTitle='Patrons', legend='Search Results')
    else:
        return redirect('/')

@app.route('/material/new', methods=['GET', 'POST'])
def add_material():
    form = MaterialForm()
    if form.validate_on_submit():
        material = group7_materials(materialClass=form.materialClass.data, callNumber=form.callNumber.data, title=form.title.data, author=form.author.data, publisher=form.publisher.data, copyright=form.copyright.data, ISBN=form.ISBN.data, dateAdded=datetime.datetime.now(),lastModified=datetime.datetime.now())
        db.session.add(material)
        db.session.commit()
        return redirect('/materials')

    return render_template('add_material.html', form=form, pageTitle='Add A New Material', legend="Add A New Material")

@app.route('/patron/new', methods=['GET', 'POST'])
def add_patron():
    form = PatronForm()
    if form.validate_on_submit():
        patron = group7_patron(firstName=form.firstName.data, lastName=lastName.data, birthdate=birthdate.data, address1=address1.data, address2=address2.data, city=city.data, state=state.data, zip=zip.data, phoneNumber1=phoneNumber1.data, phoneNumber2=phoneNumber2.data, email=email.data, dateAdded=datetime.datetime.now(),lastModified=datetime.datetime.now())
        db.session.add(patron)
        db.session.commit()
        return redirect('/patrons')

    return render_template('add_patron.html', form=form, pageTitle='Add A New Patron', legend="Add A New Patron")

@app.route('/material/<int:materialId>', methods=['GET','POST'])
def material(materialId):
    material = group7_materials.query.get_or_404(materialId)
    return render_template('material.html', form=material, pageTitle='Material Details')

@app.route('/patron/<int:patronId>', methods=['GET','POST'])
def patron(patronId):
    patron = group7_patron.query.get_or_404(patronId)
    return render_template('patron.html', form=patron, pageTitle='Patron Details')


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
        return redirect('/materials')

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

@app.route('/patron/<int:patronId>/update', methods=['GET','POST'])
def update_patron(patronId):
    patron = group7_patron.query.get_or_404(patronId)
    form = PatronForm()

    if form.validate_on_submit():
        patron.patronId = form.patronId.data
        patron.firstName = form.firstName.data
        patron.lastName = form.lastName.data
        patron.birthdate = form.birthdate.data
        patron.address1 = form.address1.data
        patron.address2 = form.address2.data
        patron.city = form.city.data
        patron.state = form.state.data
        patron.zip = form.zip.data
        patron.phoneNumber1 = form.phoneNumber1.data
        patron.phoneNumber2 = form.phoneNumber2.data
        patron.email = form.email.data
        patron.dateAdded = form.dateAdded.data
        patron.lastModified = datetime.datetime.now()
        db.session.commit()
        return redirect('/patrons')

    form.patronId.data = patron.patronId
    form.firstName.data = patron.firstName
    form.lastName.data = patron.lastName
    form.birthdate.data = patron.birthdate
    form.address1.data = patron.address1
    form.address2.data = patron.address2
    form.city.data = patron.city
    form.state.data = patron.state
    form.zip.data = patron.zip
    form.phoneNumber1.data = patron.phoneNumber1
    form.phoneNumber2.data = patron.phoneNumber2
    form.email.data = patron.email
    form.dateAdded.data = patron.dateAdded
    form.lastModified.data = patron.lastModified
    return render_template('update_patron.html', form=form, pageTitle='Update Patron',legend="Update A Patron")


@app.route('/material/<int:materialId>/delete', methods=['POST'])
def delete_material(materialId):
    if request.method == 'POST': #if it's a POST request, delete the material from the database
        material = group7_materials.query.get_or_404(materialId)
        db.session.delete(material)
        db.session.commit()
        flash('Material was successfully deleted!')
        return redirect("/materials")
    else: #if it's a GET request, send them to the home page
        return redirect("/")

@app.route('/patron/<int:patronId>/delete', methods=['POST'])
def delete_patron(patronId):
    if request.method == 'POST': #if it's a POST request, delete the material from the database
        patron = group7_patron.query.get_or_404(patronId)
        db.session.delete(patron)
        db.session.commit()
        flash('Material was successfully deleted!')
        return redirect("/patrons")
    else: #if it's a GET request, send them to the home page
        return redirect("/")


if __name__ == '__main__':
    app.run(debug=True)

app.config['DEBUG'] = True
