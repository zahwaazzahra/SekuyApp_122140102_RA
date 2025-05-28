from pyramid.view import view_config
from pyramid.response import Response
from pyramid.httpexceptions import HTTPNotFound, HTTPBadRequest, HTTPUnauthorized, HTTPConflict
from ..models.rental import Rental
from ..models.bike import Bike

from datetime import datetime, date
import uuid

def get_user_id(request):
    user_id = request.authenticated_userid
    if not user_id:
        raise HTTPUnauthorized(json_body={'error': 'Unauthorized'})
    return user_id

def parse_date(value, field):
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPBadRequest(json_body={'error': f'Invalid date format for {field}, expected %Y-%m-%d'})

def get_bike_or_404(request, bike_id):
    try:
        bike_id = int(bike_id)
    except ValueError:
        raise HTTPBadRequest(json_body={'error': 'Invalid bike ID format'})

    bike = request.dbsession.get(Bike, bike_id)
    if not bike:
        raise HTTPNotFound(json_body={'error': 'Bike not found'})
    return bike

def get_user_rental_or_404(request, rental_id):
    user_id = get_user_id(request)

    try:
        rental_id = int(rental_id)
    except ValueError:
        raise HTTPBadRequest(json_body={'error': 'Invalid rental ID format'})

    rental = request.dbsession.get(Rental, rental_id)
    if not rental or str(rental.user_id) != user_id:
        raise HTTPNotFound(json_body={'error': 'Rental not found or forbidden'})
    return rental

# Fungsi helper baru yang bisa mengambil rental tanpa filter user_id (sudah ada)
def get_rental_by_id_or_404(request, rental_id):
    try:
        rental_id = int(rental_id)
    except ValueError:
        raise HTTPBadRequest(json_body={'error': 'Invalid rental ID format'})

    rental = request.dbsession.get(Rental, rental_id)
    if not rental:
        raise HTTPNotFound(json_body={'error': 'Rental not found'})
    return rental

@view_config(route_name='rentals', request_method='GET', renderer='json')
def list_rentals(request):
    user_id_str = get_user_id(request)
    try:
        user_id = int(user_id_str)
    except ValueError:
        raise HTTPUnauthorized(json_body={'error': 'Invalid user ID in session'})

    rentals = request.dbsession.query(Rental).filter_by(user_id=user_id).all()
    return [r.to_dict() for r in rentals]

@view_config(route_name='rental_detail', request_method='GET', renderer='json')
def get_rental(request):
    rental = get_user_rental_or_404(request, request.matchdict['id'])
    return rental.to_dict()

@view_config(route_name='rentals', request_method='POST', renderer='json')
def create_rental(request):
    user_id_str = get_user_id(request)
    try:
        user_id = int(user_id_str)
    except ValueError:
        raise HTTPUnauthorized(json_body={'error': 'Invalid user ID in session'})

    data = request.json_body

    required_fields = ['bike_id', 'rental_date', 'duration_days', 'payment_method']
    missing = [f for f in required_fields if not data.get(f)]
    if missing:
        raise HTTPBadRequest(json_body={'error': f'Missing required fields: {", ".join(missing)}'})

    try:
        bike_id = data['bike_id']
        rental_date_str = data['rental_date']
        duration_days = data['duration_days']
        payment_method = data['payment_method']

        bike = get_bike_or_404(request, bike_id)
        rental_date = parse_date(rental_date_str, 'rental_date')
        total_amount = bike.price * duration_days
        ticket_id = f"RENT-{datetime.now().strftime('%Y%m%d%H%M%S')}-{str(uuid.uuid4())[:8].upper()}"

        if request.dbsession.query(Rental).filter_by(ticket_id=ticket_id).first():
            return HTTPConflict(json_body={'error': 'Failed to generate unique ticket ID. Please try again.'})

        rental = Rental(
            user_id=user_id,
            bike_id=bike.id,
            rental_date=rental_date,
            duration_days=duration_days,
            total_amount=total_amount,
            payment_method=payment_method,
            ticket_id=ticket_id,
            status=data.get('status', 'pending')
        )

        request.dbsession.add(rental)
        request.dbsession.flush()

        return rental.to_dict()

    except KeyError as e:
        return HTTPBadRequest(json_body={'error': f'Missing field: {e.args[0]}'})
    except (TypeError, ValueError) as e:
        return HTTPBadRequest(json_body={'error': f'Invalid data type or value for field: {e}'})
    except HTTPNotFound as e:
        return e
    except HTTPBadRequest as e:
        return e

@view_config(route_name='rental_detail', request_method='PUT', renderer='json')
def update_rental(request):
    rental = get_user_rental_or_404(request, request.matchdict['id'])
    data = request.json_body

    for key, value in data.items():
        if key == 'rental_date':
            try:
                value = parse_date(value, key)
            except HTTPBadRequest as e:
                return e

        if hasattr(rental, key):
            try:
                if key == 'duration_days':
                    value = int(value)
                elif key == 'total_amount':
                    value = float(value)
                setattr(rental, key, value)
            except (TypeError, ValueError) as e:
                return HTTPBadRequest(json_body={'error': f'Invalid data type for field "{key}": {e}'})

    if 'duration_days' in data:
        bike = get_bike_or_404(request, rental.bike_id)
        rental.total_amount = bike.price * rental.duration_days

    return rental.to_dict()

@view_config(route_name='rental_detail', request_method='DELETE', renderer='json')
def cancel_rental(request):
    # Ini hanya mengubah status menjadi 'cancelled', tidak menghapus dari DB
    rental = get_user_rental_or_404(request, request.matchdict['id'])
    rental.status = 'cancelled'
    return {'message': f'Rental {rental.ticket_id} cancelled successfully'}

@view_config(route_name='admin_rentals', request_method='GET', renderer='json')
def list_all_rentals(request):
    user_id = get_user_id(request)
    rentals = request.dbsession.query(Rental).all()
    return [r.to_dict() for r in rentals]

@view_config(route_name='admin_rental_detail', request_method='PUT', renderer='json')
def admin_update_rental(request):
    rental = get_rental_by_id_or_404(request, request.matchdict['id'])
    data = request.json_body

    for key, value in data.items():
        if key == 'rental_date':
            try:
                value = datetime.strptime(value, "%Y-%m-%d").date()
            except ValueError:
                raise HTTPBadRequest(json_body={'error': f'Invalid date format for {key}, expected %Y-%m-%d'})

        if hasattr(rental, key):
            try:
                if key == 'duration_days':
                    value = int(value)
                elif key == 'total_amount':
                    value = float(value)
                setattr(rental, key, value)
            except (TypeError, ValueError) as e:
                raise HTTPBadRequest(json_body={'error': f'Invalid data type for field "{key}": {e}'})

    if 'duration_days' in data and rental.bike_id:
        bike = request.dbsession.get(Bike, rental.bike_id)
        if bike:
            rental.total_amount = bike.price * rental.duration_days

    return rental.to_dict()

# Fungsi BARU untuk menghapus rental oleh Admin
@view_config(route_name='admin_rental_detail', request_method='DELETE', renderer='json')
def admin_delete_rental(request):
    # Menggunakan helper get_rental_by_id_or_404 agar admin bisa menghapus rental siapapun
    rental = get_rental_by_id_or_404(request, request.matchdict['id'])
    
    # Hapus objek rental dari sesi database
    request.dbsession.delete(rental)
    
    # Commit perubahan ke database (jika tidak otomatis dilakukan oleh transaction manager)
    # request.dbsession.flush() # Opsional, tergantung setup transaction Pyramid
    
    return {'message': f'Rental {rental.ticket_id} (ID: {rental.id}) deleted successfully.'}