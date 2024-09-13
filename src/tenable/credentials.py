from dataclasses import dataclass


@dataclass
class TenableCredentials:
    access_key: str
    secret_key: str

    def to_api_keys_str(self) -> str:
        return f"accessKey={self.access_key};secretKey={self.secret_key};"
