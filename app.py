from flask import Flask
from flask import render_template, redirect, request, flash, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
import pymysql
import secrets
import datetime
import os
from datetime import date, timedelta

'''
conn = "mysql+pymysql://{0}:{1}@{2}/{3}".format(secrets.dbuser, secrets.dbpass, secrets.dbhost, secrets.dbname)
app = Flask(__name__)
'''
dbuser = os.environ.get('DBUSER')
dbpass = os.environ.get('DBPASS')
dbhost = os.environ.get('DBHOST')
dbname = os.environ.get('DBNAME')
conn = "mysql+pymysql://{0}:{1}@{2}/{3}".format(dbuser, dbpass, dbhost, dbname)


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

class group7_patrons(db.Model):
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
        return "id: {0} | fName: {1} | lName: {2} | bdate: {3} | add1: {4} | add2: {5} | city: {6} | state: {7} | zip: {8}| | phone1: {9} | phone2: {10} | email: {10} | date added: {11} | date modified: {12}".format(self.patronId, self.firstName, self.lastName, self.birthdate, self.address1, self.address2, self.city, self.state, self.zip, self.phoneNumber1, self.phoneNumber2, self.email, self.dateAdded, self.lastModified)

class group7_circulation(db.Model):
    checkoutId = db.Column(db.Integer, primary_key=True)
    materialId = db.Column(db.Integer, db.ForeignKey('group7_materials.materialId')) # db.ForeignKey('group7_materials.materialId'))
    patronId = db.Column(db.Integer, db.ForeignKey('group7_patrons.patronId')) # db.ForeignKey('group7_patrons.patronId'))
    dayRented = db.Column(db.DateTime)
    dueDate = db.Column(db.DateTime)
    def __repr__(self):
        return "id: {0} | material id: {1} | patron id: {2} | day rented: {3} | due date: {4}".format(self.checkoutId, self.materialId, self.patronId, self.dayRented, self.dueDate)

class CheckoutForm(FlaskForm):
    checkoutId = IntegerField('Circulation ID: ')
    materialId = IntegerField('Material ID: ', validators=[DataRequired()])
    patronId = IntegerField('Patron ID: ', validators=[DataRequired()])
    dayRented = DateField('Date: ')
    dueDate = DateField('Due Date: ')


class MaterialForm(FlaskForm):
    materialId = IntegerField('Material ID: ')
    materialClass = StringField('Material Class: *', validators=[DataRequired()])
    callNumber = StringField('Call Number: *', validators=[DataRequired()])
    title = StringField('Title: *', validators=[DataRequired()])
    author = StringField('Author: ')
    publisher = StringField('Publisher: ')
    copyright = StringField('Copyright: ')
    ISBN = IntegerField('ISBN: ')
    dateAdded = DateField('Date Added: ')
    lastModified = DateField('Date Last Modified: ')

class PatronForm(FlaskForm):
    patronId = IntegerField('Patron ID: ')
    firstName = StringField('First Name: *', validators=[DataRequired()])
    lastName = StringField('Last Name: *', validators=[DataRequired()])
    birthdate = DateField('Birthdate (YYYY-MM-DD): *', )
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

@app.errorhandler(500)
def internal_server_error(error):
    app.logger.error('Server Error: %s', (error))
    return render_template('index.html'), 500


@app.route('/')
def index():
    return render_template('index.html', pageTitle='South Liberty Public Library', legend='Home')

@app.route('/about')
def about():
    return render_template('about.html', pageTitle='About')

@app.route('/materials')
def materials():
    all_materials = group7_materials.query.all()
    return render_template('materials.html', materials=all_materials, pageTitle='Materials', legend='Materials')

@app.route('/patrons')
def patrons():
    all_patrons = group7_patrons.query.all()
    return render_template('patrons.html', patrons= all_patrons, pageTitle = 'Patrons', legend='Patrons')


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
        results = group7_patrons.query.filter( or_(group7_patrons.lastName.like(search), group7_patrons.phoneNumber1.like(search), group7_patrons.phoneNumber2.like(search), group7_patrons.email.like(search))).all()
        return render_template('patrons.html', patrons=results, pageTitle='Patrons', legend='Search Results')
    else:
        return redirect('/')

@app.route('/searchcirculations', methods=['GET', 'POST'])
def search_circulation():
    if request.method =='POST':
        form = request.form
        search_value = form['search_circulation']
        search = "%{0}%".format(search_value)
        results = group7_circulation.query.filter( or_(group7_circulation.materialId.like(search), group7_circulation.patronId.like(search))).all()
        return render_template('circulations.html', circulations=results, pageTitle='Checked Out', legend='Search Results')
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
    if request.method == 'POST':
        patron = group7_patrons(firstName=form.firstName.data, lastName=form.lastName.data, birthdate=form.birthdate.data, address1=form.address1.data, address2=form.address2.data, city=form.city.data, state=form.state.data, zip=form.zip.data, phoneNumber1=form.phoneNumber1.data, phoneNumber2=form.phoneNumber2.data, email=form.email.data, dateAdded=datetime.datetime.now(),lastModified=datetime.datetime.now())
        db.session.add(patron)
        db.session.commit()
        return redirect('/patrons')

    return render_template('add_patron.html', form=form, pageTitle='Add A New Patron', legend="Add A New Patron")

@app.route('/material/<int:materialId>', methods=['GET','POST'])
def material(materialId):
    material = group7_materials.query.get_or_404(materialId)
    return render_template('material.html', form=material, pageTitle='Material Detail', legend='Material Detail')

@app.route('/patron/<int:patronId>', methods=['GET','POST'])
def patron(patronId):
    patron = group7_patrons.query.get_or_404(patronId)
    return render_template('patron.html', form=patron, pageTitle='Patron Details', legend='Patron Details')


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
    return render_template('update_material.html', form=form, pageTitle='Update Material',)

@app.route('/patron/<int:patronId>/update', methods=['GET','POST'])
def update_patron(patronId):
    patron = group7_patrons.query.get_or_404(patronId)
    form = PatronForm()
    if form.validate_on_submit():
    #if request.method == 'POST':
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
        return redirect('/materials')
    else: #if it's a GET request, send them to the home page
        return redirect('/materials')

@app.route('/patron/<int:patronId>/delete', methods=['POST'])
def delete_patron(patronId):
    if request.method == 'POST': #if it's a POST request, delete the material from the database
        patron = group7_patrons.query.get_or_404(patronId)
        db.session.delete(patron)
        db.session.commit()
        flash('Patron was successfully deleted!')
        return redirect('/patrons')
    else: #if it's a GET request, send them to the home page
        return redirect('/patrons')

@app.route('/circulations')
def circulations():
    all_circulations = group7_circulation.query.all()
    return render_template('circulations.html', circulations=all_circulations, pageTitle='Checked Out Materials',)

@app.route('/circulations/overdue')
def circulationsoverdue():
    overdue_circulations = group7_circulation.query.filter(group7_circulation.dueDate<date.today())
    return render_template('circulationsoverdue.html', circulations=overdue_circulations, pageTitle='Overdue Materials', legend='Overdue Materials')

@app.route('/circulations/duetoday')
def circulationsduetoday():
    duetoday_circulations = group7_circulation.query.filter(group7_circulation.dueDate==date.today())
    return render_template('circulationsduetoday.html', circulations=duetoday_circulations, pageTitle='Materials Due Today', legend='Materials Due Today')

@app.route('/circulations/check_out', methods=['GET', 'POST'])
def check_out():
    form = CheckoutForm()
    if form.validate_on_submit():
            checkouts = group7_circulation(checkoutId=form.checkoutId.data, materialId=form.materialId.data, patronId=form.patronId.data, dayRented=date.today(), dueDate=(date.today() + timedelta(14) ))
            db.session.add(checkouts)
            db.session.commit()
            return redirect('/circulations')

    return render_template('check_out.html', form=form, pageTitle='Check out A New Material', legend="Check out A New Material")



@app.route('/circulations/<int:checkoutId>/checkin', methods=['POST'])
def check_in(checkoutId):
    if request.method == 'POST':
        checkins = group7_circulation.query.get_or_404(checkoutId)
        db.session.delete(checkins)
        db.session.commit()
        return redirect("/circulations")
    else: #if it's a GET request, send them to the home page
        return redirect("/")

if __name__ == '__main__':
    app.run(debug=True)

app.config['DEBUG'] = True
