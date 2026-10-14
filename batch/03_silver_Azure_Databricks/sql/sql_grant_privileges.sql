GRANT USE SCHEMA ON SCHEMA atliq_dbx.gold_gold TO `<user>`;
GRANT SELECT ON SCHEMA atliq_dbx.gold_gold TO `<user>`;
GRANT EXTERNAL USE SCHEMA ON SCHEMA atliq_dbx.gold_gold TO `<user>`;

show catalogs;

GRANT USAGE ON CATALOG atliq_dbx TO `<user>`;
GRANT USAGE ON SCHEMA gold_gold TO `<user>`;
GRANT USE ON CATALOG atliq_dbx TO `<user>`;
GRANT USE ON SCHEMA gold_gold TO `<user>`;
GRANT SELECT ON TABLE atliq_dbx.gold_gold.fact_orders TO `<user>`;
GRANT SELECT ON TABLE atliq_dbx.gold_gold.dim_customer TO `<user>`;
GRANT SELECT ON TABLE atliq_dbx.gold_gold.dim_product TO `<user>`;
GRANT SELECT ON TABLE atliq_dbx.gold_gold.dim_date TO `<user>`;

--CREATE EXTERNAL LOCATION atliq_gold_loc
--URL 'abfss://gold@atliqdatalake.dfs.core.windows.net/'
--WITH STORAGE CREDENTIAL atliq_sc;

--GRANT USE SCHEMA ON SCHEMA atliq_dbx.gold_gold TO `fabric-dbx-mirror-sp`;




