BEGIN;

DROP TABLE IF EXISTS vulnerabilities;
DROP TABLE IF EXISTS assets;
DROP TABLE IF EXISTS asset_os;
DROP TABLE IF EXISTS scans;
DROP TABLE IF EXISTS vulnerability_ports;
DROP TABLE IF EXISTS plugins;
DROP TABLE IF EXISTS plugin_vprs;
DROP TABLE IF EXISTS plugin_cvss_vectors;
DROP TABLE IF EXISTS plugin_cvss3_vectors;
DROP TABLE IF EXISTS plugin_cvss_temporal_vectors;
DROP TABLE IF EXISTS plugin_cvss3_temporal_vectors;
DROP TABLE IF EXISTS plugin_bugtraqs;
DROP TABLE IF EXISTS plugin_cpes;
DROP TABLE IF EXISTS plugin_cves;

COMMIT;
