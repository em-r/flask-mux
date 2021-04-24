from flask_mux import Router

tc_default_router = Router()


@tc_default_router.route('/')
def handle_basic():
    return {'success': True}


@tc_default_router.route('/<int:id>/<string:name>')
def handle_with_params(id, name):
    return {'success': True, 'id': id, 'name': name}
