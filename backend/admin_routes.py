"""
Admin panel routes for user management and analytics
"""
from flask import Blueprint, jsonify, request
from models import db, User, UserActivity, Recommendation, DestinationView
from auth import admin_required, log_activity
from sqlalchemy import func, desc
from datetime import datetime, timedelta
import json

admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')

# ==================== USER MANAGEMENT ====================

@admin_bp.route('/users', methods=['GET'])
@admin_required
def get_all_users(current_user_id, current_user):
    """Get all users with filtering"""
    # Get query parameters
    role_filter = request.args.get('role')
    search = request.args.get('search')
    active_only = request.args.get('active_only', 'false').lower() == 'true'
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 50))
    
    # Build query
    query = User.query
    
    if role_filter:
        query = query.filter_by(role=role_filter)
    
    if search:
        query = query.filter(
            (User.username.ilike(f'%{search}%')) |
            (User.email.ilike(f'%{search}%'))
        )
    
    if active_only:
        query = query.filter_by(is_active=True)
    
    # Order by creation date
    query = query.order_by(desc(User.created_at))
    
    # Paginate
    paginated = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'success': True,
        'users': [user.to_dict() for user in paginated.items],
        'total': paginated.total,
        'pages': paginated.pages,
        'current_page': page
    })

@admin_bp.route('/users/<int:user_id>', methods=['GET'])
@admin_required
def get_user_details(current_user_id, current_user, user_id):
    """Get detailed user information"""
    user = User.query.get_or_404(user_id)
    
    # Get user statistics
    total_activities = UserActivity.query.filter_by(user_id=user_id).count()
    total_logins = UserActivity.query.filter_by(user_id=user_id, activity_type='login').count()
    total_queries = UserActivity.query.filter_by(user_id=user_id, activity_type='sparql_query').count()
    total_recommendations = Recommendation.query.filter_by(user_id=user_id).count()
    
    # Recent activities
    recent_activities = UserActivity.query.filter_by(user_id=user_id)\
        .order_by(desc(UserActivity.timestamp))\
        .limit(10).all()
    
    return jsonify({
        'success': True,
        'user': user.to_dict(),
        'statistics': {
            'total_activities': total_activities,
            'total_logins': total_logins,
            'total_queries': total_queries,
            'total_recommendations': total_recommendations
        },
        'recent_activities': [activity.to_dict() for activity in recent_activities]
    })

@admin_bp.route('/users', methods=['POST'])
@admin_required
def create_user(current_user_id, current_user):
    """Create a new user"""
    data = request.json
    
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role', 'voyageur')
    
    if not all([username, email, password]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Check if user exists
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists'}), 400
    
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already exists'}), 400
    
    # Create user
    user = User(username=username, email=email, role=role)
    user.set_password(password)
    
    try:
        db.session.add(user)
        db.session.commit()
        
        # Log activity
        log_activity(current_user_id, 'admin_create_user', {
            'created_user_id': user.id,
            'username': username
        })
        
        return jsonify({
            'success': True,
            'message': 'User created successfully',
            'user': user.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/users/<int:user_id>', methods=['PUT'])
@admin_required
def update_user(current_user_id, current_user, user_id):
    """Update user information"""
    user = User.query.get_or_404(user_id)
    data = request.json
    
    # Update fields
    if 'username' in data:
        # Check if username is taken
        existing = User.query.filter_by(username=data['username']).first()
        if existing and existing.id != user_id:
            return jsonify({'error': 'Username already exists'}), 400
        user.username = data['username']
    
    if 'email' in data:
        # Check if email is taken
        existing = User.query.filter_by(email=data['email']).first()
        if existing and existing.id != user_id:
            return jsonify({'error': 'Email already exists'}), 400
        user.email = data['email']
    
    if 'role' in data and data['role'] in ['voyageur', 'admin']:
        user.role = data['role']
    
    if 'is_active' in data:
        user.is_active = bool(data['is_active'])
    
    if 'password' in data and data['password']:
        user.set_password(data['password'])
    
    try:
        db.session.commit()
        
        # Log activity
        log_activity(current_user_id, 'admin_update_user', {
            'updated_user_id': user_id,
            'changes': list(data.keys())
        })
        
        return jsonify({
            'success': True,
            'message': 'User updated successfully',
            'user': user.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/users/<int:user_id>', methods=['DELETE'])
@admin_required
def delete_user(current_user_id, current_user, user_id):
    """Delete a user"""
    if user_id == current_user_id:
        return jsonify({'error': 'Cannot delete your own account'}), 400
    
    user = User.query.get_or_404(user_id)
    
    try:
        # Log before deletion
        log_activity(current_user_id, 'admin_delete_user', {
            'deleted_user_id': user_id,
            'username': user.username
        })
        
        db.session.delete(user)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'User deleted successfully'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# ==================== DASHBOARD STATISTICS ====================

@admin_bp.route('/dashboard/stats', methods=['GET'])
@admin_required
def get_dashboard_stats(current_user_id, current_user):
    """Get comprehensive dashboard statistics"""
    
    # User statistics
    total_users = User.query.count()
    active_users = User.query.filter_by(is_active=True).count()
    admin_count = User.query.filter_by(role='admin').count()
    voyageur_count = User.query.filter_by(role='voyageur').count()
    
    # Activity statistics
    total_activities = UserActivity.query.count()
    total_logins = UserActivity.query.filter_by(activity_type='login').count()
    total_sparql_queries = UserActivity.query.filter_by(activity_type='sparql_query').count()
    total_searches = UserActivity.query.filter_by(activity_type='search').count()
    
    # Recommendation statistics
    total_recommendations = Recommendation.query.count()
    avg_eco_score = db.session.query(func.avg(Recommendation.eco_score))\
        .filter(Recommendation.eco_score.isnot(None)).scalar() or 0
    
    # Top destinations
    top_destinations = db.session.query(
        DestinationView.destination_name,
        func.sum(DestinationView.view_count).label('total_views')
    ).group_by(DestinationView.destination_name)\
     .order_by(desc('total_views'))\
     .limit(10).all()
    
    # Recent users (last 30 days)
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    new_users_30d = User.query.filter(User.created_at >= thirty_days_ago).count()
    
    # Daily activity (last 7 days)
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    daily_activity = db.session.query(
        func.date(UserActivity.timestamp).label('date'),
        func.count(UserActivity.id).label('count')
    ).filter(UserActivity.timestamp >= seven_days_ago)\
     .group_by(func.date(UserActivity.timestamp))\
     .order_by('date').all()
    
    return jsonify({
        'success': True,
        'users': {
            'total': total_users,
            'active': active_users,
            'admins': admin_count,
            'voyageurs': voyageur_count,
            'new_last_30d': new_users_30d
        },
        'activities': {
            'total': total_activities,
            'logins': total_logins,
            'sparql_queries': total_sparql_queries,
            'searches': total_searches
        },
        'recommendations': {
            'total': total_recommendations,
            'avg_eco_score': round(float(avg_eco_score), 2)
        },
        'top_destinations': [
            {'name': dest, 'views': views}
            for dest, views in top_destinations
        ],
        'daily_activity': [
            {'date': str(date), 'count': count}
            for date, count in daily_activity
        ]
    })

@admin_bp.route('/dashboard/user-distribution', methods=['GET'])
@admin_required
def get_user_distribution(current_user_id, current_user):
    """Get user distribution by role"""
    distribution = db.session.query(
        User.role,
        func.count(User.id).label('count')
    ).group_by(User.role).all()
    
    return jsonify({
        'success': True,
        'distribution': [
            {'role': role, 'count': count}
            for role, count in distribution
        ]
    })

@admin_bp.route('/dashboard/activity-timeline', methods=['GET'])
@admin_required
def get_activity_timeline(current_user_id, current_user):
    """Get activity timeline"""
    days = int(request.args.get('days', 30))
    start_date = datetime.utcnow() - timedelta(days=days)
    
    activities = db.session.query(
        func.date(UserActivity.timestamp).label('date'),
        UserActivity.activity_type,
        func.count(UserActivity.id).label('count')
    ).filter(UserActivity.timestamp >= start_date)\
     .group_by(func.date(UserActivity.timestamp), UserActivity.activity_type)\
     .order_by('date').all()
    
    return jsonify({
        'success': True,
        'timeline': [
            {
                'date': str(date),
                'activity_type': activity_type,
                'count': count
            }
            for date, activity_type, count in activities
        ]
    })

# ==================== USER ACTIVITY HISTORY ====================

@admin_bp.route('/users/<int:user_id>/activities', methods=['GET'])
@admin_required
def get_user_activities(current_user_id, current_user, user_id):
    """Get user activity history with filtering"""
    activity_type = request.args.get('type')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 50))
    
    query = UserActivity.query.filter_by(user_id=user_id)
    
    if activity_type:
        query = query.filter_by(activity_type=activity_type)
    
    if start_date:
        query = query.filter(UserActivity.timestamp >= datetime.fromisoformat(start_date))
    
    if end_date:
        query = query.filter(UserActivity.timestamp <= datetime.fromisoformat(end_date))
    
    query = query.order_by(desc(UserActivity.timestamp))
    paginated = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'success': True,
        'activities': [activity.to_dict() for activity in paginated.items],
        'total': paginated.total,
        'pages': paginated.pages,
        'current_page': page
    })

# ==================== RECOMMENDATIONS ANALYTICS ====================

@admin_bp.route('/recommendations', methods=['GET'])
@admin_required
def get_all_recommendations(current_user_id, current_user):
    """Get all recommendations with filtering"""
    rec_type = request.args.get('type')
    min_eco_score = request.args.get('min_eco_score')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 50))
    
    query = Recommendation.query
    
    if rec_type:
        query = query.filter_by(recommendation_type=rec_type)
    
    if min_eco_score:
        query = query.filter(Recommendation.eco_score >= float(min_eco_score))
    
    query = query.order_by(desc(Recommendation.created_at))
    paginated = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'success': True,
        'recommendations': [rec.to_dict() for rec in paginated.items],
        'total': paginated.total,
        'pages': paginated.pages,
        'current_page': page
    })
