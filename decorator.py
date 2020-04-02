from functools import wraps

from sqlalchemy.exc import IntegrityError
from flask import redirect, session


def handle_session(f):
    """ Handle session for DB transactions """

    def wrapper(self, *args, **kwargs):
        session = self.Session()
        try:
            result = f(self, session, *args, **kwargs)
            return result
        except IntegrityError:
            session.rollback()
            raise Exception("Error")
        finally:
            session.expunge_all()
            session.close()    
    return wrapper


def handle_login(f):
    """ Handle user login """

    @wraps(f)
    def wrapper(*args, **kwargs):
        if session.get("username") is None:
            return redirect("/get-started")
        return f(*args, **kwargs)
    return wrapper