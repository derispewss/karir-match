import json
from pathlib import Path
import sys

# Validate OpenAPI spec using openapi-spec-validator (needs to be installed).
# This script can be run via: python scripts/validate_openapi.py

def main():
    spec_path = Path("docs/api/openapi.yaml")
    if not spec_path.exists():
        print(f"[ERROR] OpenAPI spec not found at {spec_path}")
        sys.exit(1)
    try:
        from openapi_spec_validator import validate_spec
        import yaml
        with open(spec_path, "r", encoding="utf-8") as f:
            spec = yaml.safe_load(f)
        validate_spec(spec)
        print("✅ OpenAPI spec is valid.")
    except ImportError:
        print("[ERROR] openapi-spec-validator package not installed. Install with 'pip install openapi-spec-validator'.")
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] OpenAPI validation failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
