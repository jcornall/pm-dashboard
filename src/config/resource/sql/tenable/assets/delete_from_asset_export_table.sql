DELETE FROM asset_export
WHERE created_on < DATE(CURRENT_TIMESTAMP);