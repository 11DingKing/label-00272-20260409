"""产品质量数据对应关系模型"""


class ProductQualityDataRelation:
    def __init__(self, **kwargs):
        self.serial_number = kwargs.get('SerialNumber')
        self.product_number = kwargs.get('ProductNumber')
        self.batch_number = kwargs.get('BatchNumber')
        self.three_motion_meas_data_path = kwargs.get('ThreeMotionMeasDataPath')
        self.four_motion_meas_data_path = kwargs.get('FourMotionMeasDataPath')
        self.five_motion_meas_data_path = kwargs.get('FiveMotionMeasDataPath')
        self.blade_profile_scan_data_path = kwargs.get('BladeProfileScanDataPath')
        self.create_time = kwargs.get('CreateTime')
        self.modify_time = kwargs.get('ModifyTime')
        self.creator = kwargs.get('Creator')
        self.operator = kwargs.get('Operator')
    
    def _format_datetime(self, val):
        """格式化日期时间，支持 datetime 对象和字符串"""
        if val is None:
            return None
        if isinstance(val, str):
            return val
        return val.strftime('%Y-%m-%d %H:%M:%S')
    
    def to_dict(self):
        return {
            'serial_number': self.serial_number,
            'product_number': self.product_number,
            'batch_number': self.batch_number,
            'three_motion_meas_data_path': self.three_motion_meas_data_path,
            'four_motion_meas_data_path': self.four_motion_meas_data_path,
            'five_motion_meas_data_path': self.five_motion_meas_data_path,
            'blade_profile_scan_data_path': self.blade_profile_scan_data_path,
            'create_time': self._format_datetime(self.create_time),
            'modify_time': self._format_datetime(self.modify_time),
            'creator': self.creator,
            'operator': self.operator
        }
    
    @staticmethod
    def from_db_row(row):
        if row is None:
            return None
        return ProductQualityDataRelation(**dict(row))
