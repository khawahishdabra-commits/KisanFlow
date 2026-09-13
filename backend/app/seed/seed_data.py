from datetime import datetime, date, timezone

from sqlalchemy import select

from app.core.database import SessionLocal
from app.models.centre import Centre
from app.models.crop import Crop
from app.models.operator import Operator
from app.models.price import Price
from app.models.queue import Queue
from app.models.resource import Resource


def seed_data():
    db = SessionLocal()

    try:
        # ---------------------------------------------------------
        # 1. Crops
        # ---------------------------------------------------------
        wheat = db.scalar(
            select(Crop).where(Crop.name == "Wheat")
        )

        if not wheat:
            wheat = Crop(
                name="Wheat",
                unit="quintal",
            )
            db.add(wheat)

        paddy = db.scalar(
            select(Crop).where(Crop.name == "Paddy")
        )

        if not paddy:
            paddy = Crop(
                name="Paddy",
                unit="quintal",
            )
            db.add(paddy)

        mustard = db.scalar(
            select(Crop).where(Crop.name == "Mustard")
        )

        if not mustard:
            mustard = Crop(
                name="Mustard",
                unit="quintal",
            )
            db.add(mustard)

        db.flush()

        # ---------------------------------------------------------
        # 2. Procurement Centres
        # ---------------------------------------------------------
        centre_a = db.scalar(
            select(Centre).where(Centre.name == "Centre A")
        )

        if not centre_a:
            centre_a = Centre(
                name="Centre A",
                address="Main Market Road",
                latitude=30.3782,
                longitude=76.7767,
                status="ACTIVE",
                capacity_per_hour=20,
            )
            db.add(centre_a)

        centre_b = db.scalar(
            select(Centre).where(Centre.name == "Centre B")
        )

        if not centre_b:
            centre_b = Centre(
                name="Centre B",
                address="Grain Market Road",
                latitude=30.3645,
                longitude=76.7890,
                status="ACTIVE",
                capacity_per_hour=25,
            )
            db.add(centre_b)

        centre_c = db.scalar(
            select(Centre).where(Centre.name == "Centre C")
        )

        if not centre_c:
            centre_c = Centre(
                name="Centre C",
                address="Agricultural Market Road",
                latitude=30.3920,
                longitude=76.7600,
                status="ACTIVE",
                capacity_per_hour=18,
            )
            db.add(centre_c)

        db.flush()

        # ---------------------------------------------------------
        # 3. Operators
        # ---------------------------------------------------------
        operators = [
            ("Operator A", "9000000001", centre_a),
            ("Operator B", "9000000002", centre_b),
            ("Operator C", "9000000003", centre_c),
        ]

        for name, phone, centre in operators:
            existing = db.scalar(
                select(Operator).where(
                    Operator.phone == phone
                )
            )

            if not existing:
                operator = Operator(
                    name=name,
                    phone=phone,
                    password_hash="DEMO_PASSWORD",
                    centre_id=centre.id,
                )
                db.add(operator)

        # ---------------------------------------------------------
        # 4. Prices
        # ---------------------------------------------------------
        price_data = [
            (centre_a, wheat, 2400, 2600),
            (centre_b, wheat, 2500, 2650),
            (centre_c, wheat, 2350, 2580),

            (centre_a, paddy, 2200, 2400),
            (centre_b, paddy, 2280, 2450),
            (centre_c, paddy, 2150, 2380),

            (centre_a, mustard, 5200, 5500),
            (centre_b, mustard, 5350, 5650),
            (centre_c, mustard, 5100, 5450),
        ]

        for centre, crop, buy_price, sell_price in price_data:
            existing = db.scalar(
                select(Price).where(
                    Price.centre_id == centre.id,
                    Price.crop_id == crop.id,
                    Price.effective_date == date.today(),
                )
            )

            if not existing:
                db.add(
                    Price(
                        centre_id=centre.id,
                        crop_id=crop.id,
                        buy_price=buy_price,
                        sell_price=sell_price,
                        effective_date=date.today(),
                    )
                )

        # ---------------------------------------------------------
        # 5. Queue state
        # ---------------------------------------------------------
        queue_data = [
            (centre_a, 35, 10.0, 105.0),
            (centre_b, 18, 8.0, 57.6),
            (centre_c, 52, 11.0, 190.7),
        ]

        for centre, queue_length, service_time, wait_time in queue_data:
            existing = db.scalar(
                select(Queue).where(
                    Queue.centre_id == centre.id
                )
            )

            if not existing:
                db.add(
                    Queue(
                        centre_id=centre.id,
                        queue_length=queue_length,
                        avg_service_time=service_time,
                        estimated_wait_minutes=wait_time,
                        last_updated=datetime.now(timezone.utc),
                    )
                )

        # ---------------------------------------------------------
        # 6. Resources
        # ---------------------------------------------------------
        resource_data = [
            (centre_a, "Weighing Machine", 3, 2, "AVAILABLE"),
            (centre_b, "Weighing Machine", 4, 3, "AVAILABLE"),
            (centre_c, "Weighing Machine", 2, 1, "LIMITED"),
        ]

        for centre, resource_type, total, available, status in resource_data:
            existing = db.scalar(
                select(Resource).where(
                    Resource.centre_id == centre.id,
                    Resource.resource_type == resource_type,
                )
            )

            if not existing:
                db.add(
                    Resource(
                        centre_id=centre.id,
                        resource_type=resource_type,
                        total_units=total,
                        available_units=available,
                        status=status,
                    )
                )

        db.commit()

        print("KisanFlow demo data seeded successfully.")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_data()