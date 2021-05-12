Writing middlewares
=====================================
Middlewares are basically decorators that are run
in a queue fashion when a request hits an endpoint.
You can use as many middlewares to handle incoming requests
using the methods provided by the ``Route`` class.


.. toctree::
   :maxdepth: 2


A simple middleware:

.. code:: Python

    from functools import wraps
    from flask import has_request_context

    def mock_middleware(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            assert has_request_context()
            return fn(*args, **kwargs)
        return wrapper



A middleware that checks if the mimetype indecates JSON data:

.. code:: Python

    from functools import wraps
    from flask import request

    def is_json(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if not request.is_json:
                return { 'success': False }, 400
            return fn(*args, **kwargs)
        return wrapper


Using this signature, we can write middlewares that do all sorts
of handling, and use them all together with routing methods
provided by the ``Route`` class.


.. code:: Python

    from flask_mux import Router
    from flask_jwt_extended import jwt_required

    user_router = Router()

    user_router.post('/new', jwt_required, is_auth, is_json, view_func)


In this example, we are invoking 3 middlewares ``(jwt_required, is_auth, is_json)``
to filter out the incoming request before moving to the actual view function.

When a request hits an endpoint, the middlewares will be invoked in the same
order they were passed. 
