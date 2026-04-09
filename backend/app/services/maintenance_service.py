"""基础数据维护服务"""
from flask import current_app
from app.services.db_service import DatabaseService, get_db_status
from app.models.product_quality import ProductQualityDataRelation
from app.models.system_config import SystemConfig


# 演示模式模拟数据
DEMO_PRODUCT_QUALITY = [
    {
        'SerialNumber': 1, 'ProductNumber': 'WZ-001', 'BatchNumber': 'WZ20260115-001',
        'ThreeMotionMeasDataPath': '/mnt/data/measure/three/WZ20260115-001',
        'FourMotionMeasDataPath': '/mnt/data/measure/four/WZ20260115-001',
        'FiveMotionMeasDataPath': '/mnt/data/measure/five/WZ20260115-001',
        'BladeProfileScanDataPath': '/mnt/data/scan/blade/WZ20260115-001',
        'CreateTime': '2026-01-15 08:30:00', 'Creator': 'admin'
    },
    {
        'SerialNumber': 2, 'ProductNumber': 'WZ-002', 'BatchNumber': 'WZ20260115-002',
        'ThreeMotionMeasDataPath': '/mnt/data/measure/three/WZ20260115-002',
        'FourMotionMeasDataPath': '/mnt/data/measure/four/WZ20260115-002',
        'FiveMotionMeasDataPath': None,
        'BladeProfileScanDataPath': '/mnt/data/scan/blade/WZ20260115-002',
        'CreateTime': '2026-01-15 13:45:00', 'Creator': 'admin'
    },
    {
        'SerialNumber': 3, 'ProductNumber': 'WZ-003', 'BatchNumber': 'WZ20260116-001',
        'ThreeMotionMeasDataPath': '/mnt/data/measure/three/WZ20260116-001',
        'FourMotionMeasDataPath': '/mnt/data/measure/four/WZ20260116-001',
        'FiveMotionMeasDataPath': '/mnt/data/measure/five/WZ20260116-001',
        'BladeProfileScanDataPath': None,
        'CreateTime': '2026-01-16 09:00:00', 'Creator': 'test'
    },
    {
        'SerialNumber': 4, 'ProductNumber': 'WZ-004', 'BatchNumber': 'WZ20260116-002',
        'ThreeMotionMeasDataPath': '/mnt/data/measure/three/WZ20260116-002',
        'FourMotionMeasDataPath': '/mnt/data/measure/four/WZ20260116-002',
        'FiveMotionMeasDataPath': '/mnt/data/measure/five/WZ20260116-002',
        'BladeProfileScanDataPath': '/mnt/data/scan/blade/WZ20260116-002',
        'CreateTime': '2026-01-16 14:30:00', 'Creator': 'admin'
    },
    {
        'SerialNumber': 5, 'ProductNumber': 'WZ-005', 'BatchNumber': 'WZ20260117-001',
        'ThreeMotionMeasDataPath': '/mnt/data/measure/three/WZ20260117-001',
        'FourMotionMeasDataPath': None,
        'FiveMotionMeasDataPath': None,
        'BladeProfileScanDataPath': '/mnt/data/scan/blade/WZ20260117-001',
        'CreateTime': '2026-01-17 07:45:00', 'Creator': 'admin'
    },
    {
        'SerialNumber': 6, 'ProductNumber': 'WZ-001', 'BatchNumber': 'WZ20260117-002',
        'ThreeMotionMeasDataPath': '/mnt/data/measure/three/WZ20260117-002',
        'FourMotionMeasDataPath': '/mnt/data/measure/four/WZ20260117-002',
        'FiveMotionMeasDataPath': '/mnt/data/measure/five/WZ20260117-002',
        'BladeProfileScanDataPath': '/mnt/data/scan/blade/WZ20260117-002',
        'CreateTime': '2026-01-17 10:20:00', 'Creator': 'test'
    },
    {
        'SerialNumber': 7, 'ProductNumber': 'WZ-006', 'BatchNumber': 'WZ20260117-003',
        'ThreeMotionMeasDataPath': '/mnt/data/measure/three/WZ20260117-003',
        'FourMotionMeasDataPath': '/mnt/data/measure/four/WZ20260117-003',
        'FiveMotionMeasDataPath': '/mnt/data/measure/five/WZ20260117-003',
        'BladeProfileScanDataPath': '/mnt/data/scan/blade/WZ20260117-003',
        'CreateTime': '2026-01-17 15:00:00', 'Creator': 'admin'
    }
]


class MaintenanceService:
    # ===== 产品检测数据维护 =====
    @staticmethod
    def get_product_quality_list(page=1, page_size=20, filters=None):
        # 演示模式返回模拟数据
        if get_db_status()['demo_mode']:
            items = DEMO_PRODUCT_QUALITY.copy()
            
            # 应用过滤条件
            if filters:
                if filters.get('product_number'):
                    items = [c for c in items if filters['product_number'].lower() in c['ProductNumber'].lower()]
                if filters.get('batch_number'):
                    items = [c for c in items if filters['batch_number'].lower() in c['BatchNumber'].lower()]
            
            # 分页
            total = len(items)
            start = (page - 1) * page_size
            end = start + page_size
            items = items[start:end]
            
            return {
                'items': [ProductQualityDataRelation.from_db_row(row).to_dict() for row in items],
                'total': total, 'page': page,
                'page_size': page_size, 'total_pages': (total + page_size - 1) // page_size
            }
        
        where_clauses, params = [], []
        
        if filters:
            if filters.get('product_number'):
                where_clauses.append("ProductNumber LIKE %s")
                params.append(f"%{filters['product_number']}%")
            if filters.get('batch_number'):
                where_clauses.append("BatchNumber LIKE %s")
                params.append(f"%{filters['batch_number']}%")
        
        where_sql = " AND ".join(where_clauses) if where_clauses else "1=1"
        
        count_result = DatabaseService.execute_qdps_query(
            f"SELECT COUNT(*) as total FROM ProductQualityDataRelation WHERE {where_sql}",
            tuple(params), fetch_one=True
        )
        total = count_result.get('total', 0) if count_result else 0
        
        offset = (page - 1) * page_size
        data_sql = f"""
            SELECT * FROM ProductQualityDataRelation WHERE {where_sql}
            ORDER BY CreateTime DESC
            OFFSET %s ROWS FETCH NEXT %s ROWS ONLY
        """
        params.extend([offset, page_size])
        
        rows = DatabaseService.execute_qdps_query(data_sql, tuple(params))
        items = [ProductQualityDataRelation.from_db_row(row).to_dict() for row in rows]
        
        return {
            'items': items, 'total': total, 'page': page,
            'page_size': page_size, 'total_pages': (total + page_size - 1) // page_size
        }
    
    @staticmethod
    def get_product_quality_by_id(serial_number):
        # 演示模式从模拟数据中查找
        if get_db_status()['demo_mode']:
            for item in DEMO_PRODUCT_QUALITY:
                if item['SerialNumber'] == serial_number:
                    return ProductQualityDataRelation.from_db_row(item)
            return None
        
        sql = "SELECT * FROM ProductQualityDataRelation WHERE SerialNumber = %s"
        row = DatabaseService.execute_qdps_query(sql, (serial_number,), fetch_one=True)
        return ProductQualityDataRelation.from_db_row(row) if row else None
    
    @staticmethod
    def get_product_quality_by_batch(batch_number):
        # 演示模式从模拟数据中查找
        if get_db_status()['demo_mode']:
            for item in DEMO_PRODUCT_QUALITY:
                if item['BatchNumber'] == batch_number:
                    return ProductQualityDataRelation.from_db_row(item)
            return None
        
        sql = "SELECT * FROM ProductQualityDataRelation WHERE BatchNumber = %s"
        row = DatabaseService.execute_qdps_query(sql, (batch_number,), fetch_one=True)
        return ProductQualityDataRelation.from_db_row(row) if row else None
    
    @staticmethod
    def create_product_quality(data, creator):
        # 演示模式模拟创建
        if get_db_status()['demo_mode']:
            # 检查批次号是否已存在
            if MaintenanceService.get_product_quality_by_batch(data.get('batch_number')):
                return {'success': False, 'message': '批次号已存在'}
            
            from datetime import datetime
            new_item = {
                'SerialNumber': max([item['SerialNumber'] for item in DEMO_PRODUCT_QUALITY]) + 1,
                'ProductNumber': data.get('product_number'),
                'BatchNumber': data.get('batch_number'),
                'ThreeMotionMeasDataPath': data.get('three_motion_path'),
                'FourMotionMeasDataPath': data.get('four_motion_path'),
                'FiveMotionMeasDataPath': data.get('five_motion_path'),
                'BladeProfileScanDataPath': data.get('blade_profile_path'),
                'CreateTime': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'Creator': creator
            }
            DEMO_PRODUCT_QUALITY.append(new_item)
            return {'success': True, 'message': '创建成功（演示模式）'}
        
        if MaintenanceService.get_product_quality_by_batch(data.get('batch_number')):
            return {'success': False, 'message': '批次号已存在'}
        
        sql = """
            INSERT INTO ProductQualityDataRelation (
                ProductNumber, BatchNumber, ThreeMotionMeasDataPath,
                FourMotionMeasDataPath, FiveMotionMeasDataPath,
                BladeProfileScanDataPath, Creator, CreateTime
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, GETDATE())
        """
        params = (
            data.get('product_number'), data.get('batch_number'),
            data.get('three_motion_path'), data.get('four_motion_path'),
            data.get('five_motion_path'), data.get('blade_profile_path'), creator
        )
        
        try:
            DatabaseService.execute_qdps_command(sql, params)
            return {'success': True, 'message': '创建成功'}
        except Exception as e:
            return {'success': False, 'message': f'创建失败: {str(e)}'}
    
    @staticmethod
    def update_product_quality(serial_number, data, operator):
        # 演示模式模拟更新
        if get_db_status()['demo_mode']:
            for item in DEMO_PRODUCT_QUALITY:
                if item['SerialNumber'] == serial_number:
                    item.update({
                        'ProductNumber': data.get('product_number'),
                        'ThreeMotionMeasDataPath': data.get('three_motion_path'),
                        'FourMotionMeasDataPath': data.get('four_motion_path'),
                        'FiveMotionMeasDataPath': data.get('five_motion_path'),
                        'BladeProfileScanDataPath': data.get('blade_profile_path')
                    })
                    return {'success': True, 'message': '更新成功（演示模式）'}
            return {'success': False, 'message': '未找到记录'}
        
        sql = """
            UPDATE ProductQualityDataRelation SET
                ProductNumber = %s, ThreeMotionMeasDataPath = %s,
                FourMotionMeasDataPath = %s, FiveMotionMeasDataPath = %s,
                BladeProfileScanDataPath = %s, Operator = %s, ModifyTime = GETDATE()
            WHERE SerialNumber = %s
        """
        params = (
            data.get('product_number'), data.get('three_motion_path'),
            data.get('four_motion_path'), data.get('five_motion_path'),
            data.get('blade_profile_path'), operator, serial_number
        )
        
        try:
            affected = DatabaseService.execute_qdps_command(sql, params)
            return {'success': affected > 0, 'message': '更新成功' if affected > 0 else '未找到记录'}
        except Exception as e:
            return {'success': False, 'message': f'更新失败: {str(e)}'}
    
    @staticmethod
    def delete_product_quality(serial_number):
        # 演示模式模拟删除
        if get_db_status()['demo_mode']:
            for i, item in enumerate(DEMO_PRODUCT_QUALITY):
                if item['SerialNumber'] == serial_number:
                    DEMO_PRODUCT_QUALITY.pop(i)
                    return {'success': True, 'message': '删除成功（演示模式）'}
            return {'success': False, 'message': '未找到记录'}
        
        try:
            affected = DatabaseService.execute_qdps_command(
                "DELETE FROM ProductQualityDataRelation WHERE SerialNumber = %s", (serial_number,)
            )
            return {'success': affected > 0, 'message': '删除成功' if affected > 0 else '未找到记录'}
        except Exception as e:
            return {'success': False, 'message': f'删除失败: {str(e)}'}
    
    # ===== 系统配置维护 =====
    @staticmethod
    def get_system_config(config_key):
        if get_db_status()['demo_mode']:
            return None
        sql = "SELECT * FROM SystemConfig WHERE ConfigKey = %s"
        row = DatabaseService.execute_qdps_query(sql, (config_key,), fetch_one=True)
        return SystemConfig.from_db_row(row) if row else None
    
    @staticmethod
    def get_report_path():
        if get_db_status()['demo_mode']:
            return current_app.config.get('REPORT_BASE_PATH', 'reports')
        config = MaintenanceService.get_system_config('REPORT_BASE_PATH')
        if config and config.config_value:
            return config.config_value
        return current_app.config.get('REPORT_BASE_PATH', 'reports')
    
    @staticmethod
    def update_report_path(path, operator):
        if get_db_status()['demo_mode']:
            return {'success': True, 'message': '演示模式：路径更新成功（未实际保存）'}
        
        existing = MaintenanceService.get_system_config('REPORT_BASE_PATH')
        
        if existing:
            sql = "UPDATE SystemConfig SET ConfigValue = %s, Operator = %s, ModifyTime = GETDATE() WHERE ConfigKey = 'REPORT_BASE_PATH'"
            params = (path, operator)
        else:
            sql = """
                INSERT INTO SystemConfig (ConfigKey, ConfigValue, ConfigType, Description, Operator, CreateTime)
                VALUES ('REPORT_BASE_PATH', %s, 'PATH', '报告存储路径', %s, GETDATE())
            """
            params = (path, operator)
        
        try:
            DatabaseService.execute_qdps_command(sql, params)
            return {'success': True, 'message': '路径更新成功'}
        except Exception as e:
            return {'success': False, 'message': f'更新失败: {str(e)}'}
    
    @staticmethod
    def get_all_configs():
        if get_db_status()['demo_mode']:
            return [{'config_key': 'REPORT_BASE_PATH', 'config_value': 'reports', 'description': '报告存储路径'}]
        sql = "SELECT * FROM SystemConfig ORDER BY ConfigKey"
        rows = DatabaseService.execute_qdps_query(sql)
        return [SystemConfig.from_db_row(row).to_dict() for row in rows]
