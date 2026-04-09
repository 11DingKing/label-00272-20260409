"""认证服务"""
import hashlib
import jwt
import os
from datetime import datetime, timedelta
from flask import current_app
from app.services.db_service import DatabaseService, get_db_status
from app.models.user import User


# 演示模式内置测试账号
DEMO_USERS = {
    'admin': {
        'id': 1,
        'loginid': 'admin',
        'lastname': '管理员',
        'password': 'admin123',
        'departmentname': '质量部',
        'email': 'admin@qdps.local'
    },
    'test': {
        'id': 2,
        'loginid': 'test',
        'lastname': '测试用户',
        'password': 'test123',
        'departmentname': '测试部',
        'email': 'test@qdps.local'
    }
}


class AuthService:
    @staticmethod
    def authenticate(username, password):
        """用户认证"""
        db_status = get_db_status()
        
        # 如果是演示模式，直接使用内置账号
        if db_status['demo_mode']:
            return AuthService._demo_authenticate(username, password)
        
        # 尝试 OA 数据库认证
        try:
            sql = """
                SELECT 
                    h.id, h.loginid, h.lastname, h.password,
                    d.departmentname, h.email
                FROM HrmResource h
                LEFT JOIN HrmDepartment d ON h.departmentid = d.id
                WHERE h.loginid = %s AND h.status = 1
            """
            user_data = DatabaseService.execute_oa_query(sql, (username,), fetch_one=True)
            
            if user_data:
                if AuthService._verify_password(password, user_data.get('password', '')):
                    return User.from_oa_data(user_data)
                return None
        except Exception as e:
            print(f"OA数据库查询失败: {str(e)}")
        
        # 回退到演示模式
        return AuthService._demo_authenticate(username, password)
    
    @staticmethod
    def _demo_authenticate(username, password):
        """演示模式认证"""
        demo_user = DEMO_USERS.get(username)
        if demo_user and demo_user['password'] == password:
            return User.from_oa_data(demo_user)
        return None
    
    @staticmethod
    def _verify_password(input_password, stored_password):
        """验证密码"""
        if input_password == stored_password:
            return True
        
        md5_hash = hashlib.md5(input_password.encode()).hexdigest()
        if md5_hash == stored_password or md5_hash.upper() == stored_password:
            return True
        
        sha1_hash = hashlib.sha1(input_password.encode()).hexdigest()
        if sha1_hash == stored_password or sha1_hash.upper() == stored_password:
            return True
        
        return False
    
    @staticmethod
    def generate_token(user):
        """生成JWT Token"""
        payload = {
            'user_id': user.id,
            'username': user.username,
            'display_name': user.display_name,
            'department': user.department,
            'exp': datetime.utcnow() + timedelta(hours=8)
        }
        return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
    
    @staticmethod
    def verify_token(token):
        """验证JWT Token"""
        try:
            payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            return User(
                user_id=payload['user_id'],
                username=payload['username'],
                display_name=payload['display_name'],
                department=payload.get('department')
            )
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    @staticmethod
    def get_user_by_id(user_id):
        """根据ID获取用户"""
        try:
            sql = """
                SELECT h.id, h.loginid, h.lastname, d.departmentname, h.email
                FROM HrmResource h
                LEFT JOIN HrmDepartment d ON h.departmentid = d.id
                WHERE h.id = %s AND h.status = 1
            """
            user_data = DatabaseService.execute_oa_query(sql, (user_id,), fetch_one=True)
            if user_data:
                return User.from_oa_data(user_data)
            return None
        except:
            return None
