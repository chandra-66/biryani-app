from tests.conftest import client


def register_user(email: str, password: str, full_name: str, role: str = 'customer'):
    return client.post(
        '/api/v1/auth/register',
        json={'email': email, 'password': password, 'full_name': full_name, 'role': role},
    )


def login_user(email: str, password: str):
    return client.post('/api/v1/auth/login', json={'email': email, 'password': password})


def test_register_login_and_restaurant_flow():
    owner = register_user('owner1@example.com', 'secret123', 'Owner One', 'owner')
    assert owner.status_code == 201, owner.text

    login = login_user('owner1@example.com', 'secret123')
    assert login.status_code == 200, login.text
    token = login.json()['access_token']
    headers = {'Authorization': f'Bearer {token}'}

    restaurant = client.post(
        '/api/v1/restaurants',
        json={
            'name': 'Royal Biryani House',
            'slug': 'royal-biryani-house',
            'description': 'Best biryani in town',
            'address': 'MG Road',
            'city': 'Bengaluru',
            'state': 'Karnataka',
            'country': 'India',
        },
        headers=headers,
    )
    assert restaurant.status_code == 201, restaurant.text
    restaurant_id = restaurant.json()['id']

    menu = client.post(
        f'/api/v1/restaurants/{restaurant_id}/menu',
        json={
            'category': 'Chicken',
            'name': 'Chicken Dum Biryani',
            'description': 'Slow-cooked dum biryani',
            'price': '299.00',
            'portion_size': 'Full',
            'spice_level': 'medium',
            'is_available': True,
        },
        headers=headers,
    )
    assert menu.status_code == 201, menu.text
    item_id = menu.json()['id']

    customer = register_user('customer1@example.com', 'secret123', 'Customer One', 'customer')
    assert customer.status_code == 201, customer.text

    login_customer = login_user('customer1@example.com', 'secret123')
    assert login_customer.status_code == 200, login_customer.text
    customer_token = login_customer.json()['access_token']
    customer_headers = {'Authorization': f'Bearer {customer_token}'}

    address = client.post(
        '/api/v1/users/me/addresses',
        json={
            'label': 'Home',
            'address_line_1': '12 Residency Road',
            'city': 'Bengaluru',
            'state': 'Karnataka',
            'postal_code': '560025',
            'country': 'India',
            'is_default': True,
        },
        headers=customer_headers,
    )
    assert address.status_code == 201, address.text
    address_id = address.json()['id']

    cart = client.post('/api/v1/cart/items', json={'item_id': item_id, 'quantity': 2}, headers=customer_headers)
    assert cart.status_code == 201, cart.text

    order = client.post(
        '/api/v1/orders',
        json={'address_id': address_id, 'items': [{'item_id': item_id, 'quantity': 2}]},
        headers=customer_headers,
    )
    assert order.status_code == 201, order.text
    assert order.json()['total_amount'] == '598.00'

    review = client.post(
        '/api/v1/reviews',
        json={'restaurant_id': restaurant_id, 'item_id': item_id, 'rating': 5, 'comment': 'Very tasty'},
        headers=customer_headers,
    )
    assert review.status_code == 201, review.text
