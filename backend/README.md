# QDPS 后端服务

基于 Flask 3.0 的 RESTful API 服务，提供质量数据处理系统的后端支持。

## 技术栈

- **框架：** Flask 3.0.0
- **WSGI 服务器：** Gunicorn 21.2.0
- **数据库驱动：** PyMySQL 1.1.0 (MySQL)、PyMSSQL 2.2.11 (SQL Server)
- **认证：** PyJWT 2.8.0
- **数据处理：** Pandas 2.2.0、OpenPyXL 3.1.2
- **跨域：** Flask-CORS 4.0.0

## 项目结构

```
backend/
├── app/
│   ├── __init__.py           # Flask 应用初始化
│   ├── models/               # 数据模型
│   │   ├── user.py          # 用户模型
│   │   ├── product_quality.py    # 产品质量数据模型
│   │   ├── quality_certificate.py # 质量证明单模型
│   │   └── system_config.py      # 系统配置模型
│   ├── routes/               # API 路由
│   │   ├── auth.py          # 认证路由（登录、用户信息）
│   │   ├── dimension.py     # 尺寸判定路由
│   │   ├── certificate.py   # 质量证明单路由
│   │   └── maintenance.py   # 维护功能路由
│   └── services/             # 业务服务
│       ├── auth_service.py       # 认证服务
│       ├── db_service.py         # 数据库服务
│       ├── dimension_service.py  # 尺寸判定服务
│       ├── certificate_service.py # 证明单服务
│       └── maintenance_service.py # 维护服务
├── reports/                  # 判定报告存储（本地开发）
├── sql/                      # SQL 脚本
│   └── init_database.sql    # 数据库初始化脚本
├── config.py                 # 配置文件
├── run.py                    # 启动入口
├── requirements.txt          # Python 依赖
└── Dockerfile               # Docker 镜像构建

```

## 快速开始

### 本地开发

```bash
# 1. 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. 安装依赖
pip install -r requirements.txt

# 3. 启动服务
python run.py
```

服务将在 http://localhost:5001 启动

### Docker 部署

```bash
# 构建镜像
docker build -t qdps-backend .

# 运行容器
docker run -p 5000:5000 \
  -e OA_DB_HOST=192.168.6.88 \
  -e QDPS_DB_HOST=192.168.6.88 \
  qdps-backend
```

## 配置说明

### 环境变量

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| SECRET_KEY | JWT 密钥 | qdps-secret-key-2024-quality-data |
| REPORT_BASE_PATH | 报告存储路径 | ./reports |
| OA_DB_HOST | OA 数据库地址 | 192.168.6.88 |
| OA_DB_USER | OA 数据库用户 | sangfor |
| OA_DB_PASSWORD | OA 数据库密码 | Xrac123.com |
| OA_DB_NAME | OA 数据库名 | ecology |
| QDPS_DB_HOST | QDPS 数据库地址 | 192.168.6.88 |
| QDPS_DB_USER | QDPS 数据库用户 | qdsp |
| QDPS_DB_PASSWORD | QDPS 数据库密码 | Xrac123.com |
| QDPS_DB_NAME | QDPS 数据库名 | qdps |

### 配置文件

`config.py` 包含三个配置类：

- **Config：** 基础配置（数据库连接、密钥等）
- **DevelopmentConfig：** 开发环境配置（DEBUG=True）
- **ProductionConfig：** 生产环境配置（DEBUG=False）

## 运行模式

系统启动时自动检测数据库连接状态：

### 生产模式
- **条件：** OA 数据库 (192.168.6.88:3306) 可达
- **认证：** 使用 OA 系统 HrmResource 表的真实账号
- **数据：** 从 QDPS 数据库读取业务数据

### 演示模式
- **条件：** OA 数据库不可达
- **认证：** 使用内置测试账号（admin/admin123, test/test123）
- **数据：** 使用内存中的模拟数据
- **特点：** 所有功能可正常使用，数据不持久化

## API 接口

### 认证模块 (`/api/auth`)

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| POST | /login | 用户登录 | ❌ |
| GET | /userinfo | 获取用户信息 | ✅ |

### 尺寸判定模块 (`/api/dimension`)

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| GET | /batch-numbers | 获取批次号列表 | ✅ |
| GET | /batch-info/:batch_number | 获取批次信息 | ✅ |
| POST | /check/three-motion | 三动全尺寸判定 | ✅ |
| POST | /check/four-motion | 四动全尺寸判定 | ✅ |
| POST | /check/five-motion | 五动全尺寸判定 | ✅ |
| GET | /download/:filename | 下载判定报告 | ✅ |

### 质量证明单模块 (`/api/certificate`)

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| GET | /list | 获取证明单列表 | ✅ |
| GET | /detail/:id | 获取证明单详情 | ✅ |
| POST | /create | 创建证明单 | ✅ |
| PUT | /update/:id | 更新证明单 | ✅ |
| DELETE | /delete/:id | 删除证明单 | ✅ |
| POST | /submit/:id | 提交证明单 | ✅ |

### 维护模块 (`/api/maintenance`)

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| GET | /product-quality/list | 获取产品质量数据列表 | ✅ |
| POST | /product-quality/create | 创建产品质量数据 | ✅ |
| PUT | /product-quality/update/:id | 更新产品质量数据 | ✅ |
| DELETE | /product-quality/delete/:id | 删除产品质量数据 | ✅ |
| GET | /report-path | 获取报告路径配置 | ✅ |
| PUT | /report-path | 更新报告路径配置 | ✅ |

## 认证机制

### JWT Token

- **生成：** 登录成功后返回 JWT Token
- **有效期：** 8 小时
- **使用：** 请求头携带 `Authorization: Bearer <token>`
- **过期处理：** 返回 401 状态码，前端自动跳转登录页

### 请求示例

```bash
# 登录
curl -X POST http://localhost:5001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

# 携带 Token 请求
curl -X GET http://localhost:5001/api/dimension/batch-numbers \
  -H "Authorization: Bearer <your-token>"
```

## 数据库表结构

### ProductQualityDataRelation（产品质量数据对应关系）

```sql
CREATE TABLE ProductQualityDataRelation (
    SerialNumber INT IDENTITY(1,1) NOT NULL,
    ProductNumber VARCHAR(50) NOT NULL,
    BatchNumber VARCHAR(50) NOT NULL,
    ThreeMotionMeasDataPath VARCHAR(500) NULL,
    FourMotionMeasDataPath VARCHAR(500) NULL,
    FiveMotionMeasDataPath VARCHAR(500) NULL,
    BladeProfileScanDataPath VARCHAR(500) NULL,
    CreateTime DATETIME DEFAULT GETDATE() NOT NULL,
    ModifyTime DATETIME NULL,
    Creator VARCHAR(50) NOT NULL,
    Operator VARCHAR(50) NULL,
    CONSTRAINT PK_ProductQualityDataRelation 
        PRIMARY KEY CLUSTERED (SerialNumber, BatchNumber),
    CONSTRAINT UQ_ProductQualityDataRelation_BatchNumber 
        UNIQUE NONCLUSTERED (BatchNumber)
);
```

### QualityCertificate（质量证明单）

```sql
CREATE TABLE QualityCertificate (
    Id INT IDENTITY(1,1) PRIMARY KEY,
    CertificateNumber VARCHAR(50) NOT NULL UNIQUE,
    ProductNumber VARCHAR(50) NULL,
    ProductModel VARCHAR(100) NULL,
    BatchNumber VARCHAR(50) NULL,
    PartNumber VARCHAR(50) NULL,
    PartName NVARCHAR(100) NULL,
    Quantity INT NULL,
    Unit NVARCHAR(20) NULL,
    SupplierCode VARCHAR(20) DEFAULT '203239',
    InspectionDate DATE NULL,
    Inspector NVARCHAR(50) NULL,
    Status INT DEFAULT 0,
    Remark NVARCHAR(500) NULL,
    CreateTime DATETIME DEFAULT GETDATE() NOT NULL,
    ModifyTime DATETIME NULL,
    Creator VARCHAR(50) NOT NULL,
    Operator VARCHAR(50) NULL
);
```

### SystemConfig（系统配置）

```sql
CREATE TABLE SystemConfig (
    Id INT IDENTITY(1,1) PRIMARY KEY,
    ConfigKey VARCHAR(100) NOT NULL UNIQUE,
    ConfigValue NVARCHAR(500) NULL,
    Description NVARCHAR(200) NULL,
    CreateTime DATETIME DEFAULT GETDATE() NOT NULL,
    ModifyTime DATETIME NULL
);
```

## 业务逻辑

### 尺寸判定流程

1. 用户选择批次号
2. 从 ProductQualityDataRelation 表查询数据路径
3. 读取指定路径下的测量数据文件（Excel/CSV）
4. 执行尺寸判定逻辑（实测值与上下限对比）
5. 生成判定报告（Excel 格式，包含汇总和详细结果）
6. 返回判定结果和报告文件名

### 质量证明单编号规则

- **格式：** `QC-XXXXXX-20XX-XXXX`
- **说明：**
  - QC：质量证明（Quality Certificate）
  - XXXXXX：供应商代码（固定 203239）
  - 20XX：年代号（如 2026）
  - XXXX：4位流水号（自动递增）
- **示例：** `QC-203239-2026-0001`

### 报告生成

判定报告为 Excel 格式，包含两个工作表：

1. **汇总表：** 报告类型、产品号、批次号、判定时间、操作人、总体结果
2. **详细结果表：** 文件名、判定结果、检测项总数、合格项数、不合格项数、详情

## 开发指南

### 添加新接口

1. 在 `app/routes/` 创建或编辑路由文件
2. 在 `app/services/` 创建或编辑服务文件
3. 在 `app/__init__.py` 注册蓝图（如果是新模块）

### 数据库操作

使用 `DatabaseService` 类进行数据库操作：

```python
from app.services.db_service import DatabaseService

# 查询
result = DatabaseService.execute_qdps_query(
    "SELECT * FROM ProductQualityDataRelation WHERE BatchNumber = %s",
    (batch_number,),
    fetch_one=True
)

# 插入/更新/删除
DatabaseService.execute_qdps_update(
    "INSERT INTO QualityCertificate (...) VALUES (...)",
    (value1, value2, ...)
)
```

### 演示模式数据

在各 service 文件中定义 `DEMO_*` 常量存储演示数据：

```python
DEMO_BATCH_LIST = [
    {'BatchNumber': 'WZ20260117-001', 'ProductNumber': 'WZ-001'},
    # ...
]

# 在方法中判断模式
if get_db_status()['demo_mode']:
    return DEMO_BATCH_LIST
else:
    return DatabaseService.execute_qdps_query(sql)
```

## 日志

启动时会显示数据库连接状态：

```
==================================================
检测数据库连接...
==================================================
检测 OA (192.168.6.88:3306)... 端口不可达
跳过 QDPS 检测（OA 不可用）
>>> 启用【演示模式】
    测试账号: admin/admin123, test/test123
==================================================
```

## 常见问题

### Q: 如何切换到生产模式？
A: 确保 OA 数据库 (192.168.6.88:3306) 可访问，系统会自动切换。

### Q: 报告文件存储在哪里？
A: 本地开发存储在 `backend/reports/`，Docker 部署存储在 `/app/reports`（映射到宿主机 `data/reports/`）。

### Q: 如何修改数据库连接？
A: 编辑 `config.py` 或设置环境变量。

### Q: Token 过期怎么办？
A: 前端会自动处理，显示提示并跳转登录页。后端返回 401 状态码。

## 许可证

内部项目，仅供公司内部使用。
