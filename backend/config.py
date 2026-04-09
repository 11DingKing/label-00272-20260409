"""
QDPS 质量数据处理系统 - 配置文件
"""
import os
from datetime import timedelta

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'qdps-secret-key-2024-quality-data'
    PERMANENT_SESSION_LIFETIME = timedelta(hours=8)
    REPORT_BASE_PATH = os.environ.get('REPORT_BASE_PATH') or os.path.join(BASE_DIR, 'reports')
    
    # OA系统数据库配置（登录认证）
    OA_DB_CONFIG = {
        'host': os.environ.get('OA_DB_HOST', '192.168.6.88'),
        'user': os.environ.get('OA_DB_USER', 'sangfor'),
        'password': os.environ.get('OA_DB_PASSWORD', 'Xrac123.com'),
        'database': os.environ.get('OA_DB_NAME', 'ecology'),
        'charset': 'utf8mb4'
    }
    
    # QDPS 质量数据处理系统数据库配置（SQL Server）
    QDPS_DB_CONFIG = {
        'host': os.environ.get('QDPS_DB_HOST', '192.168.6.88'),
        'user': os.environ.get('QDPS_DB_USER', 'qdsp'),
        'password': os.environ.get('QDPS_DB_PASSWORD', 'Xrac123.com'),
        'database': os.environ.get('QDPS_DB_NAME', 'qdps'),
    }
    
    # MES系统数据库配置
    MES_DB_CONFIG = {
        'host': os.environ.get('MES_DB_HOST', '192.168.6.91'),
        'user': os.environ.get('MES_DB_USER', 'caxa_readonly'),
        'password': os.environ.get('MES_DB_PASSWORD', 'Read@123.com'),
        'database': os.environ.get('MES_DB_NAME', 'caxa_science_mes'),
        'charset': 'utf8mb4'
    }
    
    SUPPLIER_CODE = '203239'


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config_map = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
