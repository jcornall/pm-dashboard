BEGIN;

CREATE TABLE IF NOT EXISTS assets
(
    uuid                         VARCHAR(255) UNIQUE PRIMARY KEY,
    has_plugin_results           BOOL,
    created_at                   DATETIME,
    terminated_at                DATETIME,
    terminated_by                TEXT,
    updated_at                   DATETIME,
    deleted_at                   DATETIME,
    deleted_by                   TEXT,
    first_seen                   DATETIME,
    last_seen                    DATETIME,
    first_scan_time              DATETIME,
    last_scan_time               DATETIME,
    last_authenticated_scan_date DATETIME,
    last_licensed_scan_date      DATETIME,
    last_scan_id                 VARCHAR(255),
    last_schedule_id             VARCHAR(255),
    azure_vm_id                  TEXT,
    azure_resource_id            TEXT,
    gcp_project_id               TEXT,
    gcp_zone                     TEXT,
    gcp_instance_id              TEXT,
    aws_ec2_instance_ami_id      TEXT,
    aws_ec2_instance_id          TEXT,
    agent_uuid                   VARCHAR(255),
    bios_uuid                    VARCHAR(255),
    network_id                   TEXT,
    network_name                 TEXT,
    aws_owner_id                 TEXT,
    aws_availability_zone        TEXT,
    aws_region                   TEXT,
    aws_vpc_id                   TEXT,
    aws_ec2_instance_group_name  TEXT,
    aws_ec2_instance_state_name  TEXT,
    aws_ec2_instance_type        TEXT,
    aws_subnet_id                TEXT,
    aws_ec2_product_code         TEXT,
    aws_ec2_name                 TEXT,
    mcafee_epo_guid              TEXT,
    mcafee_epo_agent_guid        TEXT,
    servicenow_sysid             TEXT,
    bigfix_asset_id              TEXT,
    device_type                  TEXT,
    last_authenticated_results   DATETIME,
    last_unauthenticated_results DATETIME,
    tracked                      BOOL,
    acr_score                    TEXT,
    exposure_score               TEXT
);

CREATE TABLE IF NOT EXISTS asset_installed_softwares
(
    id           SERIAL       NOT NULL,
    asset_uuid   VARCHAR(255) NOT NULL,
    software_cpe TEXT         NOT NULL,

    CONSTRAINT pk_asset_installed_softwares PRIMARY KEY (id),
    CONSTRAINT fk_asset_installed_softwares FOREIGN KEY (asset_uuid) REFERENCES assets (uuid)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS asset_ipv4_addresses
(
    asset_uuid VARCHAR(255) NOT NULL,
    ipv4       VARCHAR(15)  NOT NULL,

    CONSTRAINT pk_asset_ipv4 PRIMARY KEY (asset_uuid, ipv4),
    CONSTRAINT fk_asset_ipv4 FOREIGN KEY (asset_uuid) REFERENCES assets (uuid)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS asset_ipv6_addresses
(
    asset_uuid VARCHAR(255) NOT NULL,
    ipv6       VARCHAR(39)  NOT NULL,

    CONSTRAINT pk_asset_ipv6 PRIMARY KEY (asset_uuid, ipv6),
    CONSTRAINT fk_asset_ipv6 FOREIGN KEY (asset_uuid) REFERENCES assets (uuid)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS asset_fqdns
(
    id         SERIAL       NOT NULL,
    asset_uuid VARCHAR(255) NOT NULL,
    fqdn       TEXT         NOT NULL,

    CONSTRAINT pk_asset_fqdns PRIMARY KEY (id),
    CONSTRAINT fk_asset_fqdns FOREIGN KEY (asset_uuid) REFERENCES assets (uuid)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS asset_mac_addresses
(
    id          SERIAL       NOT NULL,
    asset_uuid  VARCHAR(255) NOT NULL,
    mac_address TEXT(17)     NOT NULL,

    CONSTRAINT pk_asset_mac_addresses PRIMARY KEY (id),
    CONSTRAINT fk_asset_mac_addresses FOREIGN KEY (asset_uuid) REFERENCES assets (uuid)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS asset_netbios_names
(
    id           SERIAL       NOT NULL,
    asset_uuid   VARCHAR(255) NOT NULL,
    netbios_name TEXT         NOT NULL,

    CONSTRAINT pk_asset_netbios_names PRIMARY KEY (id),
    CONSTRAINT fk_asset_netbios_names FOREIGN KEY (asset_uuid) REFERENCES assets (uuid)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS asset_operating_systems
(
    id               SERIAL       NOT NULL,
    asset_uuid       VARCHAR(255) NOT NULL,
    operating_system TEXT         NOT NULL,

    CONSTRAINT pk_asset_operating_systems PRIMARY KEY (id),
    CONSTRAINT fk_asset_operating_systems FOREIGN KEY (asset_uuid) REFERENCES assets (uuid)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS asset_system_types
(
    id          SERIAL       NOT NULL,
    asset_uuid  VARCHAR(255) NOT NULL,
    system_type TEXT         NOT NULL,

    CONSTRAINT pk_asset_system_types PRIMARY KEY (id),
    CONSTRAINT fk_asset_system_types FOREIGN KEY (asset_uuid) REFERENCES assets (uuid)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS asset_hostnames
(
    id         SERIAL       NOT NULL,
    asset_uuid VARCHAR(255) NOT NULL,
    hostname   TEXT         NOT NULL,

    CONSTRAINT pk_asset_hostnames PRIMARY KEY (id),
    CONSTRAINT fk_asset_hostnames FOREIGN KEY (asset_uuid) REFERENCES assets (uuid)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS asset_ssh_fingerprints
(
    id              SERIAL       NOT NULL,
    asset_uuid      VARCHAR(255) NOT NULL,
    ssh_fingerprint TEXT         NOT NULL,

    CONSTRAINT pk_asset_ssh_fingerprints PRIMARY KEY (id),
    CONSTRAINT fk_asset_ssh_fingerprints FOREIGN KEY (asset_uuid) REFERENCES assets (uuid)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS asset_qualys_asset_ids
(
    id              SERIAL       NOT NULL,
    asset_uuid      VARCHAR(255) NOT NULL,
    qualys_asset_id TEXT         NOT NULL,

    CONSTRAINT pk_asset_qualys_asset_ids PRIMARY KEY (id),
    CONSTRAINT fk_asset_qualys_asset_ids FOREIGN KEY (asset_uuid) REFERENCES assets (uuid)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS asset_qualys_host_ids
(
    id             SERIAL       NOT NULL,
    asset_uuid     VARCHAR(255) NOT NULL,
    qualys_host_id TEXT         NOT NULL,

    CONSTRAINT pk_asset_qualys_host_ids PRIMARY KEY (id),
    CONSTRAINT fk_asset_qualys_host_ids FOREIGN KEY (asset_uuid) REFERENCES assets (uuid)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS asset_manufacturer_tpm_ids
(
    id                  SERIAL       NOT NULL,
    asset_uuid          VARCHAR(255) NOT NULL,
    manufacturer_tpm_id TEXT         NOT NULL,

    CONSTRAINT pk_asset_manufacturer_tpm_id PRIMARY KEY (id),
    CONSTRAINT fk_asset_manufacturer_tpm_id FOREIGN KEY (asset_uuid) REFERENCES assets (uuid)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS asset_symantec_ep_hardware_keys
(
    id                       SERIAL       NOT NULL,
    asset_uuid               VARCHAR(255) NOT NULL,
    symantec_ep_hardware_key TEXT         NOT NULL,

    CONSTRAINT pk_asset_symantec_ep_hardware_keys PRIMARY KEY (id),
    CONSTRAINT fk_asset_symantec_ep_hardware_keys FOREIGN KEY (asset_uuid) REFERENCES assets (uuid)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS asset_sources
(
    id         SERIAL       NOT NULL,
    asset_uuid VARCHAR(255) NOT NULL,
    name       TEXT         NOT NULL,
    first_seen DATETIME,
    last_seen  DATETIME,

    CONSTRAINT pk_asset_sources PRIMARY KEY (id),
    CONSTRAINT fk_asset_sources FOREIGN KEY (asset_uuid) REFERENCES assets (uuid)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);


CREATE TABLE IF NOT EXISTS asset_tags
(
    id         SERIAL       NOT NULL,
    asset_uuid VARCHAR(255) NOT NULL,
    `key`      TEXT,
    value      TEXT,
    added_by   TEXT,
    added_at   DATETIME,

    CONSTRAINT pk_asset_tags PRIMARY KEY (id),
    CONSTRAINT fk_asset_tags FOREIGN KEY (asset_uuid) REFERENCES assets (uuid)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS scans
(
    uuid          VARCHAR(255) NOT NULL,
    schedule_uuid TEXT         NOT NULL,
    started_at    DATETIME     NOT NULL,

    CONSTRAINT pk_scan PRIMARY KEY (uuid)
);

CREATE TABLE IF NOT EXISTS vulnerability_asset_infos
(
    asset_uuid                   VARCHAR(255),
    agent_uuid                   VARCHAR(255),
    bios_uuid                    VARCHAR(255),
    device_type                  TEXT,
    fqdn                         TEXT,
    hostname                     TEXT,
    ipv4                         TEXT,
    ipv6                         TEXT,
    last_authenticated_results   DATETIME,
    last_unauthenticated_results DATETIME,
    mac_address                  TEXT,
    netbios_name                 TEXT,
    network_id                   TEXT,
    tracked                      BOOL,

    CONSTRAINT pk_vulnerability_asset_infos PRIMARY KEY (asset_uuid),
    CONSTRAINT fk_vulnerability_asset_infos FOREIGN KEY (asset_uuid) REFERENCES assets (uuid)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS vulnerabilities
(
    uuid                       VARCHAR(255) UNIQUE,
    asset_uuid                 VARCHAR(255) NOT NULL,
    recast_reason              TEXT,
    recast_rule_uuid           VARCHAR(255),
    scan_uuid                  VARCHAR(255) NOT NULL,
    severity                   TEXT         NOT NULL,
    severity_id                INTEGER      NOT NULL,
    severity_default_id        INTEGER      NOT NULL,
    severity_modification_type TEXT         NOT NULL,
    first_found                DATETIME     NOT NULL,
    last_fixed                 DATETIME,
    last_found                 DATETIME,
    indexed                    DATETIME,
    state                      TEXT,
    source                     TEXT,

    CONSTRAINT pk_vulnerability PRIMARY KEY (uuid),
    CONSTRAINT fk_vuln_asset FOREIGN KEY (asset_uuid) REFERENCES assets (uuid)
        ON DELETE NO ACTION
        ON UPDATE CASCADE,
    CONSTRAINT fk_vuln_scan FOREIGN KEY (scan_uuid) REFERENCES scans (uuid)
        ON DELETE NO ACTION
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS vulnerability_ports
(
    vulnerability_uuid VARCHAR(255) NOT NULL,
    port               INTEGER      NOT NULL,
    protocol           TEXT         NOT NULL,
    service            TEXT,

    CONSTRAINT fk_vuln_port FOREIGN KEY (vulnerability_uuid) REFERENCES vulnerabilities (uuid)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS plugins
(
    id                           INTEGER NOT NULL,
    canvas_package               TEXT,
    checks_for_default_account   BOOL,
    checks_for_malware           BOOL,
    cvss3_base_score             FLOAT,
    cvss3_temporal_score         FLOAT,
    cvss_base_score              FLOAT,
    cvss_temporal_score          FLOAT,
    d2_elliot_name               TEXT,
    description                  TEXT,
    exploit_available            BOOL,
    exploit_framework_canvas     BOOL,
    exploit_framework_core       BOOL,
    exploit_framework_d2_elliot  BOOL,
    exploit_framework_exploithub BOOL,
    exploit_framework_metasploit BOOL,
    exploitability_ease          TEXT,
    exploited_by_malware         BOOL,
    exploited_by_nessus          BOOL,
    exploithub_sku               TEXT,
    family                       TEXT,
    family_id                    TEXT,
    has_patch                    BOOL,
    in_the_news                  BOOL,
    metasploit_name              TEXT,
    ms_bulletin                  TEXT,
    name                         TEXT,
    patch_publication_date       DATETIME,
    modification_date            DATETIME,
    publication_date             DATETIME,
    risk_factor                  TEXT,
    solution                     TEXT,
    stig_severity                TEXT,
    synopsis                     TEXT,
    type                         TEXT,
    unsupported_by_vendor        BOOL,
    usn                          TEXT,
    version                      TEXT,
    vuln_publication_date        DATETIME,

    CONSTRAINT pk_plugin PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS plugin_vprs
(
    plugin_id INTEGER NOT NULL,
    score     FLOAT,
    updated   DATETIME,

    CONSTRAINT pk_plugin_vpr PRIMARY KEY (plugin_id),
    CONSTRAINT fk_plugin_vpr FOREIGN KEY (plugin_id) REFERENCES plugins (id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS plugin_cvss_vectors
(
    id                     SERIAL,
    plugin_id              INTEGER NOT NULL,
    access_vector          TEXT,
    access_complexity      TEXT,
    authentication         TEXT,
    confidentiality_impact TEXT,
    integrity_impact       TEXT,
    availability_impact    TEXT,
    raw                    TEXT,

    CONSTRAINT pk_plugin_cvss_vector PRIMARY KEY (id),
    CONSTRAINT fk_plugin_cvss_vector FOREIGN KEY (plugin_id) REFERENCES plugins (id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS plugin_cvss3_vectors
(
    id                     SERIAL,
    plugin_id              INTEGER NOT NULL,
    access_vector          TEXT,
    access_complexity      TEXT,
    authentication         TEXT,
    confidentiality_impact TEXT,
    integrity_impact       TEXT,
    availability_impact    TEXT,
    raw                    TEXT,

    CONSTRAINT pk_plugin_cvss3_vector PRIMARY KEY (id),
    CONSTRAINT fk_plugin_cvss3_vector FOREIGN KEY (plugin_id) REFERENCES plugins (id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS plugin_cvss_temporal_vectors
(
    id                SERIAL,
    plugin_id         INTEGER NOT NULL,
    exploitability    TEXT,
    remediation_level TEXT,
    report_confidence TEXT,
    raw               TEXT,


    CONSTRAINT pk_plugin_cvss_temporal_vector PRIMARY KEY (id),
    CONSTRAINT fk_plugin_cvss_temporal_vector FOREIGN KEY (plugin_id) REFERENCES plugins (id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS plugin_cvss3_temporal_vectors
(
    id                SERIAL,
    plugin_id         INTEGER NOT NULL,
    exploitability    TEXT,
    remediation_level TEXT,
    report_confidence TEXT,
    raw               TEXT,

    CONSTRAINT pk_plugin_cvss3_temporal_vector PRIMARY KEY (id),
    CONSTRAINT fk_plugin_cvss3_temporal_vector FOREIGN KEY (plugin_id) REFERENCES plugins (id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS plugin_bugtraqs
(
    plugin_id  INTEGER NOT NULL,
    bugtraq_id INTEGER NOT NULL,

    CONSTRAINT pk_plugin_bugtraq PRIMARY KEY (plugin_id, bugtraq_id),
    CONSTRAINT fk_plugin_bugtraq FOREIGN KEY (bugtraq_id) REFERENCES plugins (id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS plugin_cpes
(
    id        SERIAL  NOT NULL,
    plugin_id INTEGER NOT NULL,
    cpe       TEXT    NOT NULL,

    CONSTRAINT pk_plugin_cpe PRIMARY KEY (id),
    CONSTRAINT fk_plugin_cpe FOREIGN KEY (plugin_id) REFERENCES plugins (id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS plugin_cves
(
    id        SERIAL       NOT NULL,
    plugin_id INTEGER      NOT NULL,
    cve       VARCHAR(512) NOT NULL,

    CONSTRAINT pk_plugin_cve PRIMARY KEY (id),
    CONSTRAINT fk_plugin_cve FOREIGN KEY (plugin_id) REFERENCES plugins (id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

COMMIT;
