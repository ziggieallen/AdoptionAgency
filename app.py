from flask import Flask, url_for, render_template, redirect, flash, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Pet
from forms import AddPetForm, EditPetForm, EditPetForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///adopt'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "chickenzarecool21837"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route('/')
def list_pets():
    """List all pets"""

    pets = Pet.query.all()
    return render_template("pet_list.html", pets=pets)

@app.route('/pets/new', methods=["GET", "POST"])
def add_pets():
    """Renders snack form (GET) or handles snack form submission (POST)"""
    form = AddPetForm()
    # makes a new form object based on the pet form class
    if form.validate_on_submit():
        name = form.name.data
        species = form.species.data
        photo_url = form.photo_url.data
        age = form.age.data
        notes = form.notes.data

        pet = Pet(name=name, species=species, photo_url=photo_url,age=age,notes=notes)
        db.session.add(pet)
        db.session.commit()
        # checks for authenticity of the CSRF token and if it is a POST request
        flash(f"Created new pet: name is {name}, species is {species}, age is {age}. Here are our notes: {notes}")
        return redirect('/')
    else:
        return render_template("add_pet_form.html", form=form) 

@app.route('/pets/<int:id>')
def pets_show(id):
    """Show a page with info on a specific pet"""

    pet = Pet.query.get_or_404(id)
    return render_template('pet_display.html', pet=pet)           

@app.route('/pets/<int:id>/edit', methods=["GET", "POST"])
def edit_pets(id):
    pet = Pet.query.get_or_404(id)
    form = EditPetForm(obj=pet)
    # obj=emp pre-populates the form with the existing data on the employee

    if form.validate_on_submit():
        photo_url = form.photo_url.data
        notes = form.notes.data
        available = form.available.data
        db.session.add(pet)
        db.session.commit()
        return redirect('/')
    else:
        return render_template("edit_pet_form.html", form=form,pet=pet)        