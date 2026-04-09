"""质量证明单号模型"""


class QualityCertificate:
    """编号规则: QC-XXXXXX(供应商代码)-20XX(年代号)-XXXX(顺序号)"""
    
    def __init__(self, **kwargs):
        self.id = kwargs.get('Id')
        self.certificate_number = kwargs.get('CertificateNumber')
        self.product_number = kwargs.get('ProductNumber')
        self.product_model = kwargs.get('ProductModel')
        self.batch_number = kwargs.get('BatchNumber')
        self.part_number = kwargs.get('PartNumber')
        self.part_name = kwargs.get('PartName')
        self.quantity = kwargs.get('Quantity')
        self.unit = kwargs.get('Unit')
        self.supplier_code = kwargs.get('SupplierCode', '203239')
        self.inspection_date = kwargs.get('InspectionDate')
        self.inspector = kwargs.get('Inspector')
        self.status = kwargs.get('Status', 0)
        self.remark = kwargs.get('Remark')
        self.create_time = kwargs.get('CreateTime')
        self.modify_time = kwargs.get('ModifyTime')
        self.creator = kwargs.get('Creator')
        self.operator = kwargs.get('Operator')
    
    def _format_date(self, val, fmt='%Y-%m-%d'):
        """格式化日期，支持 datetime 对象和字符串"""
        if val is None:
            return None
        if isinstance(val, str):
            return val.split(' ')[0] if fmt == '%Y-%m-%d' else val
        return val.strftime(fmt)
    
    def to_dict(self):
        return {
            'id': self.id,
            'certificate_number': self.certificate_number,
            'product_number': self.product_number,
            'product_model': self.product_model,
            'batch_number': self.batch_number,
            'part_number': self.part_number,
            'part_name': self.part_name,
            'quantity': self.quantity,
            'unit': self.unit,
            'supplier_code': self.supplier_code,
            'inspection_date': self._format_date(self.inspection_date, '%Y-%m-%d'),
            'inspector': self.inspector,
            'status': self.status,
            'status_text': self.get_status_text(),
            'remark': self.remark,
            'create_time': self._format_date(self.create_time, '%Y-%m-%d %H:%M:%S'),
            'modify_time': self._format_date(self.modify_time, '%Y-%m-%d %H:%M:%S'),
            'creator': self.creator,
            'operator': self.operator,
            'form_display': self.get_form_display()
        }
    
    def get_status_text(self):
        status_map = {0: '草稿', 1: '已提交', 2: '已审核'}
        return status_map.get(self.status, '未知')
    
    def get_form_display(self):
        """获取表单显示编号: 表单编号：QC-______-20___-______"""
        if self.certificate_number:
            parts = self.certificate_number.split('-')
            if len(parts) == 4:
                return f"表单编号：QC-{parts[1]}-{parts[2]}-{parts[3]}"
        return "表单编号：QC-______-20___-______"
    
    @staticmethod
    def generate_certificate_number(supplier_code, year, sequence):
        return f"QC-{supplier_code}-{year}-{str(sequence).zfill(4)}"
    
    @staticmethod
    def from_db_row(row):
        if row is None:
            return None
        return QualityCertificate(**dict(row))
