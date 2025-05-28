import unittest
import transaction
from datetime import date, datetime
from uuid import uuid4

from pyramid import testing
from pyramid.response import Response
from pyramid.httpexceptions import HTTPNotFound, HTTPBadRequest, HTTPUnauthorized, HTTPConflict

from seku_backend.models import (
    get_engine,
    get_session_factory,
    get_tm_session,
    User,
    Bike,
    Rental
)
from seku_backend.models.meta import Base

from seku_backend.views.auth import register, login, logout
from seku_backend.views.bike import list_bikes, get_bike, create_bike, update_bike, delete_bike
from seku_backend.views.rental import list_rentals, get_rental, create_rental, update_rental, cancel_rental


class BaseTest(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp(settings={
            'sqlalchemy.url': 'sqlite:///:memory:'
        })
        self.config.include('seku_backend.models')
        settings = self.config.get_settings()
        self.engine = get_engine(settings)
        session_factory = get_session_factory(self.engine)
        self.session = get_tm_session(session_factory, transaction.manager)

        # Hapus semua tabel sebelum membuat ulang untuk memastikan lingkungan bersih
        Base.metadata.drop_all(self.engine)
        Base.metadata.create_all(self.engine)

    def tearDown(self):
        transaction.abort()
        testing.tearDown()
        Base.metadata.drop_all(self.engine) # Pastikan ini berjalan dengan baik


    def dummy_request(self, user_id=None, json_body=None, matchdict=None):
        req = testing.DummyRequest(
            dbsession=self.session,
            json_body=json_body or {},
            matchdict=matchdict or {}
        )
        if user_id is not None:
            req.authenticated_userid = str(user_id)
        return req


class TestUserModel(BaseTest):
    def test_user_password_check(self):
        user = User(username="testuser", email="test@example.com")
        user.password = "secret"
        self.session.add(user)
        self.session.flush()

        self.assertTrue(user.check_password("secret"))
        self.assertFalse(user.check_password("wrong"))

    def test_user_repr_and_dict(self):
        user = User(username="john", email="john@doe.com")
        user.password = "pwd123"
        self.session.add(user)
        self.session.flush()

        user_dict = user.to_dict()
        self.assertIn("john", repr(user))
        self.assertEqual(user_dict["username"], "john")
        self.assertEqual(user_dict["email"], "john@doe.com")
        self.assertNotIn("password", user_dict)
        self.assertIsNotNone(user_dict["id"])


class TestBikeModel(BaseTest):
    def test_bike_to_dict_and_repr(self):
        bike = Bike(
            title="Mountain Bike",
            description="Robust bike for trails",
            price=150000.00,
            thumbnail="http://example.com/mtb.jpg"
        )
        self.session.add(bike)
        self.session.flush()

        data = bike.to_dict()
        self.assertIn("Mountain Bike", repr(bike))
        self.assertEqual(data["title"], "Mountain Bike")
        self.assertEqual(data["price"], 150000.00)
        self.assertIsNotNone(data["id"])


class TestRentalModel(BaseTest):
    def test_rental_to_dict_and_repr(self):
        user = User(username="renter", email="renter@example.com")
        user.password = "pass"
        bike = Bike(title="City Bike", description="Good for city", price=50000.00)
        self.session.add_all([user, bike])
        self.session.flush()

        rental = Rental(
            user_id=user.id,
            bike_id=bike.id,
            rental_date=date.today(),
            duration_days=2,
            total_amount=100000.00,
            payment_method="tunai",
            ticket_id=f"TICKET-{str(uuid4())[:8].upper()}",
            status="pending"
        )
        self.session.add(rental)
        self.session.flush()

        data = rental.to_dict()
        self.assertIn(rental.ticket_id, repr(rental))
        self.assertEqual(data["status"], "pending")
        self.assertEqual(data["user_id"], user.id)
        self.assertEqual(data["bike_id"], bike.id)
        self.assertEqual(data["total_amount"], 100000.00)
        self.assertIsNotNone(data["id"])


class TestAuthViews(BaseTest):
    def test_register_success(self):
        request = self.dummy_request(
            json_body={
                "username": "newuser",
                "email": "new@example.com",
                "password": "secret"
            }
        )
        result = register(request)
        self.assertEqual(result["message"], "Registration successful")
        self.assertIn("newuser", result["user"]["username"])
        self.assertIsNotNone(result["user"]["id"])

    def test_register_duplicate_email(self):
        user = User(username="exist", email="exist@example.com")
        user.password = "123"
        self.session.add(user)
        self.session.flush()

        request = self.dummy_request(
            json_body={
                "username": "another",
                "email": "exist@example.com",
                "password": "secret"
            }
        )
        result = register(request)
        self.assertEqual(result.status_code, 409)

    def test_register_missing_fields(self):
        request = self.dummy_request(
            json_body={
                "username": "incomplete",
                "email": "incomplete@example.com"
            }
        )
        response = register(request)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Missing fields", response.json_body["error"])

    def test_login_success(self):
        user = User(username="loginuser", email="log@example.com")
        user.password = "password"
        self.session.add(user)
        self.session.flush()

        request = self.dummy_request(
            json_body={
                "email": "log@example.com",
                "password": "password"
            }
        )
        response = login(request)
        self.assertEqual(response.json_body["message"], "Login successful")
        self.assertIn("loginuser", response.json_body["user"]["username"])
        self.assertIn("Set-Cookie", response.headers)

    def test_login_invalid(self):
        request = self.dummy_request(
            json_body={"email": "wrong@example.com", "password": "wrong"}
        )
        response = login(request)
        self.assertEqual(response.status_code, 401)

    def test_login_missing_fields(self):
        request = self.dummy_request(
            json_body={"email": "missing@example.com"}
        )
        response = login(request)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Missing fields", response.json_body["error"])

    def test_logout(self):
        # Untuk test logout, kita harus memastikan ada headers yang diset.
        # Biasanya, after successful login, ada header Set-Cookie.
        # Karena logout menghapus cookie, kita bisa buat dummy response yang meniru itu.
        # Atau, panggil login dulu untuk mendapatkan headers, lalu logout.
        # Namun, cara paling sederhana adalah menguji bahwa forget() dipanggil
        # dan Response mengembalikan headers untuk menghapus cookie.
        # Karena response dari `logout` langsung mengembalikan `Response` dari `forget`,
        # yang seharusnya sudah memiliki `Set-Cookie` untuk menghapus.
        request = self.dummy_request()
        # Saat logout, biasanya cookie diset untuk menghapus sesi.
        # Pastikan Pyramid forget() menambahkan Set-Cookie header.
        # Jika assert ini fail, mungkin ada masalah dengan konfigurasi auth di Pyramid.
        response = logout(request)
        self.assertEqual(response.json_body["message"], "Logout successful")
        self.assertIn("Set-Cookie", response.headers) # Ini akan menguji header Set-Cookie yang dihapus


class TestBikeViews(BaseTest):
    def setUp(self):
        super().setUp()
        self.test_user = User(username="admin_user", email="admin@example.com")
        self.test_user.password = "adminpass"
        self.session.add(self.test_user)
        self.session.flush()

        self.bike1 = Bike(title="Test Bike 1", price=100000.00)
        self.bike2 = Bike(title="Test Bike 2", price=120000.00)
        self.session.add_all([self.bike1, self.bike2])
        self.session.flush()
        self.bike1 = self.session.query(Bike).filter_by(title="Test Bike 1").first()
        self.bike2 = self.session.query(Bike).filter_by(title="Test Bike 2").first()

    def test_list_bikes(self):
        request = self.dummy_request()
        response = list_bikes(request)
        self.assertEqual(len(response), 2)
        self.assertTrue(any(b["title"] == "Test Bike 1" for b in response))

    def test_get_bike_success(self):
        request = self.dummy_request(matchdict={"id": str(self.bike1.id)})
        response = get_bike(request)
        self.assertEqual(response["id"], self.bike1.id)
        self.assertEqual(response["title"], "Test Bike 1")

    def test_get_bike_not_found(self):
        request = self.dummy_request(matchdict={"id": "999999999"})
        response = get_bike(request)
        self.assertEqual(response.status_code, 404)
        self.assertIn("Bike not found", response.json_body["error"])

    def test_get_bike_invalid_id_format(self):
        request = self.dummy_request(matchdict={"id": "abc"})
        response = get_bike(request)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid bike ID format", response.json_body["error"])

    def test_create_bike_success(self):
        create_data = {
            "title": "New Electric Bike",
            "description": "Fast and eco-friendly",
            "price": 200000.00,
            "thumbnail": "http://example.com/ebike.jpg"
        }
        # Jika create_bike di views/bike.py membutuhkan autentikasi
        request = self.dummy_request(user_id=self.test_user.id, json_body=create_data)
        response = create_bike(request)
        self.assertEqual(response["title"], "New Electric Bike")
        self.assertEqual(response["price"], 200000.00)
        self.assertIsNotNone(response["id"])
        # Asumsi view mengembalikan message sukses. Jika tidak, hapus baris ini.
        # Karena di views/bike.py tidak ada message success di create_bike, hapus assert ini.
        # self.assertIn("message", response)
        # self.assertEqual(response["message"], "Bike created successfully")

    def test_create_bike_missing_fields(self):
        create_data = {"description": "Missing title and price"}
        # Jika create_bike di views/bike.py membutuhkan autentikasi
        request = self.dummy_request(user_id=self.test_user.id, json_body=create_data)
        response = create_bike(request)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Missing required fields", response.json_body["error"])

    def test_create_bike_invalid_price_type(self):
        create_data = {
            "title": "Bad Bike",
            "description": "Will fail",
            "price": "not_a_number",
            "thumbnail": "http://example.com/bad.jpg"
        }
        # Jika create_bike di views/bike.py membutuhkan autentikasi
        request = self.dummy_request(user_id=self.test_user.id, json_body=create_data)
        response = create_bike(request)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid data type for field", response.json_body["error"])

    def test_create_bike_unauthenticated(self):
        create_data = {"title": "Unauthorized Bike", "price": 100.00}
        request = self.dummy_request(user_id=None, json_body=create_data)
        response = create_bike(request)
        self.assertEqual(response.status_code, 401)
        self.assertIn("Unauthorized", response.json_body["error"])

    def test_update_bike_success(self):
        update_data = {"price": 110000.00, "description": "Updated description"}
        # Jika update_bike di views/bike.py membutuhkan autentikasi
        request = self.dummy_request(
            user_id=self.test_user.id,
            matchdict={"id": str(self.bike1.id)},
            json_body=update_data
        )
        response = update_bike(request)
        self.assertEqual(response["price"], 110000.00)
        self.assertEqual(response["description"], "Updated description")

    def test_update_bike_not_found(self):
        update_data = {"price": 110000.00}
        # Jika update_bike di views/bike.py membutuhkan autentikasi
        request = self.dummy_request(
            user_id=self.test_user.id,
            matchdict={"id": "999999999"},
            json_body=update_data
        )
        response = update_bike(request)
        self.assertEqual(response.status_code, 404)
        self.assertIn("Bike not found", response.json_body["error"])

    def test_update_bike_invalid_id_format(self):
        update_data = {"price": 110000.00}
        # Jika update_bike di views/bike.py membutuhkan autentikasi
        request = self.dummy_request(
            user_id=self.test_user.id,
            matchdict={"id": "abc"},
            json_body=update_data
        )
        response = update_bike(request)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid bike ID format", response.json_body["error"])

    def test_update_bike_invalid_price_type(self):
        update_data = {"price": "xyz"}
        # Jika update_bike di views/bike.py membutuhkan autentikasi
        request = self.dummy_request(
            user_id=self.test_user.id,
            matchdict={"id": str(self.bike1.id)},
            json_body=update_data
        )
        response = update_bike(request)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid data type for field \"price\"", response.json_body["error"])

    def test_update_bike_with_non_existent_field(self):
        # Ini untuk memastikan loop 'for' di update_bike tercakup sepenuhnya
        # saat ada field yang tidak ada di model.
        update_data = {"non_existent_field": "some_value", "price": 123456.00}
        # Jika update_bike di views/bike.py membutuhkan autentikasi
        request = self.dummy_request(
            user_id=self.test_user.id,
            matchdict={"id": str(self.bike1.id)},
            json_body=update_data
        )
        response = update_bike(request)
        self.assertEqual(response["price"], 123456.00)
        self.assertNotIn("non_existent_field", response)

    def test_update_bike_unauthenticated(self):
        update_data = {"price": 130000.00}
        request = self.dummy_request(
            user_id=None,
            matchdict={"id": str(self.bike1.id)},
            json_body=update_data
        )
        response = update_bike(request)
        self.assertEqual(response.status_code, 401)
        self.assertIn("Unauthorized", response.json_body["error"])

    def test_delete_bike_success(self):
        bike_to_delete = Bike(title="To Be Deleted", price=50000)
        self.session.add(bike_to_delete)
        self.session.flush()
        delete_id = bike_to_delete.id

        # Jika delete_bike di views/bike.py membutuhkan autentikasi
        request = self.dummy_request(user_id=self.test_user.id, matchdict={"id": str(delete_id)})
        response = delete_bike(request)
        self.assertEqual(response["message"], "Bike deleted successfully")

        deleted_bike = self.session.get(Bike, delete_id)
        self.assertIsNone(deleted_bike)

    def test_delete_bike_not_found(self):
        # Jika delete_bike di views/bike.py membutuhkan autentikasi
        request = self.dummy_request(user_id=self.test_user.id, matchdict={"id": "999999999"})
        response = delete_bike(request)
        self.assertEqual(response.status_code, 404)
        self.assertIn("Bike not found", response.json_body["error"])

    def test_delete_bike_invalid_id_format(self):
        # Jika delete_bike di views/bike.py membutuhkan autentikasi
        request = self.dummy_request(user_id=self.test_user.id, matchdict={"id": "xyz"})
        response = delete_bike(request)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid bike ID format", response.json_body["error"])

    def test_delete_bike_unauthenticated(self):
        bike_to_delete_unauth = Bike(title="Unauthorized Delete", price=100)
        self.session.add(bike_to_delete_unauth)
        self.session.flush()
        delete_id_unauth = bike_to_delete_unauth.id

        request = self.dummy_request(user_id=None, matchdict={"id": str(delete_id_unauth)})
        response = delete_bike(request)
        self.assertEqual(response.status_code, 401)
        self.assertIn("Unauthorized", response.json_body["error"])


class TestRentalViews(BaseTest):
    def setUp(self):
        super().setUp()
        self.user1 = User(username="renter1", email="r1@example.com")
        self.user1.password = "pass1"
        self.user2 = User(username="renter2", email="r2@example.com")
        self.user2.password = "pass2"
        self.session.add_all([self.user1, self.user2])
        self.session.flush()

        self.bike1 = Bike(title="Bike A", price=50000.00)
        self.bike2 = Bike(title="Bike B", price=75000.00)
        self.session.add_all([self.bike1, self.bike2])
        self.session.flush()

        self.rental1 = Rental(
            user_id=self.user1.id,
            bike_id=self.bike1.id,
            rental_date=date(2025, 6, 1),
            duration_days=2,
            total_amount=self.bike1.price * 2,
            payment_method="tunai",
            ticket_id="RENT-A1",
            status="pending"
        )
        self.session.add(self.rental1)
        self.session.flush()

    def test_list_rentals_authenticated(self):
        request = self.dummy_request(user_id=self.user1.id)
        response = list_rentals(request)
        self.assertEqual(len(response), 1)
        self.assertEqual(response[0]["ticket_id"], "RENT-A1")
        self.assertEqual(response[0]["user_id"], self.user1.id)

    def test_list_rentals_unauthenticated(self):
        request = self.dummy_request(user_id=None)
        response = list_rentals(request)
        self.assertEqual(response.status_code, 401)

    def test_get_rental_success(self):
        request = self.dummy_request(user_id=self.user1.id, matchdict={"id": str(self.rental1.id)})
        response = get_rental(request)
        self.assertEqual(response["ticket_id"], "RENT-A1")
        self.assertEqual(response["user_id"], self.user1.id)

    def test_get_rental_not_found_or_forbidden(self):
        request = self.dummy_request(user_id=self.user1.id, matchdict={"id": "999999999"})
        response = get_rental(request)
        self.assertEqual(response.status_code, 404)

        request = self.dummy_request(user_id=self.user2.id, matchdict={"id": str(self.rental1.id)})
        response = get_rental(request)
        self.assertEqual(response.status_code, 404)

    def test_get_rental_unauthenticated(self):
        request = self.dummy_request(user_id=None, matchdict={"id": str(self.rental1.id)})
        response = get_rental(request)
        self.assertEqual(response.status_code, 401)

    def test_get_rental_invalid_id_format(self):
        request = self.dummy_request(user_id=self.user1.id, matchdict={"id": "abc"})
        response = get_rental(request)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid rental ID format", response.json_body["error"])

    def test_create_rental_success(self):
        create_data = {
            "bike_id": self.bike2.id,
            "rental_date": str(date(2025, 6, 5)),
            "duration_days": 3,
            "payment_method": "non-tunai"
        }
        request = self.dummy_request(user_id=self.user1.id, json_body=create_data)
        response = create_rental(request)
        self.assertIsNotNone(response["ticket_id"])
        self.assertEqual(response["user_id"], self.user1.id)
        self.assertEqual(response["bike_id"], self.bike2.id)
        self.assertEqual(response["total_amount"], self.bike2.price * 3)
        self.assertEqual(response["status"], "pending")

    def test_create_rental_missing_fields(self):
        create_data = {
            "bike_id": self.bike1.id,
            "rental_date": str(date(2025, 6, 5))
        }
        request = self.dummy_request(user_id=self.user1.id, json_body=create_data)
        response = create_rental(request)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Missing required fields", response.json_body["error"])

    def test_create_rental_invalid_bike_id(self):
        create_data = {
            "bike_id": 999999999,
            "rental_date": str(date(2025, 6, 5)),
            "duration_days": 3,
            "payment_method": "tunai"
        }
        request = self.dummy_request(user_id=self.user1.id, json_body=create_data)
        response = create_rental(request)
        self.assertEqual(response.status_code, 404)

    def test_create_rental_unauthenticated(self):
        create_data = {
            "bike_id": self.bike2.id,
            "rental_date": str(date(2025, 6, 5)),
            "duration_days": 3,
            "payment_method": "non-tunai"
        }
        request = self.dummy_request(user_id=None, json_body=create_data)
        response = create_rental(request)
        self.assertEqual(response.status_code, 401)

    def test_create_rental_invalid_date_format(self):
        create_data = {
            "bike_id": self.bike1.id,
            "rental_date": "2025/06/05",
            "duration_days": 1,
            "payment_method": "tunai"
        }
        request = self.dummy_request(user_id=self.user1.id, json_body=create_data)
        response = create_rental(request)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid date format", response.json_body["error"])

    def test_create_rental_invalid_duration_type(self):
        create_data = {
            "bike_id": self.bike1.id,
            "rental_date": str(date(2025, 6, 5)),
            "duration_days": "two",
            "payment_method": "tunai"
        }
        request = self.dummy_request(user_id=self.user1.id, json_body=create_data)
        response = create_rental(request)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid data type or value for field", response.json_body["error"])

    def test_update_rental_success(self):
        update_data = {"duration_days": 5, "status": "completed"}
        request = self.dummy_request(
            user_id=self.user1.id,
            matchdict={"id": str(self.rental1.id)},
            json_body=update_data
        )
        response = update_rental(request)
        self.assertEqual(response["duration_days"], 5)
        self.assertEqual(response["status"], "completed")
        self.assertEqual(response["total_amount"], self.bike1.price * 5)

    def test_update_rental_not_found_or_forbidden(self):
        update_data = {"status": "returned"}
        request = self.dummy_request(user_id=self.user1.id, matchdict={"id": "999999999"}, json_body=update_data)
        response = update_rental(request)
        self.assertEqual(response.status_code, 404)

        request = self.dummy_request(user_id=self.user2.id, matchdict={"id": str(self.rental1.id)}, json_body=update_data)
        response = update_rental(request)
        self.assertEqual(response.status_code, 404)

    def test_update_rental_invalid_id_format(self):
        update_data = {"status": "completed"}
        request = self.dummy_request(
            user_id=self.user1.id,
            matchdict={"id": "def"},
            json_body=update_data
        )
        response = update_rental(request)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid rental ID format", response.json_body["error"])

    def test_update_rental_invalid_data_type(self):
        update_data = {"duration_days": "lima"}
        request = self.dummy_request(
            user_id=self.user1.id,
            matchdict={"id": str(self.rental1.id)},
            json_body=update_data
        )
        response = update_rental(request)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid data type for field", response.json_body["error"])

    def test_update_rental_invalid_date_format(self):
        update_data = {"rental_date": "2025/06/05"}
        request = self.dummy_request(
            user_id=self.user1.id,
            matchdict={"id": str(self.rental1.id)},
            json_body=update_data
        )
        response = update_rental(request)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid date format", response.json_body["error"])

    def test_cancel_rental_success(self):
        request = self.dummy_request(user_id=self.user1.id, matchdict={"id": str(self.rental1.id)})
        response = cancel_rental(request)
        self.assertEqual(response["message"], f"Rental {self.rental1.ticket_id} cancelled successfully")

        updated_rental = self.session.get(Rental, self.rental1.id)
        self.assertEqual(updated_rental.status, "cancelled")

    def test_cancel_rental_forbidden(self):
        request = self.dummy_request(user_id=self.user2.id, matchdict={"id": str(self.rental1.id)})
        response = cancel_rental(request)
        self.assertEqual(response.status_code, 404)

    def test_cancel_rental_invalid_id_format(self):
        request = self.dummy_request(user_id=self.user1.id, matchdict={"id": "ghi"})
        response = cancel_rental(request)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid rental ID format", response.json_body["error"])


if __name__ == "__main__":
    unittest.main()