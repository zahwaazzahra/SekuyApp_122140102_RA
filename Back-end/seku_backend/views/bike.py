from pyramid.view import view_config
from pyramid.response import Response
from pyramid.httpexceptions import HTTPNotFound, HTTPBadRequest, HTTPUnauthorized
from ..models.bike import Bike

def get_user_id(request):
    user_id = request.authenticated_userid
    if not user_id:
        raise HTTPUnauthorized(json_body={'error': 'Unauthorized'})
    return user_id

def get_bike_or_404(request, bike_id):
    try:
        bike_id = int(bike_id)
    except ValueError:
        raise HTTPBadRequest(json_body={'error': 'Invalid bike ID format'})

    bike = request.dbsession.get(Bike, bike_id)
    if not bike:
        raise HTTPNotFound(json_body={'error': 'Bike not found'})
    return bike

@view_config(route_name='bikes', request_method='GET', renderer='json')
def list_bikes(request):
    bikes = request.dbsession.query(Bike).all()
    return [b.to_dict() for b in bikes]

@view_config(route_name='bike_detail', request_method='GET', renderer='json')
def get_bike(request):
    bike = get_bike_or_404(request, request.matchdict['id'])
    return bike.to_dict()

@view_config(route_name='bikes', request_method='POST', renderer='json')
def create_bike(request):
    # In a real application, only admins should add bikes.
    # get_user_id(request)

    data = request.json_body

    required_fields = ['title', 'price']
    missing = [f for f in required_fields if not data.get(f)]
    if missing:
        raise HTTPBadRequest(json_body={'error': f'Missing required fields: {", ".join(missing)}'})

    try:
        bike = Bike(
            title=data['title'],
            description=data.get('description'),
            price=data['price'],
            thumbnail=data.get('thumbnail')
        )
    except KeyError as e:
        return HTTPBadRequest(json_body={'error': f'Missing field: {e.args[0]}'})
    except (TypeError, ValueError) as e:
        return HTTPBadRequest(json_body={'error': f'Invalid data type for field: {e}'})

    request.dbsession.add(bike)
    request.dbsession.flush()

    return bike.to_dict()

@view_config(route_name='bike_detail', request_method='PUT', renderer='json')
def update_bike(request):
    # In a real application, only admins should update bikes.
    # get_user_id(request)

    bike = get_bike_or_404(request, request.matchdict['id'])
    data = request.json_body

    for key, value in data.items():
        if hasattr(bike, key):
            try:
                if key == 'price':
                    value = float(value)
                setattr(bike, key, value)
            except (TypeError, ValueError) as e:
                return HTTPBadRequest(json_body={'error': f'Invalid data type for field "{key}": {e}'})

    return bike.to_dict()

@view_config(route_name='bike_detail', request_method='DELETE', renderer='json')
def delete_bike(request):
    # In a real application, only admins should delete bikes.
    # get_user_id(request)

    bike = get_bike_or_404(request, request.matchdict['id'])
    request.dbsession.delete(bike)
    return {'message': 'Bike deleted successfully'}
