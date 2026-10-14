-- ============================================================================
--  AtliQ Commerce  |  File Control Table (metadata-driven CSV ingestion)
--  One row per source file. The Azure Data Factory pipeline reads this table
--  and decides WHAT file to ingest and WHERE to load it:
--    * load_type = 'FULL'         -> load the entire file every run
--    * load_type = 'INCREMENTAL'  -> load only new/changed records
--                                   (if incremental logic is implemented)
--    * is_active = 1              -> file is included in pipeline execution
--    * is_active = 0              -> file is skipped
--  This metadata-driven approach allows ONE generic pipeline to process
--  multiple CSV files without hardcoding file-specific logic.
-- ============================================================================

IF SCHEMA_ID('dbo') IS NULL EXEC('CREATE SCHEMA dbo;');
GO

IF OBJECT_ID('dbo.file_control_table', 'U') IS NOT NULL
    DROP TABLE dbo.file_control_table;
GO

CREATE TABLE dbo.file_control_table (
    id               INT IDENTITY(1,1) NOT NULL,
    sourcefilename   VARCHAR(100) NOT NULL,
    sourcefolder     VARCHAR(200) NOT NULL,
    targetfolder     VARCHAR(200) NOT NULL,
    loadtype         VARCHAR(20)  NOT NULL,
    isactive         BIT NOT NULL CONSTRAINT DF_file_ctl_active DEFAULT 1,

    CONSTRAINT PK_file_control_table PRIMARY KEY (id),
    CONSTRAINT CK_file_ctl_loadtype CHECK (loadtype IN ('FULL', 'INCREMENTAL'))
);
GO

INSERT INTO dbo.file_control_table
(
    sourcefilename,
    sourcefolder,
    targetfolder,
    loadtype,
    isactive
)
VALUES
(
    'marketing_spend.csv',
    'landing/marketing_spend/',
    'bronze/marketing_spend/',
    'FULL',
    1
),
(
    'supplier_price_list.csv',
    'landing/supplier_price_list/',
    'bronze/supplier_price_list/',
    'FULL',
    1
);
GO

PRINT 'File control table created and seeded successfully.';
GO