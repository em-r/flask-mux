Flask-Mux example
=====================================
In this example, we are going to re-write the app we are using
in :doc:`flask-only` using **Flask-Mux**


We will create the Flask instance and instantiate the extensions
in ``app.py`` module:

.. code:: Python

    from flask import Flask
    from flask_jwt_extended import JWTManager
    from flask_mux import Mux
    from routes import index_router, auth_router, home_router

    app = Flask(__name__)
    jwt = JWTManager(app)
    mux = Mux(app)

    mux.use('/', index_router)
    mux.use('/auth', auth_router)
    mux.use('/api', api_router)

We also imported the routers for different namespaces that we are 
going to create now.

In the current directory, create a new Python package and call it routes:

.. code:: Bash

    $ mkdir routes
    $ touch routes/__init__.py


For each router, we'll create a seperate module in the routes package.

``routes/index.py``:

.. code:: Python

    from flask_mux import Router

    index_router = Router()

    def home():
        return 'home page'
    
    index_router.get('/' home)


``routes/auth.py``:

.. code:: Python

    from flask_mux import Router
    from flask_jwt_extended import create_access_token, jwt_required

    auth_router = Router()

    def login():
        identity = {'user_id': 1234}
        return { 'access_token': create_access_token(identity) }

    def logout():
        return { 'message': 'logged out' }

    auth_router.post('/login', login)
    auth_router.get('/logout', jwt_required, logout)

The ``Router`` class provides a set of methods (post, get...) to handle each request.
All those methods follow the same pattern, the 1st parameter is the endpoint
to be handled and the 2nd paramater is a variadic paramater of middlewares.
Notice how we passed 2 functions in the last line, you can pass an unlimited amount
of functions as long as they are middlewares.


``routes/api.py``:

.. code:: Python

    from flask_mux import Router
    from flask_jwt_extended import jwt_required

    api_router = Router()

    def profile(id):
        return { 'user_id': id }

    api_router.get('/user/<int:id>', jwt_required, profile)

The ``Router`` class provides a set of methods (post, get...) to handle each request.
All those methods have the same signature, the 1st parameter is the endpoint
to be handled and the 2nd paramater is a variadic paramater of middlewares.
Notice how we passed 2 functions in the last line, you can pass an unlimited amount
of functions as long as they are middlewares.