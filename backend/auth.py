"""
Authentication module with JWT token management
"""
from flask import request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, verify_jwt_in_request
from functools import wraps
from datetime import datetime, timedelta
import json
from models import db, User, UserActivity

def register_user(username, email, password, role='voyageur'):
    """
    Register a new user
    """
    # Check if user already exists
    if User.query.filter_by(username=username).first():
        return {'success': False, 'error': 'Username already exists'}, 400
    
    if User.query.filter_by(email=email).first():
        return {'success': False, 'error': 'Email already exists'}, 400
    
    # Validate role
    if role not in ['voyageur', 'admin']:
        role = 'voyageur'
    
    # Create new user
    user = User(username=username, email=email, role=role)
    user.set_password(password)
    
    try:
        db.session.add(user)
        db.session.commit()
        
        # Log registration activity
        log_activity(user.id, 'registration', {'username': username, 'role': role})
        
        return {
            'success': True,
            'message': 'User registered successfully',
            'user': user.to_dict()
        }, 201
    except Exception as e:
        db.session.rollback()
        return {'success': False, 'error': str(e)}, 500

def login_user(username, password):
    """
    Login user and return JWT tokens
    """
    user = User.query.filter_by(username=username).first()
    
    if not user or not user.check_password(password):
        return {'success': False, 'error': 'Invalid username or password'}, 401
    
    if not user.is_active:
        return {'success': False, 'error': 'Account is deactivated'}, 403
    
    # Update last login
    user.last_login = datetime.utcnow()
    db.session.commit()
    
    # Create tokens
    access_token = create_access_token(
        identity=user.id,
        additional_claims={'role': user.role, 'username': user.username}
    )
    refresh_token = create_refresh_token(identity=user.id)
    
    # Log login activity
    log_activity(user.id, 'login', {'username': username})
    
    return {
        'success': True,
        'access_token': access_token,
        'refresh_token': refresh_token,
        'user': user.to_dict()
    }, 200

def log_activity(user_id, activity_type, activity_data=None, ip_address=None):
    """
    Log user activity
    """
    try:
        activity = UserActivity(
            user_id=user_id,
            activity_type=activity_type,
            activity_data=json.dumps(activity_data) if activity_data else None,
            ip_address=ip_address or request.remote_addr if request else None
        )
        db.session.add(activity)
        db.session.commit()
    except Exception as e:
        print(f"Error logging activity: {e}")
        db.session.rollback()

def token_required(f):
    """
    Decorator to require valid JWT token
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            verify_jwt_in_request()
            current_user_id = get_jwt_identity()
            return f(current_user_id=current_user_id, *args, **kwargs)
        except Exception as e:
            return jsonify({'error': 'Authentication required', 'details': str(e)}), 401
    return decorated

def admin_required(f):
    """
    Decorator to require admin role
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            verify_jwt_in_request()
            current_user_id = get_jwt_identity()
            user = User.query.get(current_user_id)
            
            if not user or user.role != 'admin':
                return jsonify({'error': 'Admin access required'}), 403
            
            return f(current_user_id=current_user_id, current_user=user, *args, **kwargs)
        except Exception as e:
            return jsonify({'error': 'Authentication required', 'details': str(e)}), 401
    return decorated

def get_current_user():
    """
    Get current authenticated user
    """
    try:
        verify_jwt_in_request(optional=True)
        user_id = get_jwt_identity()
        if user_id:
            return User.query.get(user_id)
    except:
        pass
    return None
