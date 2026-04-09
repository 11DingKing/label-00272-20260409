"""质量证明单路由"""
from flask import Blueprint, request, jsonify, g
from app.routes.auth import login_required
from app.services.certificate_service import CertificateService

certificate_bp = Blueprint('certificate', __name__)


@certificate_bp.route('/list', methods=['GET'])
@login_required
def get_list():
    """获取质量证明单列表"""
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 20, type=int)
    
    filters = {
        'certificate_number': request.args.get('certificate_number'),
        'batch_number': request.args.get('batch_number'),
        'product_number': request.args.get('product_number'),
        'status': request.args.get('status', type=int)
    }
    filters = {k: v for k, v in filters.items() if v is not None and v != ''}
    
    result = CertificateService.get_certificate_list(page, page_size, filters)
    return jsonify({'success': True, 'data': result})


@certificate_bp.route('/detail/<int:certificate_id>', methods=['GET'])
@login_required
def get_detail(certificate_id):
    """获取质量证明单详情"""
    certificate = CertificateService.get_certificate_by_id(certificate_id)
    if certificate:
        return jsonify({'success': True, 'data': certificate.to_dict()})
    return jsonify({'success': False, 'message': '未找到记录'})


@certificate_bp.route('/generate-number', methods=['GET'])
@login_required
def generate_number():
    """生成新的证明单号"""
    certificate_number = CertificateService.generate_certificate_number()
    return jsonify({
        'success': True,
        'data': {
            'certificate_number': certificate_number,
            'form_display': f"表单编号：{certificate_number}"
        }
    })


@certificate_bp.route('/create', methods=['POST'])
@login_required
def create():
    """创建质量证明单"""
    data = request.get_json()
    
    if not data.get('product_number') or not data.get('batch_number'):
        return jsonify({'success': False, 'message': '产品号和批次号不能为空'})
    
    result = CertificateService.create_certificate(data, g.current_user.display_name)
    return jsonify(result)


@certificate_bp.route('/update/<int:certificate_id>', methods=['PUT'])
@login_required
def update(certificate_id):
    """更新质量证明单"""
    data = request.get_json()
    result = CertificateService.update_certificate(certificate_id, data, g.current_user.display_name)
    return jsonify(result)


@certificate_bp.route('/delete/<int:certificate_id>', methods=['DELETE'])
@login_required
def delete(certificate_id):
    """删除质量证明单"""
    result = CertificateService.delete_certificate(certificate_id)
    return jsonify(result)


@certificate_bp.route('/submit/<int:certificate_id>', methods=['POST'])
@login_required
def submit(certificate_id):
    """提交质量证明单"""
    result = CertificateService.submit_certificate(certificate_id, g.current_user.display_name)
    return jsonify(result)
