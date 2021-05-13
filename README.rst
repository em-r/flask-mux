Flask-Mux
================

**Flask-Mux** is a lightweight Flask_ extension that provides a routing 
system similar to that of Express.js_. It basically wraps Flask's 
url route registrations API to add more flexibility.

.. _Flask: https://palletsprojects.com/p/flask/
.. _Express.js: https://www.expressjs.com


Installing
----------
Install using `pip`_:

.. code-block:: text

  $ pip install Flask-Mux

.. _pip: https://pip.pypa.io/en/stable/quickstart/


A Simple Example
----------------

.. code-block:: python

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


User's Guide
------------
You'll find the user guide and all documentation here_

.. _here: https://flask-mux.readthedocs.com/

Links
-----

-   Documentation: https://flask-mux.readthedocs.com/
-   PyPI Releases: https://pypi.org/project/Flask-Mux/
-   Source Code: https://github.com/ElMehdi19/flask-mux/
-   Issue Tracker: https://github.com/ElMehdi19/flask-mux/issues/