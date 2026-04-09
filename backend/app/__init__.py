"""
QDPS 质量数据处理系统 - 后端API
"""
from flask import Flask
from flask_cors import CORS
import os

from config import config_map


def create_app(config_name='default'):
    """创建Flask应用"""
    app = Flask(__name__)
    
    # 加载配置
    app.config.from_object(config_map[config_name])
    
    # 启用CORS
    CORS(app, supports_credentials=True, origins=['*'])
    
    # 确保报告目录存在
    report_path = app.config.get('REPORT_BASE_PATH')
    if report_path and not os.path.exists(report_path):
        os.makedirs(report_path)
    
    # 启动时检测数据库连接
    from app.services.db_service import check_database_connections
    check_database_connections(app)
    
    # 注册蓝图
    from app.routes.auth import auth_bp
    from app.routes.dimension import dimension_bp
    from app.routes.certificate import certificate_bp
    from app.routes.maintenance import maintenance_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(dimension_bp, url_prefix='/api/dimension')
    app.register_blueprint(certificate_bp, url_prefix='/api/certificate')
    app.register_blueprint(maintenance_bp, url_prefix='/api/maintenance')
    
    @app.route('/api/health')
    def health():
        from app.services.db_service import get_db_status
        db_status = get_db_status()
        return {
            'status': 'ok', 
            'service': 'QDPS Backend',
            'mode': '演示模式' if db_status['demo_mode'] else '生产模式',
            'database': db_status
        }
    
    return app
