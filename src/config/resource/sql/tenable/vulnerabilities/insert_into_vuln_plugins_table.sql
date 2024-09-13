INSERT INTO vuln_plugins (
    e_id,
    created_on,
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
    plugin_vuln_publication_date
)
SELECT DISTINCT
        e_id,
    created_on,
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
    plugin_vuln_publication_date
FROM vuln_export
WHERE NOT EXISTS (
    SELECT * FROM vuln_plugins
    WHERE vuln_export.created_on = vuln_plugins.created_on
);