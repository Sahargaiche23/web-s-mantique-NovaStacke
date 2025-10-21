"""
Database models for authentication and activity tracking
"""
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime
import json

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model):
    """User model with role-based access control"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='voyageur')  # 'voyageur' or 'admin'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    activities = db.relationship('UserActivity', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        """Verify password"""
        return bcrypt.check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """Convert user to dictionary"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'is_active': self.is_active
        }

class UserActivity(db.Model):
    """Track user activities for analytics"""
    __tablename__ = 'user_activities'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    activity_type = db.Column(db.String(50), nullable=False)  # 'login', 'sparql_query', 'recommendation', 'search'
    activity_data = db.Column(db.Text)  # JSON data with details
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    ip_address = db.Column(db.String(50))
    
    def to_dict(self):
        """Convert activity to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'username': self.user.username if self.user else None,
            'activity_type': self.activity_type,
            'activity_data': json.loads(self.activity_data) if self.activity_data else {},
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'ip_address': self.ip_address
        }

class Recommendation(db.Model):
    """Store generated recommendations for analytics"""
    __tablename__ = 'recommendations'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    recommendation_type = db.Column(db.String(50))  # 'destination', 'accommodation', 'activity', 'transport'
    recommendation_data = db.Column(db.Text)  # JSON with recommendation details
    eco_score = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert recommendation to dictionary"""
        # Get username
        username = 'Anonymous'
        if self.user_id:
            user = User.query.get(self.user_id)
            if user:
                username = user.username
        
        return {
            'id': self.id,
            'user_id': self.user_id,
            'username': username,
            'recommendation_type': self.recommendation_type,
            'recommendation_data': json.loads(self.recommendation_data) if self.recommendation_data else {},
            'eco_score': self.eco_score,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class DestinationView(db.Model):
    """Track destination views for popularity analytics"""
    __tablename__ = 'destination_views'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    destination_name = db.Column(db.String(200))
    view_count = db.Column(db.Integer, default=1)
    last_viewed = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'destination_name': self.destination_name,
            'view_count': self.view_count,
            'last_viewed': self.last_viewed.isoformat() if self.last_viewed else None
        }

class SPARQLQuery(db.Model):
    """Track SPARQL queries for analytics"""
    __tablename__ = 'sparql_queries'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    query_text = db.Column(db.Text)
    query_type = db.Column(db.String(20))  # 'SELECT', 'INSERT', 'DELETE', 'UPDATE'
    results_count = db.Column(db.Integer, default=0)
    success = db.Column(db.Boolean, default=True)
    error_message = db.Column(db.Text)
    execution_time = db.Column(db.Float)  # in seconds
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert to dictionary"""
        username = 'Anonymous'
        if self.user_id:
            user = User.query.get(self.user_id)
            if user:
                username = user.username
        
        return {
            'id': self.id,
            'user_id': self.user_id,
            'username': username,
            'query_text': self.query_text,
            'query_type': self.query_type,
            'results_count': self.results_count,
            'success': self.success,
            'error_message': self.error_message,
            'execution_time': self.execution_time,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
