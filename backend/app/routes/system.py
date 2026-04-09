"""系统路由 - 模块管理和操作日志"""
from flask import Blueprint, request, jsonify, g
from app.routes.auth import login_required
from datetime import datetime

system_bp = Blueprint('system', __name__)

# 模块列表配置
MODULES = [
    {
        'path': '/dimension/three',
        'title': '三动全尺寸判定',
        'desc': '对三动产品进行全尺寸测量数据判定分析',
        'icon': 'DataLine',
        'gradient': 'linear-gradient(135deg, #3b82f6, #1d4ed8)',
        'enabled': True
    },
    {
        'path': '/dimension/four',
        'title': '四动全尺寸判定',
        'desc': '对四动产品进行全尺寸测量数据判定分析',
        'icon': 'DataLine',
        'gradient': 'linear-gradient(135deg, #8b5cf6, #6d28d9)',
        'enabled': True
    },
    {
        'path': '/dimension/five',
        'title': '五动全尺寸判定',
        'desc': '对五动产品进行全尺寸测量数据判定分析',
        'icon': 'DataLine',
        'gradient': 'linear-gradient(135deg, #ec4899, #be185d)',
        'enabled': True
    },
    {
        'path': '/certificate',
        'title': '质量证明单号',
        'desc': '管理和生成质量证明单号文档',
        'icon': 'Document',
        'gradient': 'linear-gradient(135deg, #10b981, #059669)',
        'enabled': True
    },
    {
        'path': '/maintenance/product-quality',
        'title': '产品检测数据维护',
        'desc': '维护产品质量数据对应关系',
        'icon': 'Coin',
        'gradient': 'linear-gradient(135deg, #f59e0b, #d97706)',
        'enabled': True
    },
    {
        'path': '/maintenance/report-path',
        'title': '报告路径维护',
        'desc': '配置系统生成报告的存储位置',
        'icon': 'FolderOpened',
        'gradient': 'linear-gradient(135deg, #6366f1, #4338ca)',
        'enabled': True
    }
]

# 模拟操作日志存储
operation_logs = []

def add_log(action, module, message, details=None):
    """添加操作日志"""
    log = {
        'id': len(operation_logs) + 1,
        'user_id': g.current_user.id if hasattr(g, 'current_user') else None,
        'user_name': g.current_user.display_name if hasattr(g, 'current_user') else '系统',
        'action': action,
        'module': module,
        'message': message,
        'details': details,
        'created_at': datetime.now().isoformat()
    }
    operation_logs.insert(0, log)
    # 只保留最近100条日志
    if len(operation_logs) > 100:
        operation_logs.pop()


@system_bp.route('/modules', methods=['GET'])
@login_required
def get_modules():
    """获取模块列表"""
    return jsonify({
        'success': True,
        'data': MODULES
    })


@system_bp.route('/logs/recent', methods=['GET'])
@login_required
def get_recent_logs():
    """获取最近50条操作日志"""
    # 返回最近50条日志，按时间倒序
    recent_logs = operation_logs[:50]
    return jsonify({
        'success': True,
        'data': recent_logs
    })


@system_bp.route('/logs', methods=['POST'])
@login_required
def create_log():
    """创建操作日志"""
    data = request.get_json()
    action = data.get('action', '操作')
    module = data.get('module', '')
    message = data.get('message', '')
    details = data.get('details')
    
    add_log(action, module, message, details)
    
    return jsonify({
        'success': True,
        'message': '日志记录成功'
    })
