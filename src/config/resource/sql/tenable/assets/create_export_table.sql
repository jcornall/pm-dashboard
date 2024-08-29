CREATE TABLE IF NOT EXISTS assets_export (
asset_id INT AUTO_INCREMENT NOT NULL,
created_on DATE DEFAULT DATE(CURRENT_TIMESTAMP),
acr_score INT,
agent_names_0 TEXT,
agent_uuid TEXT,
aws_availability_zone TEXT,
aws_ec2_instance_ami_id TEXT,
aws_ec2_instance_group_name TEXT,
aws_ec2_instance_id TEXT,
aws_ec2_instance_state_name TEXT,
aws_ec2_instance_type TEXT,
aws_ec2_name TEXT,
aws_ec2_product_code TEXT,
aws_owner_id TEXT,
aws_region TEXT,
aws_subnet_id TEXT,
aws_vpc_id TEXT,
azure_resource_id TEXT,
azure_vm_id TEXT,
bigfix_asset_id TEXT,
bios_uuid TEXT,
created_at DATETIME,
deleted_at DATETIME,
deleted_by TEXT,
exposure_score INT,
first_scan_time DATETIME,
first_seen DATETIME,
fqdns_0 TEXT,
fqdns_1 TEXT,
gcp_instance_id TEXT,
gcp_project_id TEXT,
gcp_zone TEXT,
has_agent VARCHAR(8),
has_plugin_results VARCHAR(8),
hostnames_0 TEXT,
id VARCHAR(32),
ipv4s_0 VARCHAR(32),
ipv4s_1 VARCHAR(32),
ipv4s_2 VARCHAR(32),
ipv4s_3 VARCHAR(32),
ipv4s_4 VARCHAR(32),
ipv4s_5 VARCHAR(32),
ipv4s_6 VARCHAR(32),
ipv4s_7 VARCHAR(32),
ipv6s_0 VARCHAR(32),
ipv6s_1 VARCHAR(32),
ipv6s_2 VARCHAR(32),
ipv6s_3 VARCHAR(32),
last_authenticated_scan_date DATETIME,
last_licensed_scan_date DATETIME,
last_scan_id TEXT,
last_scan_time DATETIME,
last_schedule_id TEXT,
last_seen DATETIME,
mac_addresses_0 TEXT,
mcafee_epo_agent_guid TEXT,
mcafee_epo_guid TEXT,
netbios_names_0 TEXT,
network_id TEXT,
network_name VARCHAR(32),
open_ports TEXT,
operating_systems_0 TEXT,
operating_systems_1 TEXT,
operating_systems_2 TEXT,
operating_systems_3 TEXT,
qualys_asset_ids TEXT,
qualys_host_ids TEXT,
servicenow_sysid TEXT,
sources_0_first_seen DATETIME,
sources_0_last_seen DATETIME,
sources_0_name TEXT,
sources_1_first_seen DATETIME,
sources_1_last_seen DATETIME,
sources_1_name TEXT,
sources_2_first_seen DATETIME,
sources_2_last_seen DATETIME,
sources_2_name TEXT,
ssh_fingerprints_0 TEXT,
symantec_ep_hardware_keys TEXT,
system_types_0 TEXT,
tags_0_added_at DATETIME,
tags_0_added_by TEXT,
tags_0_key VARCHAR(32),
tags_0_uuid TEXT,
tags_0_value VARCHAR(32),
tags_1_added_at DATETIME,
tags_1_added_by TEXT,
tags_1_key VARCHAR(32),
tags_1_uuid TEXT,
tags_1_value VARCHAR(32),
tags_2_added_at DATETIME,
tags_2_added_by TEXT,
tags_2_key VARCHAR(32),
tags_2_uuid TEXT,
tags_2_value VARCHAR(32),
tags_3_added_at DATETIME,
tags_3_added_by TEXT,
tags_3_key VARCHAR(32),
tags_3_uuid TEXT,
tags_3_value VARCHAR(32),
tags_4_added_at DATETIME,
tags_4_added_by TEXT,
tags_4_key VARCHAR(32),
tags_4_uuid TEXT,
tags_4_value VARCHAR(32),
tags_5_added_at DATETIME,
tags_5_added_by TEXT,
tags_5_key VARCHAR(32),
tags_5_uuid TEXT,
tags_5_value VARCHAR(32),
tags_6_added_at DATETIME,
tags_6_added_by TEXT,
tags_6_key VARCHAR(32),
tags_6_uuid TEXT,
tags_6_value VARCHAR(32),
tags_7_added_at DATETIME,
tags_7_added_by TEXT,
tags_7_key VARCHAR(32),
tags_7_uuid TEXT,
tags_7_value VARCHAR(32),
tags_8_added_at DATETIME,
tags_8_added_by TEXT,
tags_8_key VARCHAR(32),
tags_8_uuid TEXT,
tags_8_value VARCHAR(32),
tags_9_added_at DATETIME,
tags_9_added_by TEXT,
tags_9_key VARCHAR(32),
tags_9_uuid TEXT,
tags_9_value VARCHAR(32),
terminated_at DATETIME,
terminated_by TEXT,
updated_at DATETIME,
PRIMARY KEY (asset_id)
);