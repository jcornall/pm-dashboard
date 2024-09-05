INSERT INTO vuln_assets (
    e_id,
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
    asset_tracked, 
    asset_uuid
)
SELECT DISTINCT 
    e_id,
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
    asset_tracked, 
    asset_uuid 
FROM vuln_export
WHERE NOT EXISTS (
    SELECT * FROM vuln_assets
    WHERE vuln_export.created_on = vuln_assets.created_on
);