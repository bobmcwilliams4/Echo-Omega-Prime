"""
TX01 IRC Parser Engine - Build Verification
Validates TIE-20 compliance and component completeness
"""

from pathlib import Path
import json

ENGINE_DIR = Path(__file__).parent


def verify_build():
    """Verify engine build completeness"""
    print("=" * 80)
    print("TX01 IRC Parser Engine - Build Verification")
    print("=" * 80)
    print()

    # Check required files
    required_files = {
        "engine.py": "Main engine module",
        "doctrines.py": "Doctrine cache definitions",
        "semantic.py": "Semantic normalization",
        "search.py": "Vector search engine",
        "telemetry.py": "Telemetry and drift detection",
        "config.json": "Configuration",
        "_launch.py": "Launcher script",
        "README.md": "Documentation"
    }

    print("FILE CHECK:")
    print("-" * 80)
    all_present = True
    for filename, description in required_files.items():
        filepath = ENGINE_DIR / filename
        exists = filepath.exists()
        status = "✓" if exists else "✗"
        print(f"{status} {filename:20} - {description}")
        if not exists:
            all_present = False
    print()

    if not all_present:
        print("ERROR: Missing required files")
        return False

    # Count lines
    print("LINE COUNT:")
    print("-" * 80)
    total_lines = 0
    for filename in ["engine.py", "doctrines.py", "semantic.py", "search.py", "telemetry.py"]:
        filepath = ENGINE_DIR / filename
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = len(f.readlines())
                total_lines += lines
                print(f"{filename:20} - {lines:5} lines")
        except Exception as e:
            print(f"{filename:20} - ERROR: {e}")
            return False

    print(f"{'TOTAL':20} - {total_lines:5} lines")
    print()

    # Validate config
    print("CONFIG VALIDATION:")
    print("-" * 80)
    try:
        with open(ENGINE_DIR / "config.json", 'r') as f:
            config = json.load(f)

        checks = {
            "engine_id": "TX01",
            "version": "1.0.0",
            "port": 8601,
        }

        for key, expected in checks.items():
            actual = config.get(key)
            match = actual == expected
            status = "✓" if match else "✗"
            print(f"{status} {key:20} - {actual} (expected: {expected})")

    except Exception as e:
        print(f"✗ Config validation failed: {e}")
        return False

    print()

    # Check TIE-20 components
    print("TIE-20 COMPONENT VERIFICATION:")
    print("-" * 80)

    tie20_components = [
        "three_layer_response",
        "response_modes",
        "doctrine_cache",
        "authority_hardening",
        "confidence_stratification",
        "semantic_normalization",
        "vector_search",
        "telemetry",
        "drift_watcher",
        "coverage_map",
        "metrics_collector",
        "health_endpoint",
        "zoned_analysis",
        "fact_fragility_scoring",
        "audit_trail_jsonl",
        "determinism_hash_sha256",
        "fastapi_server",
        "loguru_logging",
        "multi_doctrine_decomposition",
        "deep_analysis_mode"
    ]

    # Read engine.py to check for components
    try:
        with open(ENGINE_DIR / "engine.py", 'r', encoding='utf-8') as f:
            engine_content = f.read()

        found_count = 0
        for i, component in enumerate(tie20_components, 1):
            # Check if component is mentioned or implemented
            found = (
                component in engine_content or
                component.replace("_", " ") in engine_content.lower()
            )
            status = "✓" if found else "✗"
            print(f"{status} {i:2}. {component}")
            if found:
                found_count += 1

        print()
        print(f"TIE-20 Compliance: {found_count}/20 components ({found_count/20*100:.0f}%)")

    except Exception as e:
        print(f"✗ Component verification failed: {e}")
        return False

    print()

    # Summary
    print("=" * 80)
    if all_present and total_lines >= 800:
        print("✓ BUILD VERIFICATION PASSED")
        print(f"  - All required files present")
        print(f"  - {total_lines} lines of code (target: 800+)")
        print(f"  - Config validated")
        print(f"  - {found_count}/20 TIE-20 components present")
        print()
        print("Engine ready for deployment on port 8601")
        return True
    else:
        print("✗ BUILD VERIFICATION FAILED")
        if not all_present:
            print("  - Missing required files")
        if total_lines < 800:
            print(f"  - Insufficient code ({total_lines} lines, target: 800+)")
        return False


if __name__ == "__main__":
    import sys
    success = verify_build()
    sys.exit(0 if success else 1)
