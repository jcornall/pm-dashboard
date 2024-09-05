INSERT INTO vuln_vulnerabilities (
e_id,
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
SELECT DISTINCT * FROM vuln_export
WHERE NOT EXISTS (
    SELECT * FROM vuln_vulnerabilities
    WHERE vuln_export.created_on = vuln_vulnerabilities.created_on
);