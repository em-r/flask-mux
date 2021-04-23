from flask_mux import Router

tc_1_router = Router()


@tc_1_router.get('/')
def route_1():
    return {'success': True}


@tc_1_router.get('/<int:id>')
def route_2(id):
    return {'success': True, 'id': id}
