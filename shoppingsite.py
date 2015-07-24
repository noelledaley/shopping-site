"""Ubermelon shopping application Flask server.

Provides web interface for browsing melons, seeing detail about a melon, and
put melons in a shopping cart.

Authors: Joel Burton, Christian Fernandez, Meggie Mahnken.
"""


from flask import Flask, render_template, redirect, flash, session, jsonify
import jinja2

import model



app = Flask(__name__)

# Need to use Flask sessioning features

app.secret_key = 'something-unguessable'

# Normally, if you refer to an undefined variable in a Jinja template,
# Jinja silently ignores this. This makes debugging difficult, so we'll
# set an attribute of the Jinja environment that says to make this an
# error.

app.jinja_env.undefined = jinja2.StrictUndefined


@app.route("/")
def index():
    """Return homepage."""

    return render_template("homepage.html")


@app.route("/melons")
def list_melons():
    """Return page showing all the melons ubermelon has to offer"""

    # melons = list of melon objects
    melons = model.Melon.get_all()

    return render_template("all_melons.html", melon_list=melons)


@app.route("/melon/<int:id>")
# How does it receive this argument...?
def show_melon(id):
    """Return page showing the details of a given melon.

    Show all info about a melon. Also, provide a button to buy that melon.
    """

    # passing in id, returns an instance of Melon
    melon = model.Melon.get_by_id(id)

    return render_template("melon_details.html", display_melon=melon)


@app.route("/add_to_cart/<int:id>")
def add_to_cart(id):
    """Add a melon to cart and redirect to shopping cart page.

    When a melon is added to the cart, redirect browser to the shopping cart
    page and display a confirmation message: 'Successfully added to cart'.
    """

    # TODO: Finish shopping cart functionality
    #   - use session variables to hold cart list

    melon = model.Melon.get_by_id(id)

    # check if the key 'cart' is already in session.
    # if it's not, create a new key where the value is an empty list.
    # then, append the melon ID to that list.
    session.setdefault('cart', []).append(id)

    flash("You added a melon to your cart! Woo!")

    return redirect("/cart")


@app.route("/cart")
def shopping_cart():
    """Display content of shopping cart."""

    order_total = 0

    session_cart = session.get('cart', [])

    cart = {}

    for melon_id in session_cart:

        # looks in cart for a key called melon_id
        # if key doesn't already exist, add it with a value of an empty dictionary
        # result will be nested dict
            # ex:
            # {melon_id: {'qty': 1, 'common_name': 2...}}
        melon = cart.setdefault(melon_id, {})

        # if value of melon key isnt' blank
        if melon:
            melon['qty'] += 1

        # if value of melon key is empty
        else:
            # create an instance of the melon
            melon_attr = model.Melon.get_by_id(melon_id)

            # add new key to melon dict, set value to the melon's common name
            # {14: {'common_name': 'watermelon'}}
            melon['common_name'] = melon_attr.common_name
            melon['cost'] = melon_attr.price
            melon['qty'] = 1

        # add new key called total_cost
        # {12: {'qty': 4, 'common_name': 'crenshaw', 'cost': 10, 'total_cost': 40}}
        # order total += 40
        melon['total_cost'] = melon['cost'] * melon['qty']
        order_total += melon['total_cost']

    # cart will return list of little dictionaries
    # ex:
        # [{'qty': 4, 'common_name': 'crenshaw', 'cost': 10, 'total_cost': 40}]
    cart = cart.values()

    return render_template("cart.html", cart=cart, order_total=order_total)


@app.route("/login", methods=["GET"])
def show_login():
    """Show login form."""

    return render_template("login.html")


@app.route("/login", methods=["POST"])
def process_login():
    """Log user into site.

    Find the user's login credentials located in the 'request.form'
    dictionary, look up the user, and store them in the session.
    """

    # TODO: Need to implement this!

    return "Oops! This needs to be implemented"


@app.route("/checkout")
def checkout():
    """Checkout customer, process payment, and ship melons."""

    # For now, we'll just provide a warning. Completing this is beyond the
    # scope of this exercise.

    flash("Sorry! Checkout will be implemented in a future version.")
    return redirect("/melons")


if __name__ == "__main__":
    app.run(debug=True)
