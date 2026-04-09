"""用户模型"""


class User:
    def __init__(self, user_id, username, display_name, department=None, email=None):
        self.id = user_id
        self.username = username
        self.display_name = display_name
        self.department = department
        self.email = email
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'display_name': self.display_name,
            'department': self.department,
            'email': self.email
        }
    
    @staticmethod
    def from_oa_data(oa_user_data):
        return User(
            user_id=oa_user_data.get('id'),
            username=oa_user_data.get('loginid'),
            display_name=oa_user_data.get('lastname', ''),
            department=oa_user_data.get('departmentname', ''),
            email=oa_user_data.get('email', '')
        )
