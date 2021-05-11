Pure Flask example
=====================================
In this example, we are exposing 4 endpoints in the server.
An index endpoint, 2 authentication endpoints, and a user profile endpoint.
We are also using the ``jwt_required`` decorator provided by
the `Flask-JWT-Extended` extension to simulate the authentication process.
This is a very classic example of REST APIs implemented with Flask.
Checkout :doc:`flask-mux` to learn how to integrate ``Flask-Mux``
with this app to make it more modular.


.. toctree::
   :maxdepth: 2
   :caption: Contents:


.. code:: Python


    from flask import Flask
    from flask_jwt_extended import (
        JWTManager, 
        create_access_token, 
        jwt_required
    )

    app = Flask(__name__)
    jwt = JWTManager(app)

    @app.route('/')
    def home():
        return 'home page'

    @app.route('/auth/login', methods=['POST'])
    def login():
        identity = {'user_id': 1234}
        return { 'access_token': create_access_token(identity) }

    @app.route('/auth/logout', methods=['POST'])
    @jwt_required
    def logout():
        return { 'message': 'logged out' }

    @app.route('/api/user/<int:id>')
    @jwt_required
    def profile(id):
        return { 'user': id }