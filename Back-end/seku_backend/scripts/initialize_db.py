import argparse
import sys
from datetime import date

from pyramid.paster import bootstrap, setup_logging
from sqlalchemy.exc import OperationalError

from ..models.user import User
from ..models.bike import Bike
from ..models.rental import Rental
from ..models.meta import Base


def setup_models(dbsession, engine):
    print("Creating tables if they don't exist...")
    Base.metadata.create_all(engine)
    print("Tables created or already exist.")

    print("Inserting sample data...")

    if dbsession.query(User).count() == 0:
        user1 = User(
            username="john_doe",
            email="john.doe@example.com",
        )
        user1.password = "password123"

        user2 = User(
            username="jane_smith",
            email="jane.smith@example.com",
        )
        user2.password = "securepass"

        dbsession.add_all([user1, user2])
        dbsession.flush()

        print(f"Users '{user1.username}' and '{user2.username}' added.")

        bike1 = Bike(
            title="Sepeda Gunung Trailblazer",
            description="Sepeda gunung tangguh untuk medan off-road, dilengkapi suspensi ganda.",
            price=50000.00,
            thumbnail="https://example.com/images/bike-mtb.jpg"
        )

        bike2 = Bike(
            title="Sepeda Lipat Urbanite",
            description="Ringkas dan nyaman untuk perjalanan kota, mudah dilipat dan dibawa.",
            price=35000.00,
            thumbnail="https://example.com/images/bike-folding.jpg"
        )

        bike3 = Bike(
            title="Sepeda Listrik EcoRide",
            description="Bantuan listrik untuk perjalanan jauh dan menanjak, ramah lingkungan.",
            price=75000.00,
            thumbnail="https://example.com/images/bike-electric.jpg"
        )

        dbsession.add_all([bike1, bike2, bike3])
        dbsession.flush()

        print("Sample bikes added.")

        rental1 = Rental(
            user_id=user1.id,
            bike_id=bike1.id,
            rental_date=date(2025, 5, 20),
            duration_days=3,
            total_amount=bike1.price * 3,
            payment_method="non-tunai",
            ticket_id="RENT-20250520-001",
            status="completed"
        )

        rental2 = Rental(
            user_id=user2.id,
            bike_id=bike2.id,
            rental_date=date(2025, 5, 22),
            duration_days=1,
            total_amount=bike2.price * 1,
            payment_method="tunai",
            ticket_id="RENT-20250522-002",
            status="pending"
        )

        rental3 = Rental(
            user_id=user1.id,
            bike_id=bike3.id,
            rental_date=date(2025, 5, 25),
            duration_days=5,
            total_amount=bike3.price * 5,
            payment_method="non-tunai",
            ticket_id="RENT-20250525-003",
            status="pending"
        )

        dbsession.add_all([rental1, rental2, rental3])
        print("Sample rentals added.")
    else:
        print("Sample data already exists in the database, skipping data insertion.")


def parse_args(argv):
    parser = argparse.ArgumentParser(
        description='Script to initialize database with sample data for Sepeda Rental App.'
    )
    parser.add_argument(
        'config_uri',
        help='Configuration file, e.g., development.ini',
    )
    return parser.parse_args(argv[1:])


def main(argv=sys.argv):
    args = parse_args(argv)
    setup_logging(args.config_uri)
    env = bootstrap(args.config_uri)

    try:
        with env['request'].tm:
            dbsession = env['request'].dbsession
            engine = env['request'].registry['dbsession_factory'].kw['bind']
            setup_models(dbsession, engine)
            print("✅ Database initialization and sample data addition successful.")
    except OperationalError as err:
        print("❌ OperationalError:", err)
        print('''
Database connection failed. Possible causes:
1. You may need to initialize the tables using alembic.
2. The database server may not be running or misconfigured in development.ini.
        ''')
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
