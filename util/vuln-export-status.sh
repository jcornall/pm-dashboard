#!/bin/sh

<<comment
vuln-export-status.sh(export_uuid)
    curl API_VULN_EXPORT_STATUS
        if (response == 429)
            sleep(Retry-after)
            vuln-export-status.sh(export_uuid)
        return 0, status, total_chunks
comment