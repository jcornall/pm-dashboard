#!/bin/sh

<<comment
vuln-download-chunk.sh(chunk)
    curl API_VULN_DOWNLOAD_CHUNK
        if (response == 429)
            sleep(Retry-after)
            vuln-download-chunk.sh(chunk)
        return 0
comment