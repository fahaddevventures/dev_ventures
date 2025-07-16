from functools import wraps
from flask import jsonify
from flask_login import current_user, login_required

def role_required(*roles):
    def decorator(f):
        @wraps(f)
        @login_required
        def decorated_function(*args, **kwargs):
            if current_user.role not in roles:
                allowed_roles = [role.value for role in roles]
                return jsonify({
                    "error": "Access denied",
                    "message": f"Your role '{current_user.role.value}' is not allowed. Required: {allowed_roles}"
                }), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator
