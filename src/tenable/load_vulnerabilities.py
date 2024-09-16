import json
import logging
import mariadb
from uuid_extensions import uuid7
from src.config.constants import CONN_PARAMS, VULN_EXPORT_DIR
from src.tenable.export_vulnerabilities import VulnExportStatus

__INSERT_VULN_PORT_SQL = """
INSERT INTO vulnerability_ports
  (vulnerability_uuid, port, protocol, service)
VALUES (?,?,?,?);
"""

__INSERT_SCAN_SQL = """
INSERT INTO scans
  (uuid, schedule_uuid, started_at)
VALUES (?,?,?);
"""

__INSERT_ASSET_SQL = """
INSERT INTO assets
  (uuid, agent_uuid, bios_uuid, device_type, fqdn, hostname, ipv4, ipv6, last_authenticated_results, last_unauthenticated_results, mac_address, netbios_name, network_id, tracked)
VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?);
ON DUPLICATE KEY uuid=uuid; # do nothing when there is an existing entry for asset with the same id
"""

__INSERT_VULN_SQL = """
INSERT INTO vulnerabilities
  (uuid, asset_uuid, recast_reason, recast_rule_uuid, scan_uuid, severity, severity_id, severity_default_id, severity_modification_type, first_found, last_fixed, last_found, indexed, state, source)
VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);
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
            __INSERT_ASSET_SQL,
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

        cursor.execute(
            __INSERT_VULN_SQL,
            [
                vuln_id,
                asset.get("uuid"),
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
