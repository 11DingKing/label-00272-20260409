"""尺寸判定路由"""
from flask import Blueprint, request, jsonify, send_file, g, current_app
import os
from app.routes.auth import login_required
from app.services.dimension_service import DimensionCheckService

dimension_bp = Blueprint('dimension', __name__)


@dimension_bp.route('/batch-numbers', methods=['GET'])
@login_required
def get_batch_numbers():
    """获取批次号列表"""
    batch_numbers = DimensionCheckService.get_batch_numbers()
    return jsonify({'success': True, 'data': batch_numbers})


@dimension_bp.route('/batch-info/<batch_number>', methods=['GET'])
@login_required
def get_batch_info(batch_number):
    """获取批次信息"""
    info = DimensionCheckService.get_batch_info(batch_number)
    if info:
        return jsonify({'success': True, 'data': info})
    return jsonify({'success': False, 'message': '未找到批次信息'})


@dimension_bp.route('/check/three-motion', methods=['POST'])
@login_required
def check_three_motion():
    """三动全尺寸判定"""
    data = request.get_json()
    batch_number = data.get('batch_number')
    
    if not batch_number:
        return jsonify({'success': False, 'message': '请选择批次号'})
    
    result = DimensionCheckService.check_motion(
        batch_number=batch_number,
        motion_type='三动',
        operator=g.current_user.display_name
    )
    return jsonify(result)


@dimension_bp.route('/check/four-motion', methods=['POST'])
@login_required
def check_four_motion():
    """四动全尺寸判定"""
    data = request.get_json()
    batch_number = data.get('batch_number')
    
    if not batch_number:
        return jsonify({'success': False, 'message': '请选择批次号'})
    
    result = DimensionCheckService.check_motion(
        batch_number=batch_number,
        motion_type='四动',
        operator=g.current_user.display_name
    )
    return jsonify(result)


@dimension_bp.route('/check/five-motion', methods=['POST'])
@login_required
def check_five_motion():
    """五动全尺寸判定"""
    data = request.get_json()
    batch_number = data.get('batch_number')
    
    if not batch_number:
        return jsonify({'success': False, 'message': '请选择批次号'})
    
    result = DimensionCheckService.check_motion(
        batch_number=batch_number,
        motion_type='五动',
        operator=g.current_user.display_name
    )
    return jsonify(result)


@dimension_bp.route('/download/<filename>', methods=['GET'])
@login_required
def download_report(filename):
    """下载判定报告"""
    report_path = current_app.config.get('REPORT_BASE_PATH', 'reports')
    file_path = os.path.join(report_path, filename)
    
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    
    return jsonify({'success': False, 'message': '文件不存在'}), 404
