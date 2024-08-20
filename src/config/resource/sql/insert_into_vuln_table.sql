INSERT INTO vulnerabilities_timeseries
SELECT * FROM vulnerabilities_export
WHERE NOT EXISTS (
    SELECT * FROM vulnerabilities_timeseries
    WHERE (
        vulnerabilities_export.created_on = vulnerabilities_timeseries.created_on AND
        vulnerabilities_export.asset_fqdn = vulnerabilities_timeseries.asset_fqdn AND
        vulnerabilities_export.asset_ipv4 = vulnerabilities_timeseries.asset_ipv4 AND
        vulnerabilities_export.plugin_name = vulnerabilities_timeseries.plugin_name
    )
);