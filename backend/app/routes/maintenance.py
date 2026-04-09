"""基础数据维护路由"""
from flask import Blueprint, request, jsonify, g
from app.routes.auth import login_required
from app.services.maintenance_service import MaintenanceService

maintenance_bp = Blueprint('maintenance', __name__)


# ===== 产品检测数据维护 =====
@maintenance_bp.route('/product-quality/list', methods=['GET'])
@login_required
def product_quality_list():
    """获取产品检测数据列表"""
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 20, type=int)
    
    filters = {
        'product_number': request.args.get('product_number'),
        'batch_number': request.args.get('batch_number')
    }
    filters = {k: v for k, v in filters.items() if v}
    
    result = MaintenanceService.get_product_quality_list(page, page_size, filters)
    return jsonify({'success': True, 'data': result})


@maintenance_bp.route('/product-quality/<int:serial_number>', methods=['GET'])
@login_required
def product_quality_detail(serial_number):
    """获取产品检测数据详情"""
    data = MaintenanceService.get_product_quality_by_id(serial_number)
    if data:
        return jsonify({'success': True, 'data': data.to_dict()})
    return jsonify({'success': False, 'message': '未找到记录'})


@maintenance_bp.route('/product-quality/create', methods=['POST'])
@login_required
def product_quality_create():
    """创建产品检测数据"""
    data = request.get_json()
    
    if not data.get('product_number') or not data.get('batch_number'):
        return jsonify({'success': False, 'message': '产品号和批次号不能为空'})
    
    result = MaintenanceService.create_product_quality(data, g.current_user.display_name)
    return jsonify(result)


@maintenance_bp.route('/product-quality/<int:serial_number>', methods=['PUT'])
@login_required
def product_quality_update(serial_number):
    """更新产品检测数据"""
    data = request.get_json()
    result = MaintenanceService.update_product_quality(serial_number, data, g.current_user.display_name)
    return jsonify(result)


@maintenance_bp.route('/product-quality/<int:serial_number>', methods=['DELETE'])
@login_required
def product_quality_delete(serial_number):
    """删除产品检测数据"""
    result = MaintenanceService.delete_product_quality(serial_number)
    return jsonify(result)


# ===== 报告路径维护 =====
@maintenance_bp.route('/report-path', methods=['GET'])
@login_required
def get_report_path():
    """获取报告路径"""
    path = MaintenanceService.get_report_path()
    return jsonify({'success': True, 'data': {'path': path}})


@maintenance_bp.route('/report-path', methods=['PUT'])
@login_required
def update_report_path():
    """更新报告路径"""
    data = request.get_json()
    path = data.get('path')
    
    if not path:
        return jsonify({'success': False, 'message': '路径不能为空'})
    
    result = MaintenanceService.update_report_path(path, g.current_user.display_name)
    return jsonify(result)


# ===== 系统配置 =====
@maintenance_bp.route('/configs', methods=['GET'])
@login_required
def get_configs():
    """获取所有系统配置"""
    configs = MaintenanceService.get_all_configs()
    return jsonify({'success': True, 'data': configs})
