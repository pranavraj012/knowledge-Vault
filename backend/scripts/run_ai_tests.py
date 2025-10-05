"""
AI Test Runner - Quick script to run AI tests with nice output

Usage:
    python scripts/run_ai_tests.py
    python scripts/run_ai_tests.py --verbose
    python scripts/run_ai_tests.py --quick    # Run only fast tests
"""

import subprocess
import sys
import argparse
from pathlib import Path

def run_ai_tests(verbose=False, quick=False):
    """Run AI tests with pytest"""
    
    # Base pytest command
    cmd = ["uv", "run", "pytest", "tests/test_ai_features.py"]
    
    # Add verbosity flags
    if verbose:
        cmd.extend(["-v", "-s"])  # verbose + no capture (show prints)
    else:
        cmd.append("-v")  # just verbose
    
    # Quick mode - skip slow tests
    if quick:
        cmd.extend(["-k", "not (concurrent or performance)"])
    
    # Add nice output formatting
    cmd.extend([
        "--tb=short",  # shorter traceback format
        "--color=yes"  # colored output
    ])
    
    print("🤖 Running AI Integration Tests...")
    print("=" * 50)
    print(f"Command: {' '.join(cmd)}")
    print("=" * 50)
    
    try:
        result = subprocess.run(cmd, cwd=Path(__file__).parent.parent)
        return result.returncode
    except KeyboardInterrupt:
        print("\n⚠️  Tests interrupted by user")
        return 1
    except Exception as e:
        print(f"❌ Failed to run tests: {e}")
        return 1

def main():
    parser = argparse.ArgumentParser(description="Run AI integration tests")
    parser.add_argument("--verbose", "-v", action="store_true", 
                       help="Show detailed output and AI responses")
    parser.add_argument("--quick", "-q", action="store_true",
                       help="Run only quick tests (skip performance/concurrency)")
    
    args = parser.parse_args()
    
    # Check if server is running
    try:
        import httpx
        with httpx.Client() as client:
            response = client.get("http://localhost:8000/health", timeout=2)
            if response.status_code != 200:
                raise Exception("Server not healthy")
        print("✅ Server is running")
    except Exception:
        print("❌ FastAPI server is not running!")
        print("Please start it first: uv run uvicorn pkm_backend.main:app --reload")
        return 1
    
    print()
    return run_ai_tests(verbose=args.verbose, quick=args.quick)

if __name__ == "__main__":
    sys.exit(main())