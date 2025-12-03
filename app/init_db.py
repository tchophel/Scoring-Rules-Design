from app.database.database import engine, Base, SessionLocal
from app.database.seed import seed_data
import logging


def init_db():
    """Initialize the database: create tables and seed data."""
    print("Creating database tables...")
    try:
        Base.metadata.create_all(bind=engine)
        print("Tables created successfully.")
        db = SessionLocal()
        try:
            seed_data(db)
        except Exception as e:
            logging.exception(f"Error seeding data: {e}")
            db.rollback()
        finally:
            db.close()
    except Exception as e:
        logging.exception(f"Error initializing database: {e}")


if __name__ == "__main__":
    init_db()