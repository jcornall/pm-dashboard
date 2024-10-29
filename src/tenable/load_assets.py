import json
from mariadb import mariadb
from src.config.constants import ASSET_EXPORT_DIR, CONN_PARAMS
from src.tenable.export_assets import AssetExportStatus

INSERT_ASSET_SQL = """
INSERT INTO assets(uuid, has_plugin_results, created_at, terminated_at, terminated_by, updated_at, deleted_at,
                   deleted_by, first_seen, last_seen, first_scan_time, last_scan_time, last_authenticated_scan_date,
                   last_licensed_scan_date, last_scan_id, last_schedule_id, azure_vm_id, azure_resource_id,
                   gcp_project_id, gcp_zone, gcp_instance_id, aws_ec2_instance_ami_id, aws_ec2_instance_id, agent_uuid,
                   bios_uuid, network_id, network_name, aws_owner_id, aws_availability_zone, aws_region, aws_vpc_id,
                   aws_ec2_instance_group_name, aws_ec2_instance_state_name, aws_ec2_instance_type, aws_subnet_id,
                   aws_ec2_product_code, aws_ec2_name, mcafee_epo_guid, mcafee_epo_agent_guid, servicenow_sysid,
                   bigfix_asset_id, device_type, last_authenticated_results, last_unauthenticated_results, tracked,
                   acr_score, exposure_score)
VALUES (?, ?, STR_TO_DATE(?, "%Y-%m-%dT%T.%fZ"), STR_TO_DATE(?, "%Y-%m-%dT%T.%fZ"), ?,
        STR_TO_DATE(?, "%Y-%m-%dT%T.%fZ"), STR_TO_DATE(?, "%Y-%m-%dT%T.%fZ"), ?, STR_TO_DATE(?, "%Y-%m-%dT%T.%fZ"),
        STR_TO_DATE(?, "%Y-%m-%dT%T.%fZ"), STR_TO_DATE(?, "%Y-%m-%dT%T.%fZ"), STR_TO_DATE(?, "%Y-%m-%dT%T.%fZ"),
        STR_TO_DATE(?, "%Y-%m-%dT%T.%fZ"), STR_TO_DATE(?, "%Y-%m-%dT%T.%fZ"), ?, ?, ?, ?, ?, ?, ?,
        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
        ?, ?, ?, ?, ?, STR_TO_DATE(?, "%Y-%m-%dT%T.%fZ"), STR_TO_DATE(?, "%Y-%m-%dT%T.%fZ"), ?, ?, ?)
ON DUPLICATE KEY UPDATE uuid=uuid;"""


def load_tenable_assets(export: AssetExportStatus):
    conn = mariadb.connect(**CONN_PARAMS)

    for chunk_id in export.chunks_available:
        with open(ASSET_EXPORT_DIR / export.chunk_file_name(chunk_id)) as f:
            chunk_json = f.read()

            try:
                conn.begin()
                cursor = conn.cursor()

                __load_single_chunk(chunk_json, cursor)

                conn.commit()
            except Exception as e:
                conn.rollback()
                raise e


def __load_single_chunk(chunk_json_str: str, cursor: mariadb.Cursor):
    chunk_data = json.loads(chunk_json_str)

    for asset in chunk_data:
        asset_uuid = asset["id"]

        cursor.execute(
            INSERT_ASSET_SQL,
            [
                asset_uuid,
                asset.get("has_plugin_results"),
                asset.get("created_at"),
                asset.get("terminated_at"),
                asset.get("terminated_by"),
                asset.get("updated_at"),
                asset.get("deleted_at"),
                asset.get("deleted_by"),
                asset.get("first_seen"),
                asset.get("last_seen"),
                asset.get("first_scan_time"),
                asset.get("last_scan_time"),
                asset.get("last_authenticated_scan_date"),
                asset.get("last_licensed_scan_date"),
                asset.get("last_scan_id"),
                asset.get("last_schedule_id"),
                asset.get("azure_vm_id"),
                asset.get("azure_resource_id"),
                asset.get("gcp_project_id"),
                asset.get("gcp_zone"),
                asset.get("gcp_instance_id"),
                asset.get("aws_ec2_instance_ami_id"),
                asset.get("aws_ec2_instance_id"),
                asset.get("agent_uuid"),
                asset.get("bios_uuid"),
                asset.get("network_id"),
                asset.get("network_name"),
                asset.get("aws_owner_id"),
                asset.get("aws_availability_zone"),
                asset.get("aws_region"),
                asset.get("aws_vpc_id"),
                asset.get("aws_ec2_instance_group_name"),
                asset.get("aws_ec2_instance_state_name"),
                asset.get("aws_ec2_instance_type"),
                asset.get("aws_subnet_id"),
                asset.get("aws_ec2_product_code"),
                asset.get("aws_ec2_name"),
                asset.get("mcafee_epo_guid"),
                asset.get("mcafee_epo_agent_guid"),
                asset.get("servicenow_sysid"),
                asset.get("bigfix_asset_id"),
                asset.get("device_type"),
                asset.get("last_authenticated_results"),
                asset.get("last_unauthenticated_results"),
                asset.get("tracked"),
                asset.get("acr_score"),
                asset.get("exposure_score"),
            ],
        )

        installed_software = asset.get("installed_software")
        if installed_software and len(installed_software) > 0:
            cursor.executemany(
                "INSERT INTO asset_installed_softwares(asset_uuid, software_cpe) VALUES (?,?) "
                "ON DUPLICATE KEY UPDATE asset_uuid=asset_uuid;",
                [(asset_uuid, cpe) for cpe in installed_software],
            )

        ipv4s = asset.get("ipv4s")
        if ipv4s and len(ipv4s) > 0:
            cursor.executemany(
                "INSERT INTO asset_ipv4_addresses(asset_uuid, ipv4) VALUES (?,?) "
                "ON DUPLICATE KEY UPDATE asset_uuid=asset_uuid;",
                [(asset_uuid, ip) for ip in ipv4s],
            )

        ipv6s = asset.get("ipv6s")
        if ipv6s and len(ipv6s) > 0:
            cursor.executemany(
                "INSERT INTO asset_ipv6_addresses(asset_uuid, ipv6) VALUES (?,?) "
                "ON DUPLICATE KEY UPDATE asset_uuid=asset_uuid;",
                [(asset_uuid, ip) for ip in ipv6s],
            )

        fqdns = asset.get("fqdns")
        if fqdns and len(fqdns) > 0:
            cursor.executemany(
                "INSERT INTO asset_fqdns(asset_uuid, fqdn) VALUES(?,?) "
                "ON DUPLICATE KEY UPDATE asset_uuid=asset_uuid;",
                [(asset_uuid, fqdn) for fqdn in fqdns],
            )

        mac_addresses = asset.get("mac_addresses")
        if mac_addresses and len(mac_addresses) > 0:
            cursor.executemany(
                "INSERT INTO asset_mac_addresses(asset_uuid, mac_address) VALUES (?,?) "
                "ON DUPLICATE KEY UPDATE asset_uuid=asset_uuid;",
                [(asset_uuid, mac) for mac in mac_addresses],
            )

        netbios_names = asset.get("netbios_names")
        if netbios_names and len(netbios_names) > 0:
            cursor.executemany(
                "INSERT INTO asset_netbios_names(asset_uuid, netbios_name) VALUES (?,?) "
                "ON DUPLICATE KEY UPDATE asset_uuid=asset_uuid;",
                [(asset_uuid, name) for name in netbios_names],
            )

        operating_systems = asset.get("operating_systems")
        if operating_systems and len(operating_systems) > 0:
            cursor.executemany(
                "INSERT INTO asset_operating_systems(asset_uuid, operating_system) VALUES (?,?) "
                "ON DUPLICATE KEY UPDATE asset_uuid=asset_uuid;",
                [(asset_uuid, os) for os in operating_systems],
            )

        system_types = asset.get("system_types")
        if system_types and len(system_types) > 0:
            cursor.executemany(
                "INSERT INTO asset_system_types(asset_uuid, system_type) VALUES (?,?) "
                "ON DUPLICATE KEY UPDATE asset_uuid=asset_uuid;",
                [(asset_uuid, system_type) for system_type in system_types],
            )

        hostnames = asset.get("hostnames")
        if hostnames and len(hostnames) > 0:
            cursor.executemany(
                "INSERT INTO asset_hostnames(asset_uuid, hostname) VALUES (?,?) "
                "ON DUPLICATE KEY UPDATE asset_uuid=asset_uuid;",
                [(asset_uuid, hostname) for hostname in hostnames],
            )

        ssh_fingerprints = asset.get("ssh_fingerprints")
        if ssh_fingerprints and len(ssh_fingerprints) > 0:
            cursor.executemany(
                "INSERT INTO asset_ssh_fingerprints(asset_uuid, ssh_fingerprint) VALUES(?,?) "
                "ON DUPLICATE KEY UPDATE asset_uuid=asset_uuid;",
                [(asset_uuid, ssh_fingerprint) for ssh_fingerprint in ssh_fingerprints],
            )

        qualy_asset_ids = asset.get("qualy_asset_ids")
        if qualy_asset_ids and len(qualy_asset_ids) > 0:
            cursor.executemany(
                "INSERT INTO asset_qualy_asset_ids(asset_uuid, qualy_asset_id) VALUES(?,?) "
                "ON DUPLICATE KEY UPDATE asset_uuid=asset_uuid;",
                [(asset_uuid, qualy_asset_id) for qualy_asset_id in qualy_asset_ids],
            )

        asset_qualys_host_ids = asset.get("asset_qualys_host_ids")
        if asset_qualys_host_ids and len(asset_qualys_host_ids) > 0:
            cursor.executemany(
                "INSERT INTO asset_asset_qualys_host_ids(asset_uuid, asset_qualys_host_id) VALUES(?,?) "
                "ON DUPLICATE KEY UPDATE asset_uuid=asset_uuid;",
                [
                    (asset_uuid, asset_qualys_host_id)
                    for asset_qualys_host_id in asset_qualys_host_ids
                ],
            )

        manufacturer_tpm_ids = asset.get("manufacturer_tpm_ids")
        if manufacturer_tpm_ids and len(manufacturer_tpm_ids) > 0:
            cursor.executemany(
                "INSERT INTO asset_manufacturer_tpm_ids(asset_uuid, manufacturer_tpm_id) VALUES(?,?) "
                "ON DUPLICATE KEY UPDATE asset_uuid=asset_uuid;",
                [
                    (asset_uuid, manufacturer_tpm_id)
                    for manufacturer_tpm_id in manufacturer_tpm_ids
                ],
            )

        symantec_ep_hardware_keys = asset.get("symantec_ep_hardware_keys")
        if symantec_ep_hardware_keys and len(symantec_ep_hardware_keys) > 0:
            cursor.executemany(
                "INSERT INTO asset_symantec_ep_hardware_keys(asset_uuid, symantec_ep_hardware_key) VALUES(?,?) "
                "ON DUPLICATE KEY UPDATE asset_uuid=asset_uuid;",
                [
                    (asset_uuid, symantec_ep_hardware_key)
                    for symantec_ep_hardware_key in symantec_ep_hardware_keys
                ],
            )

        sources = asset.get("sources")
        if sources and len(sources) > 0:
            cursor.executemany(
                "INSERT INTO asset_sources(asset_uuid, name, first_seen, last_seen) "
                'VALUES (?,?,STR_TO_DATE(?,"%Y-%m-%dT%T.%fZ"), STR_TO_DATE(?,"%Y-%m-%dT%T.%fZ")) '
                "ON DUPLICATE KEY UPDATE asset_uuid=asset_uuid;",
                [
                    (
                        asset_uuid,
                        src.get("name"),
                        src.get("first_seen"),
                        src.get("last_seen"),
                    )
                    for src in sources
                ],
            )

        tags = asset.get("tags")
        if tags and len(tags) > 0:
            cursor.executemany(
                "INSERT INTO asset_tags(asset_uuid, `key`, value, added_by, added_at) "
                'VALUES(?,?,?,?,STR_TO_DATE(?,"%Y-%m-%dT%T.%fZ")) '
                "ON DUPLICATE KEY UPDATE asset_uuid=asset_uuid;",
                [
                    (
                        asset_uuid,
                        tag.get("key"),
                        tag.get("value"),
                        tag.get("added_by"),
                        tag.get("added_at"),
                    )
                    for tag in tags
                ],
            )
