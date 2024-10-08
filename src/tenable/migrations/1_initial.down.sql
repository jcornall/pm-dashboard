BEGIN;

DROP TABLE IF EXISTS tenable.asset_fqdns;
DROP TABLE IF EXISTS tenable.asset_hostnames;
DROP TABLE IF EXISTS tenable.asset_installed_softwares;
DROP TABLE IF EXISTS tenable.asset_ipv4_addresses;
DROP TABLE IF EXISTS tenable.asset_ipv6_addresses;
DROP TABLE IF EXISTS tenable.asset_mac_addresses;
DROP TABLE IF EXISTS tenable.asset_manufacturer_tpm_ids;
DROP TABLE IF EXISTS tenable.asset_netbios_names;
DROP TABLE IF EXISTS tenable.asset_operating_systems;
DROP TABLE IF EXISTS tenable.asset_qualys_asset_ids;
DROP TABLE IF EXISTS tenable.asset_qualys_host_ids;
DROP TABLE IF EXISTS tenable.asset_sources;
DROP TABLE IF EXISTS tenable.asset_ssh_fingerprints;
DROP TABLE IF EXISTS tenable.asset_symantec_ep_hardware_keys;
DROP TABLE IF EXISTS tenable.asset_system_types;
DROP TABLE IF EXISTS tenable.asset_tags;
DROP TABLE IF EXISTS tenable.assets;
DROP TABLE IF EXISTS tenable.plugin_bugtraqs;
DROP TABLE IF EXISTS tenable.plugin_cpes;
DROP TABLE IF EXISTS tenable.plugin_cves;
DROP TABLE IF EXISTS tenable.plugin_cvss3_temporal_vectors;
DROP TABLE IF EXISTS tenable.plugin_cvss3_vectors;
DROP TABLE IF EXISTS tenable.plugin_cvss_temporal_vectors;
DROP TABLE IF EXISTS tenable.plugin_cvss_vectors;
DROP TABLE IF EXISTS tenable.plugin_vprs;
DROP TABLE IF EXISTS tenable.plugins;
DROP TABLE IF EXISTS tenable.scans;
DROP TABLE IF EXISTS tenable.vulnerabilities;
DROP TABLE IF EXISTS tenable.vulnerability_asset_infos;
DROP TABLE IF EXISTS tenable.vulnerability_ports;

COMMIT;
