#!/usr/bin/env python3
"""
Test runner script for the ASST project.
Runs all tests and provides a summary of results.
"""

import os
import sys
import subprocess
import time
from datetime import datetime


def print_header(text):
    """Print a formatted header."""
    print("\n" + "=" * 80)
    print(f" {text} ".center(80, "="))
    print("=" * 80 + "\n")


def run_tests(test_path=None, verbose=False):
    """
    Run pytest with the specified options.
    
    Args:
        test_path: Optional path to specific test file or directory
        verbose: Whether to run in verbose mode
    
    Returns:
        Tuple of (success: bool, output: str)
    """
    cmd = ["pytest"]
    
    if verbose:
        cmd.append("-v")
    
    # Add coverage reporting
    cmd.extend(["--cov=app", "--cov-report=term"])
    
    if test_path:
        cmd.append(test_path)
    
    print(f"Running command: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(
            cmd,
            check=False,
            capture_output=True,
            text=True
        )
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", f"Error running tests: {str(e)}"


def main():
    """Main function to run tests."""
    start_time = time.time()
    
    print_header("ASST Test Runner")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Check if pytest is installed
    try:
        import pytest
        import pytest_cov
    except ImportError:
        print("Error: pytest or pytest-cov not installed. Please install with:")
        print("pip install pytest pytest-cov")
        return 1
    
    # Parse command line arguments
    verbose = "-v" in sys.argv or "--verbose" in sys.argv
    
    # Get specific test path if provided
    test_path = None
    for arg in sys.argv[1:]:
        if not arg.startswith("-"):
            test_path = arg
            break
    
    # Run the tests
    print_header("Running Tests")
    success, stdout, stderr = run_tests(test_path, verbose)
    
    # Print output
    print(stdout)
    if stderr:
        print("Errors:")
        print(stderr)
    
    # Print summary
    print_header("Test Summary")
    elapsed_time = time.time() - start_time
    print(f"Completed in: {elapsed_time:.2f} seconds")
    
    if success:
        print("✅ All tests passed!")
        return 0
    else:
        print("❌ Some tests failed!")
        return 1


if __name__ == "__main__":
    sys.exit(main())
