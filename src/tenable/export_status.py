from enum import Enum


class ExportRequestStatus(Enum):
    """Possible status of an export request. Applies to vuln and asset exports"""

    Queued = "QUEUED"
    Processing = "PROCESSING"
    Finished = "FINISHED"
    Cancelled = "CANCELLED"
    Error = "ERROR"
