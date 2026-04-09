"""数据库连接服务"""
import pymysql
import pymssql
import socket
from pymysql.cursors import DictCursor
from flask import current_app
from contextlib import contextmanager


# 数据库连接状态（启动时检测）
_db_status = {
    'oa_available': None,      # OA数据库是否可用
    'qdps_available': None,    # QDPS数据库是否可用
    'demo_mode': False         # 是否演示模式
}


def get_db_status():
    """获取数据库状态"""
    return _db_status.copy()


def _check_port(host, port, timeout=0.5):
    """快速检测端口是否可达"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except Exception:
        return False


def check_database_connections(app):
    """启动时检测数据库连接（快速检测）"""
    print("\n" + "=" * 50, flush=True)
    print("检测数据库连接...", flush=True)
    print("=" * 50, flush=True)
    
    oa_config = app.config['OA_DB_CONFIG']
    qdps_config = app.config['QDPS_DB_CONFIG']
    oa_host = oa_config['host']
    qdps_host = qdps_config['host']
    
    # 检测 OA 数据库（端口 + 实际连接）
    print(f"检测 OA ({oa_host}:3306)...", end=" ", flush=True)
    if not _check_port(oa_host, 3306, timeout=0.5):
        _db_status['oa_available'] = False
        print("端口不可达", flush=True)
    else:
        # 端口可达，尝试实际连接
        try:
            conn = pymysql.connect(
                host=oa_config['host'],
                user=oa_config['user'],
                password=oa_config['password'],
                database=oa_config['database'],
                connect_timeout=2,
                read_timeout=2
            )
            conn.ping()
            conn.close()
            _db_status['oa_available'] = True
            print("连接成功", flush=True)
        except Exception as e:
            _db_status['oa_available'] = False
            print(f"失败", flush=True)
    
    # OA 不可用则直接进入演示模式，跳过 QDPS 检测
    if not _db_status['oa_available']:
        _db_status['demo_mode'] = True
        _db_status['qdps_available'] = False
        print(f"跳过 QDPS 检测（OA 不可用）", flush=True)
        print("\n>>> 启用【演示模式】", flush=True)
        print("    测试账号: admin/admin123, test/test123", flush=True)
        print("=" * 50 + "\n", flush=True)
        return _db_status
    
    # OA 可用时才检测 QDPS（只检测端口，不实际连接）
    print(f"检测 QDPS ({qdps_host}:1433)...", end=" ", flush=True)
    if _check_port(qdps_host, 1433, timeout=0.5):
        _db_status['qdps_available'] = True
        print("端口可达", flush=True)
    else:
        _db_status['qdps_available'] = False
        print("端口不可达", flush=True)
    
    _db_status['demo_mode'] = False
    print("\n>>> 启用【生产模式】", flush=True)
    print("=" * 50 + "\n", flush=True)
    return _db_status


class DatabaseService:
    @staticmethod
    @contextmanager
    def get_oa_connection():
        """获取OA系统数据库连接（MySQL）"""
        config = current_app.config['OA_DB_CONFIG']
        connection = None
        try:
            connection = pymysql.connect(
                host=config['host'],
                user=config['user'],
                password=config['password'],
                database=config['database'],
                charset=config.get('charset', 'utf8mb4'),
                cursorclass=DictCursor,
                connect_timeout=3,  # 连接超时3秒
                read_timeout=5      # 读取超时5秒
            )
            yield connection
        finally:
            if connection:
                connection.close()
    
    @staticmethod
    @contextmanager
    def get_qdps_connection():
        """获取QDPS数据库连接（SQL Server）"""
        config = current_app.config['QDPS_DB_CONFIG']
        connection = None
        try:
            connection = pymssql.connect(
                server=config['host'],
                user=config['user'],
                password=config['password'],
                database=config['database'],
                charset='utf8',
                as_dict=True,
                login_timeout=3,  # 登录超时3秒
                timeout=5         # 查询超时5秒
            )
            yield connection
        finally:
            if connection:
                connection.close()
    
    @staticmethod
    def execute_qdps_query(sql, params=None, fetch_one=False):
        """执行QDPS数据库查询"""
        with DatabaseService.get_qdps_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, params or ())
            if fetch_one:
                return cursor.fetchone()
            return cursor.fetchall()
    
    @staticmethod
    def execute_qdps_command(sql, params=None):
        """执行QDPS数据库命令"""
        with DatabaseService.get_qdps_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, params or ())
            conn.commit()
            return cursor.rowcount
    
    @staticmethod
    def execute_oa_query(sql, params=None, fetch_one=False):
        """执行OA数据库查询"""
        with DatabaseService.get_oa_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, params or ())
            if fetch_one:
                return cursor.fetchone()
            return cursor.fetchall()
