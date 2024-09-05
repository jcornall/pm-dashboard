INSERT INTO vuln_timeseries (
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
asset_tracked, asset_uuid,
first_found,
indexed,
last_fixed,
last_found,
plugin_bid_0,
plugin_canvas_package,
plugin_checks_for_default_account,
plugin_checks_for_malware,
plugin_cvss3_base_score,
plugin_cvss3_temporal_score,
plugin_cvss3_temporal_vector,
plugin_cvss3_temporal_vector_exploitability,
plugin_cvss3_temporal_vector_raw,
plugin_cvss3_temporal_vector_remediation_level, plugin_cvss3_temporal_vector_report_confidence,
plugin_cvss3_vector_access_complexity,
plugin_cvss3_vector_access_vector,
plugin_cvss3_vector_availability_impact,
plugin_cvss3_vector_confidentiality_impact,
plugin_cvss3_vector_integrity_impact,
plugin_cvss3_vector_raw,
plugin_cvss_base_score,
plugin_cvss_temporal_score,
plugin_cvss_temporal_vector,
plugin_cvss_temporal_vector_exploitability,
plugin_cvss_temporal_vector_raw,
plugin_cvss_temporal_vector_remediation_level,
plugin_cvss_temporal_vector_report_confidence,
plugin_cvss_vector_access_complexity,
plugin_cvss_vector_access_vector,
plugin_cvss_vector_authentication,
plugin_cvss_vector_availability_impact,
plugin_cvss_vector_confidentiality_impact,
plugin_cvss_vector_integrity_impact,
plugin_cvss_vector_raw,
plugin_d2_elliot_name,
plugin_exploit_available,
plugin_exploit_framework_canvas,
plugin_exploit_framework_core,
plugin_exploit_framework_d2_elliot,
plugin_exploit_framework_exploithub,
plugin_exploit_framework_metasploit,
plugin_exploitability_ease,
plugin_exploited_by_malware,
plugin_exploited_by_nessus,
plugin_family,
plugin_family_id,
plugin_has_patch,
plugin_id,
plugin_in_the_news,
plugin_metasploit_name,
plugin_modification_date,
plugin_name,
plugin_patch_publication_date,
plugin_publication_date,
plugin_risk_factor,
plugin_solution,
plugin_stig_severity,
plugin_synopsis,
plugin_type,
plugin_unsupported_by_vendor,
plugin_version,
plugin_vpr_drivers_age_of_vuln_lower_bound,
plugin_vpr_drivers_age_of_vuln_upper_bound,
plugin_vpr_drivers_cvss3_impact_score,
plugin_vpr_drivers_cvss_impact_score_predicted,
plugin_vpr_drivers_exploit_code_maturity,
plugin_vpr_drivers_product_coverage,
plugin_vpr_drivers_threat_intensity_last28,
plugin_vpr_drivers_threat_recency_lower_bound,
plugin_vpr_drivers_threat_recency_upper_bound,
plugin_vpr_drivers_threat_sources_last28_0,
plugin_vpr_drivers_threat_sources_last28_1,
plugin_vpr_score,
plugin_vpr_updated,
plugin_vuln_publication_date,
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
    SELECT * FROM vuln_timeseries
    WHERE vuln_export.created_on = vuln_timeseries.created_on 
);