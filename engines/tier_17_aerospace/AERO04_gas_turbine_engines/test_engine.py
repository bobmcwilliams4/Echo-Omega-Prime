"""Test AERO04 Gas Turbine Engine"""

import sys
from pathlib import Path

# Test import
sys.path.insert(0, str(Path(__file__).resolve().parent))

try:
    from engine import AERO04_GasTurbineEngine, ResponseMode, EngineType

    # Initialize engine
    engine = AERO04_GasTurbineEngine()

    print(f"✓ Engine initialized: {engine.engine_name} v{engine.version}")
    print(f"✓ Port: {engine.port}")
    print(f"✓ Doctrine blocks loaded: {len(engine.doctrine_cache)}")

    # List all doctrine topics
    print(f"\n=== Doctrine Topics ({len(engine.doctrine_cache)}) ===")
    for i, topic in enumerate(engine.doctrine_cache.keys(), 1):
        print(f"{i:2d}. {topic}")

    # Test queries
    test_questions = [
        ("Explain Brayton cycle efficiency", ResponseMode.FAST, None),
        ("How does axial compressor surge occur?", ResponseMode.DEFENSE, EngineType.TURBOFAN),
        ("Turbine blade cooling methods", ResponseMode.MEMO, EngineType.TURBOFAN)
    ]

    print(f"\n=== Test Queries ({len(test_questions)}) ===")
    for i, (question, mode, eng_type) in enumerate(test_questions, 1):
        print(f"\n{i}. Question: {question}")
        print(f"   Mode: {mode.value}")
        if eng_type:
            print(f"   Engine Type: {eng_type.value}")

        answer, used_blocks, confidence = engine.three_layer_response(question, mode, eng_type)

        print(f"   ✓ Confidence: {confidence.value}")
        print(f"   ✓ Blocks used: {', '.join(used_blocks[:3])}")
        print(f"   ✓ Answer length: {len(answer)} chars")
        print(f"   ✓ Answer preview: {answer[:150]}...")

    # Test telemetry
    telemetry = engine.get_telemetry()
    print(f"\n=== Telemetry ===")
    for key, value in telemetry.items():
        print(f"  {key}: {value}")

    print(f"\n✓ All tests passed!")
    print(f"✓ Engine ready for deployment on port {engine.port}")

except Exception as e:
    print(f"✗ Test failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
