DELETE FROM vulnerabilities_export
WHERE created_on > DATE(CURRENT_TIMESTAMP);