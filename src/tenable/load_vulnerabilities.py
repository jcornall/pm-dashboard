import json
import logging
import mariadb
from uuid_extensions import uuid7
from src.config.constants import VULN_EXPORT_DIR, CONN_PARAMS
from src.tenable.export_vulnerabilities import VulnExportStatus

__INSERT_VULN_PORT_SQL = """
INSERT INTO vulnerability_ports
  (vulnerability_uuid, port, protocol, service)
VALUES (?,?,?,?)
ON DUPLICATE KEY UPDATE port=port;
"""

__INSERT_SCAN_SQL = """
INSERT INTO scans
  (uuid, schedule_uuid, started_at)
VALUES (?, ?, STR_TO_DATE(?, "%Y-%m-%dT%T.%fZ"))
ON DUPLICATE KEY update uuid=uuid;
"""

__INSERT_ASSET_INFO_SQL = """
INSERT INTO vulnerability_asset_infos
  (asset_uuid, agent_uuid, bios_uuid, device_type, fqdn, hostname, ipv4, ipv6, last_authenticated_results, last_unauthenticated_results, mac_address, netbios_name, network_id, tracked)
VALUES (
  ?,?,?,?,?,?,?,?,
  STR_TO_DATE(?, "%Y-%m-%dT%T%.%#Z"),
  STR_TO_DATE(?, "%Y-%m-%dT%T%.%#Z"),
  ?,?,?,?
)
ON DUPLICATE KEY UPDATE asset_uuid=asset_uuid;
"""

__INSERT_VULN_SQL = """
INSERT INTO vulnerabilities
  (uuid, asset_uuid, plugin_id, recast_reason, recast_rule_uuid, scan_uuid, severity, severity_id, severity_default_id, severity_modification_type, first_found, last_fixed, last_found, indexed, state, source)
VALUES (
  ?,?,?,?,?,?,?,?,?,?,
  STR_TO_DATE(?, "%Y-%m-%dT%T%.%#Z"),
  STR_TO_DATE(?, "%Y-%m-%dT%T%.%#Z"),
  STR_TO_DATE(?, "%Y-%m-%dT%T%.%#Z"),
  STR_TO_DATE(?, "%Y-%m-%dT%T%.%#Z"),
  ?,?
);
"""

__INSERT_PLUGIN_SQL = """
INSERT INTO plugins(id, canvas_package, checks_for_default_account, checks_for_malware, cvss3_base_score,
                    cvss3_temporal_score, cvss_base_score, cvss_temporal_score, d2_elliot_name,
                    description, exploit_available, exploit_framework_canvas, exploit_framework_core,
                    exploit_framework_d2_elliot, exploit_framework_exploithub, exploit_framework_metasploit,
                    exploitability_ease, exploited_by_malware, exploited_by_nessus, exploithub_sku, family, family_id,
                    has_patch, in_the_news, metasploit_name, ms_bulletin, name, patch_publication_date,
                    modification_date, publication_date, risk_factor, solution, stig_severity, synopsis, type,
                    unsupported_by_vendor, usn, version, vuln_publication_date)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
        STR_TO_DATE(?, '%Y-%m-%dT%T%.%#Z'), STR_TO_DATE(?, '%Y-%m-%dT%T%.%#Z'),
        STR_TO_DATE(?, '%Y-%m-%dT%T%.%#Z'), ?, ?, ?, ?, ?, ?,
        ?, ?, STR_TO_DATE(?, '%Y-%m-%dT%T%.%#Z'))
ON DUPLICATE KEY UPDATE id=id;
"""

__INSERT_PLUGIN_CVSS3_VECTOR = """
INSERT INTO plugin_cvss3_vectors(plugin_id, access_vector, access_complexity, authentication,
                                 confidentiality_impact, integrity_impact, availability_impact, raw)
VALUES (?, ?, ?, ?, ?, ?, ?, ?)
ON DUPLICATE KEY UPDATE plugin_id=plugin_id;
"""

__INSERT_PLUGIN_CVSS3_TEMPORAL_VECTOR = """
INSERT INTO plugin_cvss3_temporal_vectors(plugin_id, exploitability, remediation_level, report_confidence, raw)
VALUES (?, ?, ?, ?, ?)
ON DUPLICATE KEY UPDATE plugin_id=plugin_id;
"""

__INSERT_PLUGIN_CVSS_TEMPORAL_VECTOR = """
INSERT INTO plugin_cvss_temporal_vectors(plugin_id, exploitability, remediation_level, report_confidence, raw)
VALUES (?, ?, ?, ?, ?)
ON DUPLICATE KEY UPDATE plugin_id=plugin_id;
"""

__INSERT_PLUGIN_CVSS_VECTOR = """
INSERT INTO plugin_cvss_vectors(plugin_id, access_vector, access_complexity, authentication,
                                 confidentiality_impact, integrity_impact, availability_impact, raw)
VALUES (?, ?, ?, ?, ?, ?, ?, ?)
ON DUPLICATE KEY UPDATE plugin_id=plugin_id;
"""

__INSERT_PLUGIN_VPR = """
INSERT INTO plugin_vprs(plugin_id, score, updated)
VALUES (?, ?, STR_TO_DATE(?, "%Y-%m-%dT%T%.%#Z"))
ON DUPLICATE KEY UPDATE plugin_id=plugin_id;
"""


def load_tenable_vulnerabilities(export: VulnExportStatus):
    """Loads all vulnerabilities within the given export to the database"""

    conn = mariadb.connect(**CONN_PARAMS)

    for chunk_id in export.chunks_available:
        with open(VULN_EXPORT_DIR / export.chunk_file_name(chunk_id), "r") as f:
            logging.info(
                f"loading chunk {chunk_id} of vuln_export {export.uuid} into database..."
            )
            chunk_json = f.read()

            try:
                conn.begin()
                cursor = conn.cursor()

                __load_single_chunk(chunk_json, cursor)

                conn.commit()

                logging.info(
                    f"chunk {chunk_id} of vuln_export {export.uuid} loaded successfully."
                )
            except Exception as e:
                conn.rollback()
                raise e


def __load_single_chunk(chunk_json_str: str, cursor: mariadb.Cursor):
    json_data = json.loads(chunk_json_str)

    for vuln in json_data:
        vuln_id = uuid7()

        scan_info = vuln["scan"]
        cursor.execute(
            __INSERT_SCAN_SQL,
            [scan_info["uuid"], scan_info["schedule_uuid"], scan_info["started_at"]],
        )

        asset = vuln["asset"]
        cursor.execute(
            __INSERT_ASSET_INFO_SQL,
            [
                asset.get("uuid"),
                asset.get("agent_uuid"),
                asset.get("bios_uuid"),
                asset.get("device_type"),
                asset.get("fqdn"),
                asset.get("hostname"),
                asset.get("ipv4"),
                asset.get("ipv6"),
                asset.get("last_authenticated_results"),
                asset.get("last_unauthenticated_results"),
                asset.get("mac_address"),
                asset.get("netbios_name"),
                asset.get("network_id"),
                asset.get("tracked"),
            ],
        )

        plugin = vuln["plugin"]
        plugin_id = plugin.get("id")
        cursor.execute(
            __INSERT_PLUGIN_SQL,
            [
                plugin_id,
                plugin.get("canvas_package"),
                plugin.get("checks_for_default_account"),
                plugin.get("checks_for_malware"),
                plugin.get("cvss3_base_score"),
                plugin.get("cvss3_temporal_score"),
                plugin.get("cvss_base_score"),
                plugin.get("cvss_temporal_score"),
                plugin.get("d2_elliot_name"),
                plugin.get("description"),
                plugin.get("exploit_available"),
                plugin.get("exploit_framework_canvas"),
                plugin.get("exploit_framework_core"),
                plugin.get("exploit_framework_d2_elliot"),
                plugin.get("exploit_framework_exploithub"),
                plugin.get("exploit_framework_metasploit"),
                plugin.get("exploitability_ease"),
                plugin.get("exploited_by_malware"),
                plugin.get("exploited_by_nessus"),
                plugin.get("exploithub_sku"),
                plugin.get("family"),
                plugin.get("family_id"),
                plugin.get("has_patch"),
                plugin.get("in_the_news"),
                plugin.get("metasploit_name"),
                plugin.get("ms_bulletin"),
                plugin.get("name"),
                plugin.get("patch_publication_date"),
                plugin.get("modification_date"),
                plugin.get("publication_date"),
                plugin.get("risk_factor"),
                plugin.get("solution"),
                plugin.get("stig_severity"),
                plugin.get("synopsis"),
                plugin.get("type"),
                plugin.get("unsupported_by_vendor"),
                plugin.get("usn"),
                plugin.get("version"),
                plugin.get("vuln_publication_date"),
            ],
        )

        plugin_cvss3_temporal_vector = plugin.get("cvss3_temporal_vector")
        if plugin_cvss3_temporal_vector:
            cursor.execute(
                __INSERT_PLUGIN_CVSS3_TEMPORAL_VECTOR,
                [
                    plugin_id,
                    plugin_cvss3_temporal_vector.get("exploitability"),
                    plugin_cvss3_temporal_vector.get("remediation_level"),
                    plugin_cvss3_temporal_vector.get("report_confidence"),
                    plugin_cvss3_temporal_vector.get("raw"),
                ],
            )

        plugin_cvss3_vector = plugin.get("cvss3_vector")
        if plugin_cvss3_vector:
            cursor.execute(
                __INSERT_PLUGIN_CVSS3_VECTOR,
                [
                    plugin_id,
                    plugin_cvss3_vector.get("access_vector"),
                    plugin_cvss3_vector.get("access_complexity"),
                    plugin_cvss3_vector.get("authentication"),
                    plugin_cvss3_vector.get("confidentiality_impact"),
                    plugin_cvss3_vector.get("integrity_impact"),
                    plugin_cvss3_vector.get("availability_impact"),
                    plugin_cvss3_vector.get("raw"),
                ],
            )

        plugin_cvss_temporal_vector = plugin.get("cvss_temporal_vector")
        if plugin_cvss_temporal_vector:
            cursor.execute(
                __INSERT_PLUGIN_CVSS_TEMPORAL_VECTOR,
                [
                    plugin_id,
                    plugin_cvss_temporal_vector.get("exploitability"),
                    plugin_cvss_temporal_vector.get("remediation_level"),
                    plugin_cvss_temporal_vector.get("report_confidence"),
                    plugin_cvss_temporal_vector.get("raw"),
                ],
            )

        plugin_cvss_vector = plugin.get("cvss_vector")
        if plugin_cvss_vector:
            cursor.execute(
                __INSERT_PLUGIN_CVSS_VECTOR,
                [
                    plugin_id,
                    plugin_cvss_vector.get("access_vector"),
                    plugin_cvss_vector.get("access_complexity"),
                    plugin_cvss_vector.get("authentication"),
                    plugin_cvss_vector.get("confidentiality_impact"),
                    plugin_cvss_vector.get("integrity_impact"),
                    plugin_cvss_vector.get("availability_impact"),
                    plugin_cvss_vector.get("raw"),
                ],
            )

        plugin_vpr = plugin.get("vpr")
        if plugin_vpr:
            cursor.execute(
                __INSERT_PLUGIN_VPR,
                [plugin_id, plugin_vpr.get("score"), plugin_vpr.get("updated")],
            )

        bid = plugin.get("bid")
        if bid and len(bid) > 0:
            cursor.executemany(
                "INSERT INTO plugin_bugtraqs(plugin_id, bugtraq_id) VALUES (?,?) "
                "ON DUPLICATE KEY UPDATE plugin_id=plugin_id;",
                [(plugin_id, id) for id in bid],
            )

        cpes = plugin.get("cpe")
        if cpes and len(cpes) > 0:
            cursor.executemany(
                "INSERT INTO plugin_cpes(plugin_id, cpe) VALUES (?,?) "
                "ON DUPLICATE KEY UPDATE plugin_id=plugin_id;",
                [(plugin_id, cpe) for cpe in cpes],
            )

        cves = plugin.get("cve")
        if cves and len(cves) > 0:
            cursor.executemany(
                "INSERT INTO plugin_cves(plugin_id, cve) VALUES (?,?) "
                "ON DUPLICATE KEY UPDATE plugin_id=plugin_id;",
                [(plugin_id, cve) for cve in cves],
            )

        cursor.execute(
            __INSERT_VULN_SQL,
            [
                vuln_id,
                asset.get("uuid"),
                plugin_id,
                vuln.get("recast_reason"),
                vuln.get("recast_rule_uuid"),
                scan_info.get("uuid"),
                vuln.get("severity"),
                vuln.get("severity_id"),
                vuln.get("severity_default_id"),
                vuln.get("severity_modification_type"),
                vuln.get("first_found"),
                vuln.get("last_fixed"),
                vuln.get("last_found"),
                vuln.get("indexed"),
                vuln.get("state"),
                vuln.get("source"),
            ],
        )

        port_info = vuln["port"]
        cursor.execute(
            __INSERT_VULN_PORT_SQL,
            [
                vuln_id,
                port_info.get("port"),
                port_info.get("protocol"),
                port_info.get("service"),
            ],
        )
