def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    
    config.add_route('register', '/register')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')

    # Bike Routes
    config.add_route('bikes', '/bikes')
    config.add_route('bike_detail', '/bikes/{id}')

    # Rental Routes
    config.add_route('rentals', '/rentals')
    config.add_route('rental_detail', '/rentals/{id}')
    
    config.add_route('admin_rentals', '/admin/rentals')
    config.add_route('admin_rental_detail', '/admin/rentals/{id}')
