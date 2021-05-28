from flask_mux import Router


def handler():
    return {'success': True}


auth_router = Router(__name__)
auth_router.post('/login', handler)
auth_router.post('/join', handler)
auth_router.get('/logout', handler)


api_router = Router(__name__)
api_router.get('/users', handler)
api_router.post('/articles', handler)
api_router.put('/articles', handler)


admin_router = Router(__name__)
admin_router.post('/login', handler)
admin_router.get('/logout', handler)
