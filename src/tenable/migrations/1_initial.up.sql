BEGIN;

CREATE TABLE IF NOT EXISTS assets
(
    uuid                         VARCHAR(255) UNIQUE PRIMARY KEY,
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
    tracked                      BOOL
);

CREATE TABLE IF NOT EXISTS scans
(
    uuid          VARCHAR(255) NOT NULL,
    schedule_uuid TEXT         NOT NULL,
    started_at    DATETIME     NOT NULL,

    CONSTRAINT pk_scan PRIMARY KEY (uuid)
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

CREATE TABLE IF NOT EXISTS asset_os
(
    asset_uuid       VARCHAR(255) NOT NULL,
    operating_system VARCHAR(255) NOT NULL,

    CONSTRAINT pk_asset_os PRIMARY KEY (asset_uuid, operating_system),
    CONSTRAINT fk_asset_os FOREIGN KEY (asset_uuid) REFERENCES assets (uuid)
        ON DELETE CASCADE
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
    plugin_id INTEGER      NOT NULL,

    # cpe strings doesn't have a defined length
    # but primary key requires all participating columns to have fixed length
    # 512 should be long enough
    cpe       VARCHAR(512) NOT NULL,

    CONSTRAINT pk_plugin_cpe PRIMARY KEY (plugin_id, cpe),
    CONSTRAINT fk_plugin_cpe FOREIGN KEY (plugin_id) REFERENCES plugins (id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS plugin_cves
(
    plugin_id INTEGER      NOT NULL,

    # cve strings doesn't have a defined length
    # but primary key requires all participating columns to have fixed length
    # 512 should be long enough
    cve       VARCHAR(512) NOT NULL,

    CONSTRAINT pk_plugin_cve PRIMARY KEY (plugin_id, cve),
    CONSTRAINT fk_plugin_cve FOREIGN KEY (plugin_id) REFERENCES plugins (id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

COMMIT;
