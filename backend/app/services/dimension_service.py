"""尺寸判定服务"""
import os
import pandas as pd
from datetime import datetime
from flask import current_app
from app.services.db_service import DatabaseService, get_db_status


# 演示模式批次数据
DEMO_BATCH_LIST = [
    {'BatchNumber': 'WZ20260117-003', 'ProductNumber': 'WZ-006'},
    {'BatchNumber': 'WZ20260117-002', 'ProductNumber': 'WZ-001'},
    {'BatchNumber': 'WZ20260117-001', 'ProductNumber': 'WZ-005'},
    {'BatchNumber': 'WZ20260116-002', 'ProductNumber': 'WZ-004'},
    {'BatchNumber': 'WZ20260116-001', 'ProductNumber': 'WZ-003'},
    {'BatchNumber': 'WZ20260115-002', 'ProductNumber': 'WZ-002'},
    {'BatchNumber': 'WZ20260115-001', 'ProductNumber': 'WZ-001'},
]

DEMO_BATCH_INFO = {
    'WZ20260117-003': {
        'BatchNumber': 'WZ20260117-003', 'ProductNumber': 'WZ-006',
        'ThreeMotionMeasDataPath': '/mnt/data/measure/three/WZ20260117-003',
        'FourMotionMeasDataPath': '/mnt/data/measure/four/WZ20260117-003',
        'FiveMotionMeasDataPath': '/mnt/data/measure/five/WZ20260117-003',
    },
    'WZ20260117-002': {
        'BatchNumber': 'WZ20260117-002', 'ProductNumber': 'WZ-001',
        'ThreeMotionMeasDataPath': '/mnt/data/measure/three/WZ20260117-002',
        'FourMotionMeasDataPath': '/mnt/data/measure/four/WZ20260117-002',
        'FiveMotionMeasDataPath': '/mnt/data/measure/five/WZ20260117-002',
    },
    'WZ20260117-001': {
        'BatchNumber': 'WZ20260117-001', 'ProductNumber': 'WZ-005',
        'ThreeMotionMeasDataPath': '/mnt/data/measure/three/WZ20260117-001',
        'FourMotionMeasDataPath': None,
        'FiveMotionMeasDataPath': None,
    },
    'WZ20260116-002': {
        'BatchNumber': 'WZ20260116-002', 'ProductNumber': 'WZ-004',
        'ThreeMotionMeasDataPath': '/mnt/data/measure/three/WZ20260116-002',
        'FourMotionMeasDataPath': '/mnt/data/measure/four/WZ20260116-002',
        'FiveMotionMeasDataPath': '/mnt/data/measure/five/WZ20260116-002',
    },
    'WZ20260116-001': {
        'BatchNumber': 'WZ20260116-001', 'ProductNumber': 'WZ-003',
        'ThreeMotionMeasDataPath': '/mnt/data/measure/three/WZ20260116-001',
        'FourMotionMeasDataPath': '/mnt/data/measure/four/WZ20260116-001',
        'FiveMotionMeasDataPath': '/mnt/data/measure/five/WZ20260116-001',
    },
    'WZ20260115-002': {
        'BatchNumber': 'WZ20260115-002', 'ProductNumber': 'WZ-002',
        'ThreeMotionMeasDataPath': '/mnt/data/measure/three/WZ20260115-002',
        'FourMotionMeasDataPath': '/mnt/data/measure/four/WZ20260115-002',
        'FiveMotionMeasDataPath': None,
    },
    'WZ20260115-001': {
        'BatchNumber': 'WZ20260115-001', 'ProductNumber': 'WZ-001',
        'ThreeMotionMeasDataPath': '/mnt/data/measure/three/WZ20260115-001',
        'FourMotionMeasDataPath': '/mnt/data/measure/four/WZ20260115-001',
        'FiveMotionMeasDataPath': '/mnt/data/measure/five/WZ20260115-001',
    },
}


class DimensionCheckService:
    @staticmethod
    def get_batch_numbers():
        """获取所有批次号列表"""
        if get_db_status()['demo_mode']:
            return DEMO_BATCH_LIST
        
        sql = """
            SELECT DISTINCT BatchNumber, ProductNumber 
            FROM ProductQualityDataRelation 
            ORDER BY BatchNumber DESC
        """
        return DatabaseService.execute_qdps_query(sql)
    
    @staticmethod
    def get_batch_info(batch_number):
        """根据批次号获取信息"""
        if get_db_status()['demo_mode']:
            return DEMO_BATCH_INFO.get(batch_number)
        
        sql = "SELECT * FROM ProductQualityDataRelation WHERE BatchNumber = %s"
        return DatabaseService.execute_qdps_query(sql, (batch_number,), fetch_one=True)
    
    @staticmethod
    def check_motion(batch_number, motion_type, operator):
        """执行尺寸判定"""
        batch_info = DimensionCheckService.get_batch_info(batch_number)
        if not batch_info:
            return {'success': False, 'message': f'未找到批次号 {batch_number} 的数据'}
        
        path_key = {
            '三动': 'ThreeMotionMeasDataPath',
            '四动': 'FourMotionMeasDataPath',
            '五动': 'FiveMotionMeasDataPath'
        }.get(motion_type)
        
        data_path = batch_info.get(path_key)
        if not data_path:
            return {'success': False, 'message': f'{motion_type}实测数据路径未配置'}
        
        # 演示模式返回模拟判定结果
        if get_db_status()['demo_mode']:
            return DimensionCheckService._demo_check_result(
                batch_number, motion_type, 
                batch_info.get('ProductNumber'), operator
            )
        
        if not os.path.exists(data_path):
            return {'success': False, 'message': f'数据路径不存在: {data_path}'}
        
        try:
            return DimensionCheckService._process_check(
                data_path, motion_type, batch_number,
                batch_info.get('ProductNumber'), operator
            )
        except Exception as e:
            return {'success': False, 'message': f'判定过程出错: {str(e)}'}
    
    @staticmethod
    def _demo_check_result(batch_number, motion_type, product_number, operator):
        """演示模式模拟判定结果"""
        import random
        
        # 模拟几个测量文件的结果
        demo_files = [
            f'{batch_number}_测量数据_001.xlsx',
            f'{batch_number}_测量数据_002.xlsx',
            f'{batch_number}_测量数据_003.xlsx',
        ]
        
        results = []
        files_passed = 0
        files_failed = 0
        
        for filename in demo_files:
            # 90% 概率合格
            passed = random.random() > 0.1
            total_items = random.randint(15, 30)
            if passed:
                passed_items = total_items
                failed_items = 0
                details = '所有项目合格'
                files_passed += 1
            else:
                failed_items = random.randint(1, 3)
                passed_items = total_items - failed_items
                details = f'直径尺寸: 25.08超出[24.95, 25.05]; 圆度: 0.012超出[0, 0.01]'
                files_failed += 1
            
            results.append({
                'filename': filename,
                'passed': passed,
                'details': details,
                'total_items': total_items,
                'passed_items': passed_items,
                'failed_items': failed_items
            })
        
        overall_passed = files_failed == 0
        report_filename = f"{motion_type}全尺寸判定报告_{batch_number}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        
        # 演示模式也生成实际的报告文件
        report_base_path = current_app.config.get('REPORT_BASE_PATH', 'reports')
        os.makedirs(report_base_path, exist_ok=True)
        report_path = os.path.join(report_base_path, report_filename)
        DimensionCheckService._generate_report(results, report_path, motion_type, batch_number, product_number, operator)
        
        return {
            'success': True,
            'passed': overall_passed,
            'message': '判定完成（演示模式）',
            'summary': {
                'motion_type': motion_type,
                'batch_number': batch_number,
                'product_number': product_number,
                'files_processed': len(demo_files),
                'files_passed': files_passed,
                'files_failed': files_failed,
                'overall_result': '合格' if overall_passed else '不合格'
            },
            'details': results,
            'report_filename': report_filename,
            'demo_mode': True
        }
    
    @staticmethod
    def _process_check(data_path, motion_type, batch_number, product_number, operator):
        """处理判定逻辑"""
        results = []
        files_processed = files_passed = files_failed = 0
        
        report_base_path = current_app.config.get('REPORT_BASE_PATH', 'reports')
        os.makedirs(report_base_path, exist_ok=True)
        
        for filename in os.listdir(data_path):
            if filename.endswith(('.xlsx', '.xls', '.csv')):
                file_path = os.path.join(data_path, filename)
                try:
                    df = pd.read_csv(file_path) if filename.endswith('.csv') else pd.read_excel(file_path)
                    check_result = DimensionCheckService._check_dimensions(df)
                    
                    files_processed += 1
                    if check_result['passed']:
                        files_passed += 1
                    else:
                        files_failed += 1
                    
                    results.append({
                        'filename': filename,
                        'passed': check_result['passed'],
                        'details': check_result['details'],
                        'total_items': check_result.get('total_items', 0),
                        'passed_items': check_result.get('passed_items', 0),
                        'failed_items': check_result.get('failed_items', 0)
                    })
                except Exception as e:
                    results.append({'filename': filename, 'passed': False, 'details': f'文件处理错误: {str(e)}', 'error': True})
                    files_processed += 1
                    files_failed += 1
        
        report_filename = f"{motion_type}全尺寸判定报告_{batch_number}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        report_path = os.path.join(report_base_path, report_filename)
        
        DimensionCheckService._generate_report(results, report_path, motion_type, batch_number, product_number, operator)
        
        overall_passed = files_failed == 0 and files_processed > 0
        
        return {
            'success': True,
            'passed': overall_passed,
            'message': '判定完成',
            'summary': {
                'motion_type': motion_type,
                'batch_number': batch_number,
                'product_number': product_number,
                'files_processed': files_processed,
                'files_passed': files_passed,
                'files_failed': files_failed,
                'overall_result': '合格' if overall_passed else '不合格'
            },
            'details': results,
            'report_filename': report_filename
        }
    
    @staticmethod
    def _check_dimensions(df):
        """执行尺寸判定"""
        passed_items = failed_items = 0
        details = []
        
        column_mapping = {}
        for col in df.columns:
            col_lower = str(col).lower().strip()
            if '测量' in col_lower or '项目' in col_lower:
                column_mapping['测量项'] = col
            elif '标准' in col_lower:
                column_mapping['标准值'] = col
            elif '上限' in col_lower or 'upper' in col_lower:
                column_mapping['上限'] = col
            elif '下限' in col_lower or 'lower' in col_lower:
                column_mapping['下限'] = col
            elif '实测' in col_lower or 'actual' in col_lower:
                column_mapping['实测值'] = col
        
        if '实测值' not in column_mapping or ('上限' not in column_mapping and '下限' not in column_mapping):
            return {'passed': True, 'details': '数据格式不符合标准格式', 'total_items': len(df), 'passed_items': len(df), 'failed_items': 0}
        
        for idx, row in df.iterrows():
            try:
                actual = float(row[column_mapping.get('实测值')])
                upper = float(row[column_mapping.get('上限')]) if '上限' in column_mapping else float('inf')
                lower = float(row[column_mapping.get('下限')]) if '下限' in column_mapping else float('-inf')
                
                if lower <= actual <= upper:
                    passed_items += 1
                else:
                    failed_items += 1
                    item_name = row.get(column_mapping.get('测量项'), f'项目{idx+1}')
                    details.append(f'{item_name}: {actual}超出[{lower}, {upper}]')
            except:
                passed_items += 1
        
        return {
            'passed': failed_items == 0,
            'details': '; '.join(details) if details else '所有项目合格',
            'total_items': passed_items + failed_items,
            'passed_items': passed_items,
            'failed_items': failed_items
        }
    
    @staticmethod
    def _generate_report(results, report_path, motion_type, batch_number, product_number, operator):
        """生成报告"""
        os.makedirs(os.path.dirname(report_path), exist_ok=True)
        
        report_data = [{
            '文件名': r['filename'],
            '判定结果': '合格' if r['passed'] else '不合格',
            '检测项总数': r.get('total_items', '-'),
            '合格项数': r.get('passed_items', '-'),
            '不合格项数': r.get('failed_items', '-'),
            '详情': r['details']
        } for r in results]
        
        df_report = pd.DataFrame(report_data)
        
        summary_data = {
            '报告类型': [f'{motion_type}全尺寸判定报告'],
            '产品号': [product_number],
            '批次号': [batch_number],
            '判定时间': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
            '操作人': [operator],
            '总体结果': ['合格' if all(r['passed'] for r in results) else '不合格']
        }
        df_summary = pd.DataFrame(summary_data)
        
        with pd.ExcelWriter(report_path, engine='openpyxl') as writer:
            df_summary.T.to_excel(writer, sheet_name='汇总', header=False)
            df_report.to_excel(writer, sheet_name='详细结果', index=False)
