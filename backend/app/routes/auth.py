"""认证路由"""
from functools import wraps
from flask import Blueprint, request, jsonify, g
from app.services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__)


def login_required(f):
    """登录验证装饰器"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if not token:
            return jsonify({'success': False, 'message': '请先登录'}), 401
        
        user = AuthService.verify_token(token)
        if not user:
            return jsonify({'success': False, 'message': '登录已过期，请重新登录'}), 401
        
        g.current_user = user
        return f(*args, **kwargs)
    return decorated


@auth_bp.route('/login', methods=['POST'])
def login():
    """登录"""
    data = request.get_json()
    username = data.get('username', '').strip()
    password = data.get('password', '')
    
    if not username or not password:
        return jsonify({'success': False, 'message': '请输入用户名和密码'})
    
    user = AuthService.authenticate(username, password)
    if not user:
        return jsonify({'success': False, 'message': '用户名或密码错误'})
    
    token = AuthService.generate_token(user)
    
    return jsonify({
        'success': True,
        'message': '登录成功',
        'data': {
            'token': token,
            'user': user.to_dict()
        }
    })


@auth_bp.route('/userinfo', methods=['GET'])
@login_required
def userinfo():
    """获取当前用户信息"""
    return jsonify({
        'success': True,
        'data': g.current_user.to_dict()
    })


@auth_bp.route('/verify', methods=['GET'])
@login_required
def verify():
    """验证token是否有效"""
    return jsonify({'success': True, 'message': 'Token有效'})


@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    """退出登录"""
    return jsonify({'success': True, 'message': '退出成功'})
