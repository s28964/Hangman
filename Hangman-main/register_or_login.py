import bcrypt
from models import User
from database import session

def register(username, password):
    if not username or not password or len(username) < 3 or len(password) < 4:
        return False, "Username must be at least 3 characters long abd password must be at least 4 characters long"

    if session.query(User).filter_by(username = username).first():
        return False, "User already exists"

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    user = User(username = username, password = hashed_password.decode('utf-8'))
    session.add(user)
    session.commit()
    return True, "User has been registered"

def login(username, password):
    if not username or not password:
        return False, "Username and/or password cannot be empty"

    user = session.query(User).filter_by(username = username).first()
    if not user:
        return False, "Wrong login or password"

    if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        return True, f"Welcome {username}"
    else:
        return False, "Wrong login or password"