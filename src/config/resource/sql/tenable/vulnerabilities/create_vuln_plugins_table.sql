CREATE TABLE IF NOT EXISTS vuln_plugins (
vulnerability_id INT AUTO_INCREMENT NOT NULL,
created_on DATE DEFAULT DATE(CURRENT_TIMESTAMP),
plugin_bid_0 INT,
plugin_canvas_package VARCHAR(16),
plugin_checks_for_default_account VARCHAR(16),
plugin_checks_for_malware VARCHAR(16),
plugin_cvss3_base_score DECIMAL(10,1),
plugin_cvss3_temporal_score DECIMAL(10,1),
plugin_cvss3_temporal_vector VARCHAR(8),
plugin_cvss3_temporal_vector_exploitability VARCHAR(32),
plugin_cvss3_temporal_vector_raw VARCHAR(32),
plugin_cvss3_temporal_vector_remediation_level VARCHAR(32),
plugin_cvss3_temporal_vector_report_confidence VARCHAR(16),
plugin_cvss3_vector_access_complexity VARCHAR(8),
plugin_cvss3_vector_access_vector VARCHAR(32),
plugin_cvss3_vector_availability_impact VARCHAR(8),
plugin_cvss3_vector_confidentiality_impact VARCHAR(8),
plugin_cvss3_vector_integrity_impact VARCHAR(8),
plugin_cvss3_vector_raw VARCHAR(64),
plugin_cvss_base_score DECIMAL(10,1),
plugin_cvss_temporal_score DECIMAL(10,1),
plugin_cvss_temporal_vector VARCHAR(8),
plugin_cvss_temporal_vector_exploitability VARCHAR(32),
plugin_cvss_temporal_vector_raw VARCHAR(32),
plugin_cvss_temporal_vector_remediation_level VARCHAR(32),
plugin_cvss_temporal_vector_report_confidence VARCHAR(16),
plugin_cvss_vector_access_complexity VARCHAR(16),
plugin_cvss_vector_access_vector VARCHAR(32),
plugin_cvss_vector_authentication VARCHAR(16),
plugin_cvss_vector_availability_impact VARCHAR(16),
plugin_cvss_vector_confidentiality_impact VARCHAR(16),
plugin_cvss_vector_integrity_impact VARCHAR(16),
plugin_cvss_vector_raw VARCHAR(32),
plugin_d2_elliot_name VARCHAR(128),
plugin_exploit_available VARCHAR(8),
plugin_exploit_framework_canvas VARCHAR(8),
plugin_exploit_framework_core VARCHAR(8),
plugin_exploit_framework_d2_elliot VARCHAR(8),
plugin_exploit_framework_exploithub VARCHAR(8),
plugin_exploit_framework_metasploit VARCHAR(8),
plugin_exploitability_ease VARCHAR(64),
plugin_exploited_by_malware VARCHAR(8),
plugin_exploited_by_nessus VARCHAR(8),
plugin_family VARCHAR(64),
plugin_family_id INT,
plugin_has_patch VARCHAR(8),
plugin_id INT,
plugin_in_the_news VARCHAR(8),
plugin_metasploit_name VARCHAR(128),
plugin_modification_date DATETIME,
plugin_name VARCHAR(256),
plugin_patch_publication_date DATETIME,
plugin_publication_date DATETIME,
plugin_risk_factor VARCHAR(16),
plugin_solution VARCHAR(512),
plugin_stig_severity VARCHAR(4),
plugin_synopsis VARCHAR(256),
plugin_type VARCHAR(16),
plugin_unsupported_by_vendor VARCHAR(8),
plugin_version DECIMAL(10,1),
plugin_vpr_drivers_age_of_vuln_lower_bound INT,
plugin_vpr_drivers_age_of_vuln_upper_bound INT,
plugin_vpr_drivers_cvss3_impact_score DECIMAL(10,1),
plugin_vpr_drivers_cvss_impact_score_predicted VARCHAR(8),
plugin_vpr_drivers_exploit_code_maturity VARCHAR(32),
plugin_vpr_drivers_product_coverage VARCHAR(16),
plugin_vpr_drivers_threat_intensity_last28 VARCHAR(16),
plugin_vpr_drivers_threat_recency_lower_bound INT,
plugin_vpr_drivers_threat_recency_upper_bound INT,
plugin_vpr_drivers_threat_sources_last28_0 VARCHAR(64),
plugin_vpr_drivers_threat_sources_last28_1 VARCHAR(64),
plugin_vpr_score DECIMAL(10,1),
plugin_vpr_updated DATETIME,
plugin_vuln_publication_date DATETIME,
PRIMARY KEY (vulnerability_id)
);