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
    asset_uuid   VARCHAR(255) NOT NULL,
    software_cpe VARCHAR(512) NOT NULL,

    CONSTRAINT pk_asset_installed_softwares PRIMARY KEY (asset_uuid, software_cpe),
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
    asset_uuid VARCHAR(255) NOT NULL,
    fqdn       VARCHAR(512) NOT NULL,

    CONSTRAINT pk_asset_fqdns PRIMARY KEY (asset_uuid, fqdn),
    CONSTRAINT fk_asset_fqdns FOREIGN KEY (asset_uuid) REFERENCES assets (uuid)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS asset_mac_addresses
(
    asset_uuid  VARCHAR(255) NOT NULL,
    mac_address CHAR(17)     NOT NULL,

    CONSTRAINT pk_asset_mac_addresses PRIMARY KEY (asset_uuid, mac_address),
    CONSTRAINT fk_asset_mac_addresses FOREIGN KEY (asset_uuid) REFERENCES assets (uuid)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS asset_netbios_names
(
    asset_uuid   VARCHAR(255) NOT NULL,
    netbios_name VARCHAR(512) NOT NULL,

    CONSTRAINT pk_asset_netbios_names PRIMARY KEY (asset_uuid, netbios_name),
    CONSTRAINT fk_asset_netbios_names FOREIGN KEY (asset_uuid) REFERENCES assets (uuid)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS asset_operating_systems
(
    asset_uuid       VARCHAR(255) NOT NULL,
    operating_system VARCHAR(255) NOT NULL,

    CONSTRAINT pk_asset_operating_systems PRIMARY KEY (asset_uuid, operating_system),
    CONSTRAINT fk_asset_operating_systems FOREIGN KEY (asset_uuid) REFERENCES assets (uuid)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS asset_system_types
(
    asset_uuid  VARCHAR(255) NOT NULL,
    system_type VARCHAR(128) NOT NULL,

    CONSTRAINT pk_asset_system_types PRIMARY KEY (asset_uuid, system_type),
    CONSTRAINT fk_asset_system_types FOREIGN KEY (asset_uuid) REFERENCES assets (uuid)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS asset_hostnames
(
    asset_uuid VARCHAR(255) NOT NULL,
    hostname   VARCHAR(255) NOT NULL,

    CONSTRAINT pk_asset_hostnames PRIMARY KEY (asset_uuid, hostname),
    CONSTRAINT fk_asset_hostnames FOREIGN KEY (asset_uuid) REFERENCES assets (uuid)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS asset_ssh_fingerprints
(
    asset_uuid      VARCHAR(255) NOT NULL,
    ssh_fingerprint VARCHAR(255) NOT NULL,

    CONSTRAINT pk_asset_ssh_fingerprints PRIMARY KEY (asset_uuid, ssh_fingerprint),
    CONSTRAINT fk_asset_ssh_fingerprints FOREIGN KEY (asset_uuid) REFERENCES assets (uuid)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS asset_qualys_asset_ids
(
    asset_uuid      VARCHAR(255) NOT NULL,
    qualys_asset_id VARCHAR(255) NOT NULL,

    CONSTRAINT pk_asset_qualys_asset_ids PRIMARY KEY (asset_uuid, qualys_asset_id),
    CONSTRAINT fk_asset_qualys_asset_ids FOREIGN KEY (asset_uuid) REFERENCES assets (uuid)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS asset_qualys_host_ids
(
    asset_uuid     VARCHAR(255) NOT NULL,
    qualys_host_id VARCHAR(255) NOT NULL,

    CONSTRAINT pk_asset_qualys_host_ids PRIMARY KEY (asset_uuid, qualys_host_id),
    CONSTRAINT fk_asset_qualys_host_ids FOREIGN KEY (asset_uuid) REFERENCES assets (uuid)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS asset_manufacturer_tpm_ids
(
    asset_uuid          VARCHAR(255) NOT NULL,
    manufacturer_tpm_id VARCHAR(255) NOT NULL,

    CONSTRAINT pk_asset_manufacturer_tpm_id PRIMARY KEY (asset_uuid, manufacturer_tpm_id),
    CONSTRAINT fk_asset_manufacturer_tpm_id FOREIGN KEY (asset_uuid) REFERENCES assets (uuid)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS asset_symantec_ep_hardware_keys
(
    asset_uuid               VARCHAR(255) NOT NULL,
    symantec_ep_hardware_key VARCHAR(255) NOT NULL,

    CONSTRAINT pk_asset_symantec_ep_hardware_keys PRIMARY KEY (asset_uuid, symantec_ep_hardware_key),
    CONSTRAINT fk_asset_symantec_ep_hardware_keys FOREIGN KEY (asset_uuid) REFERENCES assets (uuid)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS asset_sources
(
    asset_uuid VARCHAR(255) NOT NULL,
    name       VARCHAR(128) NOT NULL,
    first_seen DATETIME,
    last_seen  DATETIME,

    CONSTRAINT pk_asset_sources PRIMARY KEY (asset_uuid, name),
    CONSTRAINT fk_asset_sources FOREIGN KEY (asset_uuid) REFERENCES assets (uuid)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);


CREATE TABLE IF NOT EXISTS asset_tags
(
    asset_uuid VARCHAR(255) NOT NULL,
    `key`      VARCHAR(128),
    value      VARCHAR(128),
    added_by   TEXT,
    added_at   DATETIME,

    CONSTRAINT pk_asset_tags PRIMARY KEY (asset_uuid, `key`, value),
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
    created_on                 DATETIME DEFAULT DATE(CURRENT_TIMESTAMP),
    asset_uuid                 VARCHAR(255) NOT NULL,
    plugin_id                  INTEGER      NOT NULL,
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

    INDEX idx_created_on (created_on),
    INDEX idx_source (source(2)),
    INDEX idx_severity (severity(2)),
    INDEX idx_state (state(2)),
    INDEX idx_severity_modification_type (severity_modification_type(2)),

    CONSTRAINT pk_vulnerability PRIMARY KEY (uuid),
    CONSTRAINT fk_vuln_asset FOREIGN KEY (asset_uuid) REFERENCES assets (uuid)
        ON DELETE NO ACTION
        ON UPDATE CASCADE,
    CONSTRAINT fk_vuln_scan FOREIGN KEY (scan_uuid) REFERENCES scans (uuid)
        ON DELETE NO ACTION
        ON UPDATE CASCADE,
    CONSTRAINT fk_vuln_plugin FOREIGN KEY (plugin_id) REFERENCES plugins (id)
        ON DELETE NO ACTION
        ON UPDATE CASCADE
);

ALTER TABLE vulnerabilities ADD COLUMN ts TIMESTAMP(6) GENERATED ALWAYS AS ROW START,
                            ADD COLUMN te TIMESTAMP(6) GENERATED ALWAYS AS ROW END,
                            ADD COLUMN ts_date DATE,
                            ADD PERIOD FOR SYSTEM_TIME(ts, te)
                            ADD SYSTEM VERSIONING;

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
    plugin_id              INTEGER NOT NULL,
    access_vector          TEXT,
    access_complexity      TEXT,
    authentication         TEXT,
    confidentiality_impact TEXT,
    integrity_impact       TEXT,
    availability_impact    TEXT,
    raw                    TEXT,

    CONSTRAINT pk_plugin_cvss_vector PRIMARY KEY (plugin_id),
    CONSTRAINT fk_plugin_cvss_vector FOREIGN KEY (plugin_id) REFERENCES plugins (id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS plugin_cvss3_vectors
(
    plugin_id              INTEGER NOT NULL,
    access_vector          TEXT,
    access_complexity      TEXT,
    authentication         TEXT,
    confidentiality_impact TEXT,
    integrity_impact       TEXT,
    availability_impact    TEXT,
    raw                    TEXT,

    CONSTRAINT pk_plugin_cvss3_vector PRIMARY KEY (plugin_id),
    CONSTRAINT fk_plugin_cvss3_vector FOREIGN KEY (plugin_id) REFERENCES plugins (id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS plugin_cvss_temporal_vectors
(
    plugin_id         INTEGER NOT NULL,
    exploitability    TEXT,
    remediation_level TEXT,
    report_confidence TEXT,
    raw               TEXT,


    CONSTRAINT pk_plugin_cvss_temporal_vector PRIMARY KEY (plugin_id),
    CONSTRAINT fk_plugin_cvss_temporal_vector FOREIGN KEY (plugin_id) REFERENCES plugins (id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS plugin_cvss3_temporal_vectors
(
    plugin_id         INTEGER NOT NULL,
    exploitability    TEXT,
    remediation_level TEXT,
    report_confidence TEXT,
    raw               TEXT,

    CONSTRAINT pk_plugin_cvss3_temporal_vector PRIMARY KEY (plugin_id),
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
    plugin_id INTEGER      NOT NULL,
    cpe       VARCHAR(512) NOT NULL,

    CONSTRAINT pk_plugin_cpe PRIMARY KEY (plugin_id, cpe),
    CONSTRAINT fk_plugin_cpe FOREIGN KEY (plugin_id) REFERENCES plugins (id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS plugin_cves
(
    plugin_id INTEGER      NOT NULL,
    cve       VARCHAR(512) NOT NULL,

    CONSTRAINT pk_plugin_cve PRIMARY KEY (plugin_id, cve),
    CONSTRAINT fk_plugin_cve FOREIGN KEY (plugin_id) REFERENCES plugins (id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

COMMIT;
