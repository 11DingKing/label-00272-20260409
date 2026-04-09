"""质量证明单号服务"""
from datetime import datetime
from flask import current_app
from app.services.db_service import DatabaseService, get_db_status
from app.models.quality_certificate import QualityCertificate


# 演示模式模拟数据
DEMO_CERTIFICATES = [
    {
        'Id': 1, 'CertificateNumber': 'QC-203239-2026-0001',
        'ProductNumber': 'WZ-001', 'ProductModel': 'WZ-2026A',
        'BatchNumber': 'WZ20260115-001', 'PartNumber': 'BLD-001',
        'PartName': '涡轮叶片-A型', 'Quantity': 120, 'Unit': '件',
        'SupplierCode': '203239', 'InspectionDate': '2026-01-15',
        'Inspector': '张伟', 'Status': 1, 'Remark': '首批次产品，检测合格',
        'CreateTime': '2026-01-15 09:30:00', 'Creator': 'admin'
    },
    {
        'Id': 2, 'CertificateNumber': 'QC-203239-2026-0002',
        'ProductNumber': 'WZ-002', 'ProductModel': 'WZ-2026B',
        'BatchNumber': 'WZ20260115-002', 'PartNumber': 'BLD-002',
        'PartName': '涡轮叶片-B型', 'Quantity': 80, 'Unit': '件',
        'SupplierCode': '203239', 'InspectionDate': '2026-01-15',
        'Inspector': '李明', 'Status': 1, 'Remark': '二批次产品',
        'CreateTime': '2026-01-15 14:20:00', 'Creator': 'admin'
    },
    {
        'Id': 3, 'CertificateNumber': 'QC-203239-2026-0003',
        'ProductNumber': 'WZ-003', 'ProductModel': 'WZ-2026C',
        'BatchNumber': 'WZ20260116-001', 'PartNumber': 'SFT-001',
        'PartName': '传动轴-标准型', 'Quantity': 50, 'Unit': '件',
        'SupplierCode': '203239', 'InspectionDate': '2026-01-16',
        'Inspector': '王芳', 'Status': 0, 'Remark': '待审核',
        'CreateTime': '2026-01-16 10:15:00', 'Creator': 'test'
    },
    {
        'Id': 4, 'CertificateNumber': 'QC-203239-2026-0004',
        'ProductNumber': 'WZ-004', 'ProductModel': 'WZ-2026D',
        'BatchNumber': 'WZ20260116-002', 'PartNumber': 'GER-001',
        'PartName': '齿轮组件-高精度', 'Quantity': 200, 'Unit': '套',
        'SupplierCode': '203239', 'InspectionDate': '2026-01-16',
        'Inspector': '张伟', 'Status': 1, 'Remark': '批量生产',
        'CreateTime': '2026-01-16 15:45:00', 'Creator': 'admin'
    },
    {
        'Id': 5, 'CertificateNumber': 'QC-203239-2026-0005',
        'ProductNumber': 'WZ-005', 'ProductModel': 'WZ-2026E',
        'BatchNumber': 'WZ20260117-001', 'PartNumber': 'HSG-001',
        'PartName': '轴承座-铸造件', 'Quantity': 30, 'Unit': '件',
        'SupplierCode': '203239', 'InspectionDate': '2026-01-17',
        'Inspector': '李明', 'Status': 0, 'Remark': '新工艺试制',
        'CreateTime': '2026-01-17 08:00:00', 'Creator': 'admin'
    },
    {
        'Id': 6, 'CertificateNumber': 'QC-203239-2026-0006',
        'ProductNumber': 'WZ-001', 'ProductModel': 'WZ-2026A',
        'BatchNumber': 'WZ20260117-002', 'PartNumber': 'BLD-001',
        'PartName': '涡轮叶片-A型', 'Quantity': 150, 'Unit': '件',
        'SupplierCode': '203239', 'InspectionDate': '2026-01-17',
        'Inspector': '王芳', 'Status': 0, 'Remark': '第三批次',
        'CreateTime': '2026-01-17 11:30:00', 'Creator': 'test'
    }
]


class CertificateService:
    @staticmethod
    def get_next_sequence_number(year=None):
        if year is None:
            year = datetime.now().year
        
        sql = """
            SELECT MAX(CAST(RIGHT(CertificateNumber, 4) AS INT)) as max_seq
            FROM QualityCertificate
            WHERE CertificateNumber LIKE %s
        """
        result = DatabaseService.execute_qdps_query(sql, (f'QC-%-{year}-%',), fetch_one=True)
        
        if result and result.get('max_seq'):
            return result['max_seq'] + 1
        return 1
    
    @staticmethod
    def generate_certificate_number():
        # 演示模式生成模拟编号
        if get_db_status()['demo_mode']:
            supplier_code = '203239'
            year = datetime.now().year
            # 从演示数据中找到最大序号
            max_seq = 0
            for cert in DEMO_CERTIFICATES:
                cert_num = cert['CertificateNumber']
                if f'-{year}-' in cert_num:
                    seq = int(cert_num.split('-')[-1])
                    max_seq = max(max_seq, seq)
            sequence = max_seq + 1
            return QualityCertificate.generate_certificate_number(supplier_code, year, sequence)
        
        supplier_code = current_app.config.get('SUPPLIER_CODE', '203239')
        year = datetime.now().year
        sequence = CertificateService.get_next_sequence_number(year)
        return QualityCertificate.generate_certificate_number(supplier_code, year, sequence)
    
    @staticmethod
    def create_certificate(data, creator):
        # 演示模式模拟创建
        if get_db_status()['demo_mode']:
            certificate_number = CertificateService.generate_certificate_number()
            new_cert = {
                'Id': max([c['Id'] for c in DEMO_CERTIFICATES]) + 1,
                'CertificateNumber': certificate_number,
                'ProductNumber': data.get('product_number'),
                'ProductModel': data.get('product_model'),
                'BatchNumber': data.get('batch_number'),
                'PartNumber': data.get('part_number'),
                'PartName': data.get('part_name'),
                'Quantity': data.get('quantity'),
                'Unit': data.get('unit'),
                'SupplierCode': '203239',
                'InspectionDate': data.get('inspection_date'),
                'Inspector': data.get('inspector'),
                'Status': 0,
                'Remark': data.get('remark'),
                'CreateTime': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'Creator': creator
            }
            DEMO_CERTIFICATES.append(new_cert)
            return {'success': True, 'message': '创建成功（演示模式）', 'certificate_number': certificate_number}
        
        certificate_number = CertificateService.generate_certificate_number()
        
        sql = """
            INSERT INTO QualityCertificate (
                CertificateNumber, ProductNumber, ProductModel, BatchNumber,
                PartNumber, PartName, Quantity, Unit, SupplierCode,
                InspectionDate, Inspector, Status, Remark, Creator, CreateTime
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, GETDATE())
        """
        
        params = (
            certificate_number, data.get('product_number'), data.get('product_model'),
            data.get('batch_number'), data.get('part_number'), data.get('part_name'),
            data.get('quantity'), data.get('unit'),
            current_app.config.get('SUPPLIER_CODE', '203239'),
            data.get('inspection_date'), data.get('inspector'), 0, data.get('remark'), creator
        )
        
        try:
            DatabaseService.execute_qdps_command(sql, params)
            return {'success': True, 'message': '创建成功', 'certificate_number': certificate_number}
        except Exception as e:
            return {'success': False, 'message': f'创建失败: {str(e)}'}
    
    @staticmethod
    def get_certificate_list(page=1, page_size=20, filters=None):
        # 演示模式返回模拟数据
        if get_db_status()['demo_mode']:
            items = DEMO_CERTIFICATES.copy()
            
            # 应用过滤条件
            if filters:
                if filters.get('certificate_number'):
                    items = [c for c in items if filters['certificate_number'].lower() in c['CertificateNumber'].lower()]
                if filters.get('batch_number'):
                    items = [c for c in items if filters['batch_number'].lower() in c['BatchNumber'].lower()]
                if filters.get('product_number'):
                    items = [c for c in items if filters['product_number'].lower() in c['ProductNumber'].lower()]
                if filters.get('status') is not None:
                    items = [c for c in items if c['Status'] == filters['status']]
            
            # 分页
            total = len(items)
            start = (page - 1) * page_size
            end = start + page_size
            items = items[start:end]
            
            return {
                'items': [QualityCertificate.from_db_row(row).to_dict() for row in items],
                'total': total, 'page': page,
                'page_size': page_size, 'total_pages': (total + page_size - 1) // page_size
            }
        
        where_clauses, params = [], []
        
        if filters:
            if filters.get('certificate_number'):
                where_clauses.append("CertificateNumber LIKE %s")
                params.append(f"%{filters['certificate_number']}%")
            if filters.get('batch_number'):
                where_clauses.append("BatchNumber LIKE %s")
                params.append(f"%{filters['batch_number']}%")
            if filters.get('product_number'):
                where_clauses.append("ProductNumber LIKE %s")
                params.append(f"%{filters['product_number']}%")
            if filters.get('status') is not None:
                where_clauses.append("Status = %s")
                params.append(filters['status'])
        
        where_sql = " AND ".join(where_clauses) if where_clauses else "1=1"
        
        count_result = DatabaseService.execute_qdps_query(
            f"SELECT COUNT(*) as total FROM QualityCertificate WHERE {where_sql}",
            tuple(params), fetch_one=True
        )
        total = count_result.get('total', 0) if count_result else 0
        
        offset = (page - 1) * page_size
        data_sql = f"""
            SELECT * FROM QualityCertificate WHERE {where_sql}
            ORDER BY CreateTime DESC
            OFFSET %s ROWS FETCH NEXT %s ROWS ONLY
        """
        params.extend([offset, page_size])
        
        rows = DatabaseService.execute_qdps_query(data_sql, tuple(params))
        certificates = [QualityCertificate.from_db_row(row).to_dict() for row in rows]
        
        return {
            'items': certificates, 'total': total, 'page': page,
            'page_size': page_size, 'total_pages': (total + page_size - 1) // page_size
        }
    
    @staticmethod
    def get_certificate_by_id(certificate_id):
        # 演示模式返回模拟数据
        if get_db_status()['demo_mode']:
            for cert_data in DEMO_CERTIFICATES:
                if cert_data['Id'] == certificate_id:
                    return QualityCertificate.from_db_row(cert_data)
            return None
        
        sql = "SELECT * FROM QualityCertificate WHERE Id = %s"
        row = DatabaseService.execute_qdps_query(sql, (certificate_id,), fetch_one=True)
        return QualityCertificate.from_db_row(row) if row else None
    
    @staticmethod
    def update_certificate(certificate_id, data, operator):
        # 演示模式模拟更新
        if get_db_status()['demo_mode']:
            for cert_data in DEMO_CERTIFICATES:
                if cert_data['Id'] == certificate_id:
                    # 更新模拟数据
                    cert_data.update({
                        'ProductNumber': data.get('product_number'),
                        'ProductModel': data.get('product_model'),
                        'BatchNumber': data.get('batch_number'),
                        'PartNumber': data.get('part_number'),
                        'PartName': data.get('part_name'),
                        'Quantity': data.get('quantity'),
                        'Unit': data.get('unit'),
                        'InspectionDate': data.get('inspection_date'),
                        'Inspector': data.get('inspector'),
                        'Remark': data.get('remark')
                    })
                    return {'success': True, 'message': '更新成功（演示模式）'}
            return {'success': False, 'message': '未找到记录'}
        
        sql = """
            UPDATE QualityCertificate SET
                ProductNumber = %s, ProductModel = %s, BatchNumber = %s,
                PartNumber = %s, PartName = %s, Quantity = %s, Unit = %s,
                InspectionDate = %s, Inspector = %s, Remark = %s,
                Operator = %s, ModifyTime = GETDATE()
            WHERE Id = %s
        """
        params = (
            data.get('product_number'), data.get('product_model'), data.get('batch_number'),
            data.get('part_number'), data.get('part_name'), data.get('quantity'), data.get('unit'),
            data.get('inspection_date'), data.get('inspector'), data.get('remark'),
            operator, certificate_id
        )
        
        try:
            affected = DatabaseService.execute_qdps_command(sql, params)
            return {'success': affected > 0, 'message': '更新成功' if affected > 0 else '未找到记录'}
        except Exception as e:
            return {'success': False, 'message': f'更新失败: {str(e)}'}
    
    @staticmethod
    def delete_certificate(certificate_id):
        # 演示模式模拟删除
        if get_db_status()['demo_mode']:
            for i, cert_data in enumerate(DEMO_CERTIFICATES):
                if cert_data['Id'] == certificate_id:
                    if cert_data['Status'] != 0:
                        return {'success': False, 'message': '只能删除草稿状态的证明单'}
                    DEMO_CERTIFICATES.pop(i)
                    return {'success': True, 'message': '删除成功（演示模式）'}
            return {'success': False, 'message': '未找到记录'}
        
        cert = CertificateService.get_certificate_by_id(certificate_id)
        if not cert:
            return {'success': False, 'message': '未找到记录'}
        if cert.status != 0:
            return {'success': False, 'message': '只能删除草稿状态的证明单'}
        
        try:
            DatabaseService.execute_qdps_command("DELETE FROM QualityCertificate WHERE Id = %s", (certificate_id,))
            return {'success': True, 'message': '删除成功'}
        except Exception as e:
            return {'success': False, 'message': f'删除失败: {str(e)}'}
    
    @staticmethod
    def submit_certificate(certificate_id, operator):
        # 演示模式模拟提交
        if get_db_status()['demo_mode']:
            for cert_data in DEMO_CERTIFICATES:
                if cert_data['Id'] == certificate_id and cert_data['Status'] == 0:
                    cert_data['Status'] = 1
                    return {'success': True, 'message': '提交成功（演示模式）'}
            return {'success': False, 'message': '提交失败'}
        
        sql = "UPDATE QualityCertificate SET Status = 1, Operator = %s, ModifyTime = GETDATE() WHERE Id = %s AND Status = 0"
        try:
            affected = DatabaseService.execute_qdps_command(sql, (operator, certificate_id))
            return {'success': affected > 0, 'message': '提交成功' if affected > 0 else '提交失败'}
        except Exception as e:
            return {'success': False, 'message': f'提交失败: {str(e)}'}
