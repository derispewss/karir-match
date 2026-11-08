import secrets
import hmac
import hashlib
import base64
from datetime import datetime, timedelta
from typing import Optional

# Simple CSRF utility (no external deps). Uses a secret stored in env or settings.
# Token = base64url(HMAC(secret, timestamp)) + ":" + timestamp
# Verify by recomputing HMAC and checking timestamp freshness (default 30 min).

class CSRFProtection:
    def __init__(self, secret: str, max_age_seconds: int = 1800):
        self.secret = secret.encode()
        self.max_age = max_age_seconds

    def generate_token(self) -> str:
        ts = int(datetime.utcnow().timestamp())
        mac = hmac.new(self.secret, str(ts).encode(), hashlib.sha256).digest()
        token = base64.urlsafe_b64encode(mac).decode().rstrip('=') + f":{ts}"
        return token

    def validate_token(self, token: str) -> bool:
        try:
            mac_b64, ts_str = token.split(":")
            ts = int(ts_str)
            # check age
            now = int(datetime.utcnow().timestamp())
            if now - ts > self.max_age:
                return False
            expected_mac = hmac.new(self.secret, str(ts).encode(), hashlib.sha256).digest()
            expected_b64 = base64.urlsafe_b64encode(expected_mac).decode().rstrip('=')
            return hmac.compare_digest(mac_b64, expected_b64)
        except Exception:
            return False
