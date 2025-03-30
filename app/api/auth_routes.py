from flask import Blueprint, request, jsonify
from app.models import User, db
from app.forms import LoginForm, SignUpForm
from flask_login import current_user, login_user, logout_user, login_required
from sqlalchemy.exc import SQLAlchemyError
from functools import wraps
import time


auth_routes = Blueprint('auth', __name__)

# tracking failed login attempts
failed_login_attempts = {}

def rate_limiter(max_attempts=5, timeout=300):
    """Basic implementation of a rate limiter for auth routes"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            ip = request.remote_addr
            current_time = int(time.time())

            # Clear old entries
            for key in list(failed_login_attempts.keys()):
                timestamp, attempts = failed_login_attempts[key]
                if current_time - timestamp > timeout:
                    del failed_login_attempts[key]

            # Check if user is rate limited
            if ip in failed_login_attempts:
                timestamp, attempts = failed_login_attempts[ip]
                if attempts >= max_attempts and current_time - timestamp < timeout:
                    return jsonify({
                        "error": "Too many attempts",
                        "message": f"Please try again after {timeout - (current_time - timestamp)} seconds"
                    }), 429

            return f(*args, **kwargs)
        return decorated_function
    return decorator


@auth_routes.route('/')
def authenticate():
    """
    Authenticates a user.
    """
    if current_user.is_authenticated:
        return jsonify(current_user.to_dict())
    return jsonify({"error": "Unauthorized", "message": "Authentication required"}), 401


@auth_routes.route('/login', methods=['POST'])
@rate_limiter(max_attempts=5, timeout=300)
def login():
    """
    Logs a user in
    """
    ip = request.remote_addr
    form = LoginForm()
    form['csrf_token'].data = request.cookies['csrf_token']
    
    if form.validate_on_submit():
        # User is added to session and is logged on
        user = User.query.filter(User.email == form.data['email']).first()
        login_user(user)
        
        # Clear failed attempts on successful login
        if ip in failed_login_attempts:
            del failed_login_attempts[ip]
            
        return jsonify(user.to_dict())
    
    # Track failed login attempts
    current_time = int(time.time())
    if ip in failed_login_attempts:
        timestamp, attempts = failed_login_attempts[ip]
        failed_login_attempts[ip] = (current_time, attempts + 1)
    else:
        failed_login_attempts[ip] = (current_time, 1)
        
    return jsonify({"error": "Authentication failed", "details": form.errors}), 401


@auth_routes.route('/logout')
def logout():
    """
    Logs a user out
    """
    logout_user()
    return jsonify({"message": "User logged out"})


@auth_routes.route('/signup', methods=['POST'])
def sign_up():
    """
    Creates a new user and logs them in
    """
    form = SignUpForm()
    form['csrf_token'].data = request.cookies['csrf_token']
    
    if form.validate_on_submit():
        try:
            user = User(
                username=form.data['username'],
                email=form.data['email'],
                password=form.data['password']
            )
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return jsonify(user.to_dict())
        except SQLAlchemyError:
            db.session.rollback()
            return jsonify({"error": "Database error", "message": "Could not create user account"}), 500
            
    return jsonify({"error": "Validation failed", "details": form.errors}), 400


@auth_routes.route('/unauthorized')
def unauthorized():
    """
    Returns unauthorized JSON when flask-login authentication fails
    """
    return jsonify({"error": "Unauthorized", "message": "Authentication required"}), 401