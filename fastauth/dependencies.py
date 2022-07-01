from fastauth.db.database import sessionlocal


def get_db():
    db = None
    try:
        db = sessionlocal()
        yield db
    finally:
        db.close()
