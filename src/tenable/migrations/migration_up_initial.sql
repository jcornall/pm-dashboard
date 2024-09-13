CREATE TABLE IF NOT EXISTS vulnerability
(
    uuid                       UUID UNIQUE,
    asset_uuid                 UUID      NOT NULL,
    recast_reason              TEXT,
    recast_rule_uuid           UUID,
    scan_uuid                  UUID      NOT NULL,
    severity                   TEXT      NOT NULL,
    severity_id                INTEGER   NOT NULL,
    severity_default_id        INTEGER   NOT NULL,
    severity_modification_type TEXT      NOT NULL,
    first_found                TIMESTAMP NOT NULL,
    last_fixed                 TIMESTAMP,
    last_found                 TIMESTAMP,
    indexed                    TIMESTAMP,
    state                      TEXT,
    source                     TEXT,

    CONSTRAINT pk_vulnerability PRIMARY KEY (uuid),
    CONSTRAINT fk_vuln_asset FOREIGN KEY (asset_uuid) REFERENCES asset (uuid)
        ON DELETE NO ACTION
        ON UPDATE CASCADE,
    CONSTRAINT fk_vuln_scan FOREIGN KEY (scan_uuid) REFERENCES scan (uuid)
        ON DELETE NO ACTION
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS asset
(
    uuid                         UUID UNIQUE PRIMARY KEY,
    agent_uuid                   UUID,
    bios_uuid                    UUID,
    device_type                  TEXT,
    fqdn                         TEXT,
    hostname                     TEXT,
    ipv4                         TEXT,
    ipv6                         TEXT,
    last_authenticated_results   TIMESTAMP,
    last_unauthenticated_results TIMESTAMP,
    mac_address                  TEXT,
    netbios_name                 TEXT,
    network_id                   TEXT,
    tracked                      BOOL
);

CREATE TABLE IF NOT EXISTS asset_os
(
    asset_uuid       UUID NOT NULL,
    operating_system TEXT NOT NULL,

    CONSTRAINT pk_asset_os PRIMARY KEY (asset_uuid, operating_system),
    CONSTRAINT fk_asset_os FOREIGN KEY (asset_uuid) REFERENCES asset (uuid)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS scan
(
    uuid          UUID      NOT NULL,
    schedule_uuid UUID      NOT NULL,
    started_at    TIMESTAMP NOT NULL,

    CONSTRAINT pk_scan PRIMARY KEY (uuid)
);

CREATE TABLE IF NOT EXISTS vulnerability_port
(
    vulnerability_uuid UUID    NOT NULL,
    port               INTEGER NOT NULL,
    protocol           TEXT    NOT NULL,
    service            TEXT    NOT NULL,

    CONSTRAINT fk_vuln_port FOREIGN KEY (vulnerability_uuid) REFERENCES vulnerability (uuid)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS plugin
(
    id                           INTEGER NOT NULL,
    canvas_package               TEXT,
    checks_for_default_account   BOOL,
    checks_for_malware           BOOL,
    cvss3_base_score             FLOAT,
    cvss3_temporal_score         FLOAT,
    cvss3_vector                 FLOAT,
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
    patch_publication_date       TIMESTAMP,
    modification_date            TIMESTAMP,
    publication_date             TIMESTAMP,
    risk_factor                  TEXT,
    solution                     TEXT,
    stig_severity                TEXT,
    synopsis                     TEXT,
    type                         TEXT,
    unsupported_by_vendor        BOOL,
    usn                          TEXT,
    version                      TEXT,
    vuln_publication_date        TIMESTAMP,

    CONSTRAINT pk_plugin PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS plugin_vpr
(
    id        SERIAL,
    plugin_id INTEGER NOT NULL,
    score     FLOAT,
    updated   TIMESTAMP,

    CONSTRAINT pk_plugin_vpr PRIMARY KEY (id),
    CONSTRAINT fk_plugin_vpr FOREIGN KEY (plugin_id) REFERENCES plugin (id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS plugin_cvss_vector
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
    CONSTRAINT fk_plugin_cvss_vector FOREIGN KEY (plugin_id) REFERENCES plugin (id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS plugin_cvss3_vector
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
    CONSTRAINT fk_plugin_cvss3_vector FOREIGN KEY (plugin_id) REFERENCES plugin (id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS plugin_cvss_temporal_vector
(
    id                SERIAL,
    plugin_id         INTEGER NOT NULL,
    exploitability    TEXT,
    remediation_level TEXT,
    report_confidence TEXT,
    raw               TEXT,


    CONSTRAINT pk_plugin_cvss_temporal_vector PRIMARY KEY (id),
    CONSTRAINT fk_plugin_cvss_temporal_vector FOREIGN KEY (plugin_id) REFERENCES plugin (id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS plugin_cvss3_temporal_vector
(
    id                SERIAL,
    plugin_id         INTEGER NOT NULL,
    exploitability    TEXT,
    remediation_level TEXT,
    report_confidence TEXT,
    raw               TEXT,

    CONSTRAINT pk_plugin_cvss3_temporal_vector PRIMARY KEY (id),
    CONSTRAINT fk_plugin_cvss3_temporal_vector FOREIGN KEY (plugin_id) REFERENCES plugin (id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS plugin_bugtraq
(
    plugin_id  INTEGER NOT NULL,
    bugtraq_id INTEGER NOT NULL,

    CONSTRAINT pk_plugin_bugtraq PRIMARY KEY (plugin_id, bugtraq_id),
    CONSTRAINT fk_plugin_bugtraq FOREIGN KEY (bugtraq_id) REFERENCES plugin (id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS plugin_cpe
(
    plugin_id INTEGER NOT NULL,
    cpe       TEXT    NOT NULL,

    CONSTRAINT pk_plugin_cpe PRIMARY KEY (plugin_id, cpe),
    CONSTRAINT fk_plugin_cpe FOREIGN KEY (plugin_id) REFERENCES plugin (id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS plugin_cve
(
    plugin_id INTEGER NOT NULL,
    cve       TEXT    NOT NULL,

    CONSTRAINT pk_plugin_cve PRIMARY KEY (plugin_id, cve),
    CONSTRAINT fk_plugin_cve FOREIGN KEY (plugin_id) REFERENCES plugin (id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
)
