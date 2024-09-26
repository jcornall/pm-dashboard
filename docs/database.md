# Database

Each patch management tool (pmt) is assigned a database in which exported data are stored.

## Migrations

[golang-migrate](https://github.com/golang-migrate/migrate) is used to handle database migrations for this project.
Since each pmt has its own database, they evolve their database differently, which means migrations need to be handled separately. To that end, the migration scripts for each pmt is stored in the `migrations` directory located within its python module. For example, the migration scripts for Tenable is located in `src/tenable/migrations`.

To modify a database, a new migration step needs to be defined, in the form of two SQL files, named:

```
{version}_{title}.up.sql
{version}_{title}.down.sql
```

where the "up" SQL file defines what to change, and the "down" SQL file defines how to revert the changes. `version` should be an increment of the current version, and `title` should be a descriptive title that describes the migration.

### Installing `golang-migrate`

`install.sh` downloads the latest release of `golang-migrate` to `./golang-migrate` relative to the project's root.
The binary is then located in `./golang-migrate/migrate`.

### Running migration

To push changes to the database, run the `up` command:

```
./golang-migrate -path <path-to-migrations-dir> -database "mysql://user:pass@tcp(domain:port)/db-name" up
```

You will need to run the command above as well to initialize an empty database.

To revert changes, replace `up` with `down`.

## Schemas

This section documents the database schema modelled after the exported data for every patch management tool.

### Tenable

```mermaid
classDiagram
    direction BT
    class asset_fqdns {
    varchar(255) asset_uuid
    varchar(512) fqdn
    }
    class asset_hostnames {
    varchar(255) asset_uuid
    varchar(255) hostname
    }
    class asset_installed_softwares {
    varchar(255) asset_uuid
    varchar(512) software_cpe
    }
    class asset_ipv4_addresses {
    varchar(255) asset_uuid
    varchar(15) ipv4
    }
    class asset_ipv6_addresses {
    varchar(255) asset_uuid
    varchar(39) ipv6
    }
    class asset_mac_addresses {
    varchar(255) asset_uuid
    char(17) mac_address
    }
    class asset_manufacturer_tpm_ids {
    varchar(255) asset_uuid
    varchar(255) manufacturer_tpm_id
    }
    class asset_netbios_names {
    varchar(255) asset_uuid
    varchar(512) netbios_name
    }
    class asset_operating_systems {
    varchar(255) asset_uuid
    varchar(255) operating_system
    }
    class asset_qualys_asset_ids {
    varchar(255) asset_uuid
    varchar(255) qualys_asset_id
    }
    class asset_qualys_host_ids {
    varchar(255) asset_uuid
    varchar(255) qualys_host_id
    }
    class asset_sources {
    datetime first_seen
    datetime last_seen
    varchar(255) asset_uuid
    varchar(128) name
    }
    class asset_ssh_fingerprints {
    varchar(255) asset_uuid
    varchar(255) ssh_fingerprint
    }
    class asset_symantec_ep_hardware_keys {
    varchar(255) asset_uuid
    varchar(255) symantec_ep_hardware_key
    }
    class asset_system_types {
    varchar(255) asset_uuid
    varchar(128) system_type
    }
    class asset_tags {
    text added_by
    datetime added_at
    varchar(255) asset_uuid
    varchar(128) key
    varchar(128) value
    }
    class assets {
    tinyint(1) has_plugin_results
    datetime created_at
    datetime terminated_at
    text terminated_by
    datetime updated_at
    datetime deleted_at
    text deleted_by
    datetime first_seen
    datetime last_seen
    datetime first_scan_time
    datetime last_scan_time
    datetime last_authenticated_scan_date
    datetime last_licensed_scan_date
    varchar(255) last_scan_id
    varchar(255) last_schedule_id
    text azure_vm_id
    text azure_resource_id
    text gcp_project_id
    text gcp_zone
    text gcp_instance_id
    text aws_ec2_instance_ami_id
    text aws_ec2_instance_id
    varchar(255) agent_uuid
    varchar(255) bios_uuid
    text network_id
    text network_name
    text aws_owner_id
    text aws_availability_zone
    text aws_region
    text aws_vpc_id
    text aws_ec2_instance_group_name
    text aws_ec2_instance_state_name
    text aws_ec2_instance_type
    text aws_subnet_id
    text aws_ec2_product_code
    text aws_ec2_name
    text mcafee_epo_guid
    text mcafee_epo_agent_guid
    text servicenow_sysid
    text bigfix_asset_id
    text device_type
    datetime last_authenticated_results
    datetime last_unauthenticated_results
    tinyint(1) tracked
    text acr_score
    text exposure_score
    varchar(255) uuid
    }
    class plugin_bugtraqs {
    int(11) plugin_id
    int(11) bugtraq_id
    }
    class plugin_cpes {
    int(11) plugin_id
    varchar(512) cpe
    }
    class plugin_cves {
    int(11) plugin_id
    varchar(512) cve
    }
    class plugin_cvss3_temporal_vectors {
    text exploitability
    text remediation_level
    text report_confidence
    text raw
    int(11) plugin_id
    }
    class plugin_cvss3_vectors {
    text access_vector
    text access_complexity
    text authentication
    text confidentiality_impact
    text integrity_impact
    text availability_impact
    text raw
    int(11) plugin_id
    }
    class plugin_cvss_temporal_vectors {
    text exploitability
    text remediation_level
    text report_confidence
    text raw
    int(11) plugin_id
    }
    class plugin_cvss_vectors {
    text access_vector
    text access_complexity
    text authentication
    text confidentiality_impact
    text integrity_impact
    text availability_impact
    text raw
    int(11) plugin_id
    }
    class plugin_vprs {
    float score
    datetime updated
    int(11) plugin_id
    }
    class plugins {
    text canvas_package
    tinyint(1) checks_for_default_account
    tinyint(1) checks_for_malware
    float cvss3_base_score
    float cvss3_temporal_score
    float cvss_base_score
    float cvss_temporal_score
    text d2_elliot_name
    text description
    tinyint(1) exploit_available
    tinyint(1) exploit_framework_canvas
    tinyint(1) exploit_framework_core
    tinyint(1) exploit_framework_d2_elliot
    tinyint(1) exploit_framework_exploithub
    tinyint(1) exploit_framework_metasploit
    text exploitability_ease
    tinyint(1) exploited_by_malware
    tinyint(1) exploited_by_nessus
    text exploithub_sku
    text family
    text family_id
    tinyint(1) has_patch
    tinyint(1) in_the_news
    text metasploit_name
    text ms_bulletin
    text name
    datetime patch_publication_date
    datetime modification_date
    datetime publication_date
    text risk_factor
    text solution
    text stig_severity
    text synopsis
    text type
    tinyint(1) unsupported_by_vendor
    text usn
    text version
    datetime vuln_publication_date
    int(11) id
    }
    class scans {
    text schedule_uuid
    datetime started_at
    varchar(255) uuid
    }
    class schema_migrations {
    tinyint(1) dirty
    bigint(20) version
    }
    class vulnerabilities {
    datetime created_on
    varchar(255) asset_uuid
    int(11) plugin_id
    text recast_reason
    varchar(255) recast_rule_uuid
    varchar(255) scan_uuid
    text severity
    int(11) severity_id
    int(11) severity_default_id
    text severity_modification_type
    datetime first_found
    datetime last_fixed
    datetime last_found
    datetime indexed
    text state
    text source
    varchar(255) uuid
    }
    class vulnerability_asset_infos {
    varchar(255) agent_uuid
    varchar(255) bios_uuid
    text device_type
    text fqdn
    text hostname
    text ipv4
    text ipv6
    datetime last_authenticated_results
    datetime last_unauthenticated_results
    text mac_address
    text netbios_name
    text network_id
    tinyint(1) tracked
    varchar(255) asset_uuid
    }
    class vulnerability_ports {
    varchar(255) vulnerability_uuid
    int(11) port
    text protocol
    text service
    }

    asset_fqdns  -->  assets : asset_uuid
    asset_hostnames  -->  assets : asset_uuid
    asset_installed_softwares  -->  assets : asset_uuid
    asset_ipv4_addresses  -->  assets : asset_uuid
    asset_ipv6_addresses  -->  assets : asset_uuid
    asset_mac_addresses  -->  assets : asset_uuid
    asset_manufacturer_tpm_ids  -->  assets : asset_uuid
    asset_netbios_names  -->  assets : asset_uuid
    asset_operating_systems  -->  assets : asset_uuid
    asset_qualys_asset_ids  -->  assets : asset_uuid
    asset_qualys_host_ids  -->  assets : asset_uuid
    asset_sources  -->  assets : asset_uuid
    asset_ssh_fingerprints  -->  assets : asset_uuid
    asset_symantec_ep_hardware_keys  -->  assets : asset_uuid
    asset_system_types  -->  assets : asset_uuid
    asset_tags  -->  assets : asset_uuid
    plugin_bugtraqs  -->  plugins : bugtraq_id
    plugin_bugtraqs  -->  plugins : plugin_id
    plugin_cpes  -->  plugins : plugin_id
    plugin_cves  -->  plugins : plugin_id
    plugin_cvss3_temporal_vectors  -->  plugins : plugin_id
    plugin_cvss3_vectors  -->  plugins : plugin_id
    plugin_cvss_temporal_vectors  -->  plugins : plugin_id
    plugin_cvss_vectors  -->  plugins : plugin_id
    plugin_vprs  -->  plugins : plugin_id
    vulnerabilities  -->  assets : asset_uuid
    vulnerabilities  -->  plugins : plugin_id
    vulnerabilities  -->  scans : scan_uuid
    vulnerability_asset_infos  -->  assets : asset_uuid
    vulnerability_ports  -->  vulnerabilities : vulnerability_uuid
```
