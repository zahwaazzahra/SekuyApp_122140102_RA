from pyramid.view import view_config
from pyramid.response import Response
from pyramid.httpexceptions import HTTPBadRequest, HTTPConflict, HTTPUnauthorized
from pyramid.security import remember, forget
from ..models.user import User

def require_fields(data, required_fields):
    missing = [f for f in required_fields if not data.get(f)]
    if missing:
        raise HTTPBadRequest(json_body={'error': f'Missing fields: {", ".join(missing)}'})

@view_config(route_name='register', request_method='POST', renderer='json')
def register(request):
    data = request.json_body

    try:
        require_fields(data, ['username', 'email', 'password'])
    except HTTPBadRequest as e:
        return e

    username = data['username']
    email = data['email']
    password = data['password']

    if request.dbsession.query(User).filter_by(email=email).first():
        return HTTPConflict(json_body={'error': 'Email already exists'})

    new_user = User(
        username=username,
        email=email
    )
    new_user.password = password
    request.dbsession.add(new_user)
    request.dbsession.flush()

    return {
        'message': 'Registration successful',
        'user': new_user.to_dict()
    }

@view_config(route_name='login', request_method='POST', renderer='json')
def login(request):
    data = request.json_body

    try:
        require_fields(data, ['email', 'password'])
    except HTTPBadRequest as e:
        return e

    email = data['email']
    password = data['password']
    user = request.dbsession.query(User).filter_by(email=email).first()

    if not user or not user.check_password(password):
        return HTTPUnauthorized(json_body={'error': 'Invalid credentials'})

    headers = remember(request, str(user.id))

    return Response(
        json_body={
            'message': 'Login successful',
            'user': user.to_dict()
        },
        headers=headers,
        content_type='application/json'
    )

@view_config(route_name='logout', request_method='POST', renderer='json')
def logout(request):
    headers = forget(request)

    return Response(
        json_body={'message': 'Logout successful'},
        headers=headers,
        content_type='application/json'
    )
