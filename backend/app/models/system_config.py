"""系统配置模型"""


class SystemConfig:
    def __init__(self, **kwargs):
        self.id = kwargs.get('Id')
        self.config_key = kwargs.get('ConfigKey')
        self.config_value = kwargs.get('ConfigValue')
        self.config_type = kwargs.get('ConfigType')
        self.description = kwargs.get('Description')
        self.create_time = kwargs.get('CreateTime')
        self.modify_time = kwargs.get('ModifyTime')
        self.operator = kwargs.get('Operator')
    
    def to_dict(self):
        return {
            'id': self.id,
            'config_key': self.config_key,
            'config_value': self.config_value,
            'config_type': self.config_type,
            'description': self.description,
            'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S') if self.create_time else None,
            'modify_time': self.modify_time.strftime('%Y-%m-%d %H:%M:%S') if self.modify_time else None,
            'operator': self.operator
        }
    
    @staticmethod
    def from_db_row(row):
        if row is None:
            return None
        return SystemConfig(**dict(row))
