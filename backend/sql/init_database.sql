-- QDPS 质量数据处理系统 - 数据库初始化脚本 (SQL Server)

-- 1. 产品质量数据对应关系表
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='ProductQualityDataRelation' AND xtype='U')
BEGIN
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
END
GO

-- 2. 质量证明单表
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='QualityCertificate' AND xtype='U')
BEGIN
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
    CREATE INDEX IX_QualityCertificate_BatchNumber ON QualityCertificate(BatchNumber);
    CREATE INDEX IX_QualityCertificate_Status ON QualityCertificate(Status);
END
GO

-- 3. 系统配置表
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='SystemConfig' AND xtype='U')
BEGIN
    CREATE TABLE SystemConfig (
        Id INT IDENTITY(1,1) PRIMARY KEY,
        ConfigKey VARCHAR(100) NOT NULL UNIQUE,
        ConfigValue NVARCHAR(500) NULL,
        ConfigType VARCHAR(50) NULL,
        Description NVARCHAR(200) NULL,
        CreateTime DATETIME DEFAULT GETDATE() NOT NULL,
        ModifyTime DATETIME NULL,
        Operator VARCHAR(50) NULL
    );
END
GO

-- 4. 初始化配置
IF NOT EXISTS (SELECT * FROM SystemConfig WHERE ConfigKey = 'REPORT_BASE_PATH')
BEGIN
    INSERT INTO SystemConfig (ConfigKey, ConfigValue, ConfigType, Description, Operator)
    VALUES ('REPORT_BASE_PATH', '/app/reports', 'PATH', '报告文件存储路径', 'system');
END
GO

PRINT 'Database initialization completed!';
