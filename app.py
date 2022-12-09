"""Flask app for Cupcakes"""
from flask import Flask, render_template, jsonify, request, redirect, url_for
from models import db, connect_db, Cupcake
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'SECRET'
app.debug = True

toolbar = DebugToolbarExtension(app)

connect_db(app)


def serialize(cupcake):

    return {'id': cupcake.id,
            'flavor': cupcake.flavor,
            'size': cupcake.size,
            'rating': cupcake.rating,
            'image': cupcake.image}


@app.route('/')
def base():

    return render_template("index.html")


@app.route('/add-New', methods=["POST", "GET"])
def display_add_cupcake_form():
    """Display add cupcake form"""
    if request.method == 'POST':
        flavor = request.form['flavor']
        size = request.form['size']
        rating = request.form['rating']
        image = request.form['image'] or None

        new_cupcake = Cupcake(flavor=flavor, size=size,
                              rating=rating, image=image)
        db.session.add(new_cupcake)
        db.session.commit()
        return redirect('/')

    return render_template("cupcake_form.html")


@app.route('/api/cupcakes')
def get_all_cupcakes():
    """Get all Cupcakes."""

    cupcakes = Cupcake.query.all()
    serialized = [serialize(x) for x in cupcakes]

    return jsonify(serialized)


@app.route('/api/cupcakes/<int:cupcake_id>')
def get_cupcake_by_id(cupcake_id):
    """Get cupcake by ID."""

    cupcake = Cupcake.query.get(cupcake_id)
    serialized = serialize(cupcake)

    return jsonify(serialized)


@app.route('/api/cupcakes/', methods=['POST'])
def create_new_cupcake():
    """Create a new cupcake."""

    new_cupcake = Cupcake(flavor=request.json["flavor"],
                          size=request.json["size"],
                          rating=request.json["rating"])

    db.session.add(new_cupcake)
    db.session.commit()

    return (jsonify(cupcake=serialize(new_cupcake)), 201)


@app.route('/api/cupcakes/<cupcake_id>', methods=['PATCH'])
def update_cupcake(cupcake_id):
    """Update a cupcake."""

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    cupcake.flavor = request.json.get('flavor', cupcake.flavor)
    cupcake.size = request.json.get('size', cupcake.size)
    cupcake.rating = request.json.get('rating', cupcake.rating)
    cupcake.image = request.json.get('image', cupcake.image)
    db.session.commit()

    return jsonify(cupcake=serialize(cupcake))


@app.route('/api/cupcakes/<cupcake_id>', methods=["DELETE"])
def delete_cupcake(cupcake_id):

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message="deleted")
