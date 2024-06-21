#!/bin/sh

<<comment
asset-export-status.sh(export_uuid)
    curl API_VULN_EXPORT_STATUS
        if (response == 429)
            sleep(Retry-after)
            asset-export-status.sh(export_uuid)
        return 0, status, total_chunks
comment