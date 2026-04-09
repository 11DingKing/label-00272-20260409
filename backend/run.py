"""QDPS 质量数据处理系统 - 启动脚本"""
import os
from app import create_app

app = create_app(os.environ.get('FLASK_ENV', 'development'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
