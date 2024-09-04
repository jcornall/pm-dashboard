INSERT INTO vuln_assets (
vulnerability_id,
created_on,
asset_agent_uuid,
asset_bios_uuid,
asset_device_type,
asset_fqdn,
asset_hostname,
asset_ipv4,
asset_ipv6,
asset_last_authenticated_results,
asset_mac_address,
asset_netbios_name,
asset_network_id,
asset_operating_system_0,
asset_operating_system_1,
asset_operating_system_2,
asset_operating_system_3,
asset_tracked, asset_uuid
)
SELECT DISTINCT * FROM vulnerabilities_export
WHERE NOT EXISTS (
    SELECT * FROM vulnerabilities_timeseries
    WHERE vulnerabilities_export.created_on = vulnerabilities_timeseries.created_on 
);