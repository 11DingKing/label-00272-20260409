# QDPS 质量数据处理系统

## 快速启动

### 方式一：本地开发模式

```bash
# 1. 启动后端
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python run.py

# 2. 启动前端（新终端）
cd frontend-admin
npm install
npm run dev
```

启动后访问：http://localhost:8081

> **说明：** 后端启动时会自动检测数据库连接，如果 OA 数据库不可达，将自动切换到演示模式。

### 方式二：Docker 部署

```bash
# 构建并启动
docker-compose up --build -d

# 查看状态
docker-compose ps

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down

```



## 服务端口

| 服务 | 本地开发 | Docker |
|------|----------|--------|
| 前端 | 8081 | 8081 |
| 后端 | 5001 | 5000 (内部) |

> **注意：** 本地开发时后端使用 5001 端口（macOS 的 5000 端口被 AirPlay 占用）

## 技术栈

- **后端：** Python Flask + Gunicorn
- **前端：** Vue 3 + Vite + Element Plus + Pinia
- **容器：** Docker + Docker Compose
- **数据库：** SQL Server (QDPS) + MySQL (OA系统)

## 运行模式

系统启动时会自动检测数据库连接状态：

| 模式 | 条件 | 说明 |
|------|------|------|
| 生产模式 | OA 数据库可达 | 使用 OA 系统账号登录 |
| 演示模式 | OA 数据库不可达 | 使用内置测试账号 |

**测试账号（演示模式）：**

| 用户名 | 密码 | 说明 |
|--------|------|------|
| admin | admin123 | 管理员账号 |
| test | test123 | 测试用户 |

> 生产环境连接 OA 系统 (192.168.6.88) 后，将使用 HrmResource 表中的真实账号

## 题目内容

连接数据库  192.168.6.88  OA系统（登录认证）  'db_user': 'sangfor',      'db_password': 'Xrac123.com',      'db_database': 'ecology',   质量数据处理系统 数据库  QDPS（质量数据处理系统）  qdsp Xrac123.com   MES系统 caxa_science_mes    # 连接数据库              connection = pymysql.connect(                  host='192.168.6.91',  # 数据库服务器IP                  user='caxa_readonly',                  password='Read@123.com',                  database='caxa_science_mes',                  cursorclass=DictCursor              )   我需要 有一个 质量数据处理系统  B/S架构的，首先需要用户登录认证，登录认证方式见oa_auth.py  登录后用户连接QDPS数据库  系统有以下菜单，对应不同的页面，将现有程序业务逻辑调整为B/S架构，最终生成的文件存储在临时路径“WEB\报告”（路径后续在“报告路径维护”菜单可维护）  三动全尺寸判定  四动全尺寸判定  五动全尺寸判定   逻辑：  三、四、五动的判定逻辑与之前的大体一致，不过不需要用户输入文件夹，用户首先输入或者选择批次号（数据来源于ProductQualityDataRelation表的批次号），通过数据库查询相关数据的存储路径。   质量证明单号  逻辑：每个质量证明单在原有逻辑的基础上新增D4值等于“表单编号：QC-______-20___-______”  编码规则  1.本表单编号规则为“QC（质量证明）-XXXXXX（供应商代码）-20XX（年代号）-XXXX（顺序号）”。  供应商号固定203239，顺序号4位流水号自动生成，  质量证明单号，需要设计表结构，需包含产品号、产品型号、批次号、零件号等其他必要字段    基础数据维护    1、产品检测数据维护（关联数据库QDPS的ProductQualityDataRelation表，在此菜单可维护这些数据）  表结构：  -- 产品质量数据对应关系表（修正版：仅表结构+主键/唯一约束）  CREATE TABLE ProductQualityDataRelation (      -- 序号（自增）      SerialNumber INT IDENTITY(1,1) NOT NULL,      -- 产品号（非空、可重复）      ProductNumber VARCHAR(50) NOT NULL,      -- 批次号（非空、全局唯一）      BatchNumber VARCHAR(50) NOT NULL,      -- 3动实测数据保存路径      ThreeMotionMeasDataPath VARCHAR(500) NULL,      -- 4动实测数据保存路径      FourMotionMeasDataPath VARCHAR(500) NULL,      -- 5动实测数据保存路径      FiveMotionMeasDataPath VARCHAR(500) NULL,      -- 自叶型扫描数据路径      BladeProfileScanDataPath VARCHAR(500) NULL,      -- 审计字段：创建时间      CreateTime DATETIME DEFAULT GETDATE() NOT NULL,      -- 审计字段：修改时间      ModifyTime DATETIME NULL,      -- 审计字段：创建人      Creator VARCHAR(50) NOT NULL,      -- 审计字段：操作人      Operator VARCHAR(50) NULL,       -- 复合主键（聚集索引）      CONSTRAINT PK_ProductQualityDataRelation          PRIMARY KEY CLUSTERED (SerialNumber, BatchNumber),      -- 批次号唯一约束（自动生成唯一非聚集索引）      CONSTRAINT UQ_ProductQualityDataRelation_BatchNumber          UNIQUE NONCLUSTERED (BatchNumber)  );  -- 自叶型扫描数据路径  EXEC sp_addextendedproperty      @name = N'MS_Description',      @value = N'自叶型扫描数据文件的存储路径（支持本地/网络UNC路径）',      @level0type = N'SCHEMA', @level0name = N'dbo',      @level1type = N'TABLE',  @level1name = N'ProductQualityDataRelation',      @level2type = N'COLUMN', @level2name = N'BladeProfileScanDataPath';   -- 创建时间  EXEC sp_addextendedproperty      @name = N'MS_Description',      @value = N'记录创建时间，默认值为当前系统时间，不可手动修改',      @level0type = N'SCHEMA', @level0name = N'dbo',      @level1type = N'TABLE',  @level1name = N'ProductQualityDataRelation',      @level2type = N'COLUMN', @level2name = N'CreateTime';   -- 修改时间  EXEC sp_addextendedproperty      @name = N'MS_Description',      @value = N'记录最后修改时间，由触发器自动更新为当前系统时间',      @level0type = N'SCHEMA', @level0name = N'dbo',      @level1type = N'TABLE',  @level1name = N'ProductQualityDataRelation',      @level2type = N'COLUMN', @level2name = N'ModifyTime';   -- 创建人  EXEC sp_addextendedproperty      @name = N'MS_Description',      @value = N'记录数据创建人账号，非空，需手动指定',      @level0type = N'SCHEMA', @level0name = N'dbo',      @level1type = N'TABLE',  @level1name = N'ProductQualityDataRelation',      @level2type = N'COLUMN', @level2name = N'Creator';   -- 操作人  EXEC sp_addextendedproperty      @name = N'MS_Description',      @value = N'记录最后修改数据的人员账号，由触发器自动同步',      @level0type = N'SCHEMA', @level0name = N'dbo',      @level1type = N'TABLE',  @level1name = N'ProductQualityDataRelation',      @level2type = N'COLUMN', @level2name = N'Operator';）    2、报告路径维护（维护系统生成的报告放置位置）   这是我能想到的需求，帮我看看哪里不足还需要优化的帮我再检查下


### 需求描述

开发一个 B/S 架构的质量数据处理系统（QDPS），主要功能包括：

1. **用户登录认证**
   - 通过 OA 系统进行身份认证
   - 数据库：192.168.6.88 / ecology / sangfor

2. **尺寸判定功能**
   - 三动全尺寸判定
   - 四动全尺寸判定
   - 五动全尺寸判定
   - 用户选择批次号，系统从数据库查询数据路径，执行判定并生成报告

3. **质量证明单号管理**
   - 编号规则：`QC-XXXXXX(供应商代码)-20XX(年代号)-XXXX(顺序号)`
   - 供应商代码固定：203239
   - 顺序号为4位流水号自动生成
   - 表单显示：`表单编号：QC-______-20___-______`

4. **基础数据维护**
   - 产品检测数据维护（ProductQualityDataRelation 表）
   - 报告路径维护

### 数据库配置

| 系统 | 地址 | 用户 | 数据库 |
|------|------|------|--------|
| OA系统（认证） | 192.168.6.88 | sangfor | ecology |
| QDPS（业务） | 192.168.6.88 | qdsp | qdps |
| MES系统 | 192.168.6.91 | caxa_readonly | caxa_science_mes |

### 数据表结构

**ProductQualityDataRelation（产品质量数据对应关系表）**

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
    CONSTRAINT PK_ProductQualityDataRelation PRIMARY KEY CLUSTERED (SerialNumber, BatchNumber),
    CONSTRAINT UQ_ProductQualityDataRelation_BatchNumber UNIQUE NONCLUSTERED (BatchNumber)
);
```

**QualityCertificate（质量证明单表）**

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

---

## 项目结构

```
qdps/
├── backend/                    # 后端项目 (Flask)
│   ├── app/
│   │   ├── models/            # 数据模型
│   │   ├── routes/            # API 路由
│   │   └── services/          # 业务服务
│   ├── reports/               # 判定报告存储（本地开发）
│   ├── sql/                   # SQL 脚本
│   ├── Dockerfile
│   ├── requirements.txt
│   └── run.py
├── frontend-admin/             # 前端管理后台 (Vue 3)
│   ├── src/
│   │   ├── views/             # 页面组件
│   │   ├── stores/            # Pinia 状态
│   │   ├── router/            # 路由
│   │   └── utils/             # 工具函数
│   ├── Dockerfile
│   ├── nginx.conf
│   └── package.json
├── data/
│   └── reports/               # 判定报告存储（Docker部署）
├── docker-compose.yml          # Docker 编排
├── .gitignore
└── README.md
```

## 目录说明

### 报告存储目录

系统会根据运行环境自动选择报告存储位置：

- **本地开发模式：** `backend/reports/`
  - 执行判定后，Excel 报告保存在此目录
  - 可通过"报告路径维护"功能修改

- **Docker 部署模式：** `data/reports/`
  - 通过 Docker volume 挂载到容器内的 `/app/reports`
  - 报告持久化保存在宿主机，容器重启不丢失

> **注意：** 这两个目录都需要保留，删除会导致报告无法保存

## 功能模块

### 1. 尺寸判定
- 选择批次号后自动获取数据路径
- 执行判定分析，生成 Excel 报告
- 支持下载判定报告

### 2. 质量证明单
- 列表查询（支持筛选）
- 新建/编辑/查看证明单
- 提交/删除操作
- 自动生成单号

### 3. 基础数据维护
- 产品检测数据的增删改查
- 报告存储路径配置

## API 接口

### 认证
- `POST /api/auth/login` - 登录
- `GET /api/auth/userinfo` - 获取用户信息

### 尺寸判定
- `GET /api/dimension/batch-numbers` - 获取批次列表
- `POST /api/dimension/check/{motion-type}` - 执行判定
- `GET /api/dimension/download/{filename}` - 下载报告

### 质量证明单
- `GET /api/certificate/list` - 获取列表
- `POST /api/certificate/create` - 创建
- `PUT /api/certificate/update/{id}` - 更新
- `DELETE /api/certificate/delete/{id}` - 删除

### 维护
- `GET /api/maintenance/product-quality/list` - 产品数据列表
- `POST /api/maintenance/product-quality/create` - 新增
- `PUT /api/maintenance/report-path` - 更新报告路径
