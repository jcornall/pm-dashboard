INSERT INTO vuln_vulnerabilities (
vulnerability_id,
created_on,
first_found,
indexed,
last_fixed,
last_found,
port_port,
port_protocol,
port_service,
recast_reason,
recast_rule_uuid,
scan_schedule_uuid,
scan_started_at,
scan_uuid,
severity,
severity_default_id,
severity_id,
severity_modification_type,
source,
state
)
SELECT DISTINCT * FROM vulnerabilities_export
WHERE NOT EXISTS (
    SELECT * FROM vulnerabilities_timeseries
    WHERE vulnerabilities_export.created_on = vulnerabilities_timeseries.created_on 
);