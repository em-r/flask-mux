Quickstart
=====================================
In this example, we are going to create a Router instance
which will store routes registered within a single namespace,
``/`` in our case.


.. toctree::
   :maxdepth: 2



Express-like approach
-----------------------------

.. code:: Python

    from flask import Flask
    from flask_mux import Mux, Router

    app = Flask(__name__)
    mux = Mux(app)

    def home():
        return 'home'

    def about():
        return 'about'

    index_router = Router()
    index_router.get('/', home)
    index_router.get('/about', about)

    mux.use('/', index_router)



Using the route decorator
-----------------------------

.. code:: Python

    from flask import Flask
    from flask_mux import Mux, Router

    app = Flask(__name__)
    mux = Mux(app)

    index_router = Router()

    @index_router.route('/')
    def home():
        return 'home'

    @index_router.route('/about')
    def about():
        return 'about'

    mux.use('/', index_router)