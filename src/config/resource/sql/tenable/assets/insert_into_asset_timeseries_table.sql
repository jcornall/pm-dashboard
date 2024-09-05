INSERT INTO asset_timeseries (
asset_id,
created_on,
acr_score,
agent_names_0,
agent_uuid,
bios_uuid,
created_at,
deleted_at,
deleted_by,
exposure_score,
first_scan_time,
first_seen,
fqdns_0,
fqdns_1,
has_agent,
has_plugin_results,
hostnames_0,
id,
ipv4s_0,
ipv4s_1,
ipv4s_2,
ipv4s_3,
ipv4s_4,
ipv4s_5,
ipv4s_6,
ipv4s_7,
ipv6s_0,
ipv6s_1,
ipv6s_2,
ipv6s_3,
last_authenticated_scan_date,
last_licensed_scan_date,
last_scan_id,
last_scan_time,
last_schedule_id,
last_seen,
mac_addresses_0,
mcafee_epo_agent_guid,
mcafee_epo_guid,
netbios_names_0,
network_id,
network_name,
operating_systems_0,
operating_systems_1,
operating_systems_2,
operating_systems_3,
sources_0_first_seen,
sources_0_last_seen,
sources_0_name,
sources_1_first_seen,
sources_1_last_seen,
sources_1_name,
sources_2_first_seen,
sources_2_last_seen,
sources_2_name,
ssh_fingerprints_0,
symantec_ep_hardware_keys,
system_types_0,
tags_0_added_at,
tags_0_added_by,
tags_0_key,
tags_0_uuid,
tags_0_value,
tags_1_added_at,
tags_1_added_by,
tags_1_key,
tags_1_uuid,
tags_1_value,
tags_2_added_at,
tags_2_added_by,
tags_2_key,
tags_2_uuid,
tags_2_value,
tags_3_added_at,
tags_3_added_by,
tags_3_key,
tags_3_uuid,
tags_3_value,
tags_4_added_at,
tags_4_added_by,
tags_4_key,
tags_4_uuid,
tags_4_value,
tags_5_added_at,
tags_5_added_by,
tags_5_key,
tags_5_uuid,
tags_5_value,
tags_6_added_at,
tags_6_added_by,
tags_6_key,
tags_6_uuid,
tags_6_value,
tags_7_added_at,
tags_7_added_by,
tags_7_key,
tags_7_uuid,
tags_7_value,
tags_8_added_at,
tags_8_added_by,
tags_8_key,
tags_8_uuid,
tags_8_value,
tags_9_added_at,
tags_9_added_by,
tags_9_key,
tags_9_uuid,
tags_9_value,
terminated_at,
terminated_by,
updated_at
)
SELECT DISTINCT * FROM asset_export
WHERE NOT EXISTS (
    SELECT * FROM asset_timeseries
    WHERE asset_export.created_on = asset_timeseries.created_on 
);