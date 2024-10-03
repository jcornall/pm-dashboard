BEGIN;

CREATE TABLE IF NOT EXISTS systems
(
    resource_id      BIGINT                                                         NOT NULL,
    service_pack     TEXT,
    health_status    ENUM ('UNKNOWN', 'HEALTHY', 'VULNERABLE', 'HIGHLY_VULNERABLE') NOT NULL,
    os_platform      TEXT                                                           NOT NULL,
    os_name          TEXT                                                           NOT NULL,
    requires_restart BOOL                                                           NOT NULL,

    CONSTRAINT pk_systems PRIMARY KEY (resource_id)
);

CREATE TABLE IF NOT EXISTS patches
(
    installed_count   INTEGER                                                      NOT NULL,
    missing_count     INTEGER                                                      NOT NULL,
    patch_id          INTEGER                                                      NOT NULL,
    severity          ENUM ('UNRATED', 'LOW', 'MODERATE', 'IMPORTANT', 'CRITICAL') NOT NULL,
    patch_name        TEXT                                                         NOT NULL,
    patch_description TEXT                                                         NOT NULL,
    release_date      DATETIME                                                     NOT NULL,

    CONSTRAINT pk_patches PRIMARY KEY (patch_id)
);

COMMIT
