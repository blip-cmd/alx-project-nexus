#!/usr/bin/env python3
"""
🚀 Quick Test Runner for Movie Recommendation API
Simple script to run the comprehensive test suite.
"""

import subprocess
import sys
import os

def run_tests():
    """Run the API test suite."""
    print("🎬 Movie Recommendation API - Test Runner")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("../manage.py"):
        print("❌ Error: manage.py not found. Please run this from the tests directory or project root.")
        return False
    
    # Add project root to Python path for imports
    project_root = os.path.abspath('..' if not os.path.exists("manage.py") else '.')
    sys.path.insert(0, project_root)
    
    # Check if virtual environment is activated
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("⚠️  Warning: Virtual environment may not be activated.")
        print("💡 Activate it with: .\\venv\\Scripts\\Activate.ps1")
    
    try:
        # Import and run the test suite
        from api_test_suite import py_test
        
        print("🧪 Starting API tests...")
        print("📝 Results will be saved to 'test_results.txt'")
        print("-" * 50)
        
        success = py_test()
        
        if success:
            print("\n✅ Tests completed successfully!")
            print("📄 Check 'test_results.txt' for detailed results.")
        else:
            print("\n❌ Some tests failed. Check 'test_results.txt' for details.")
            
        return success
        
    except ImportError as e:
        print(f"❌ Error importing test suite: {e}")
        return False
    except Exception as e:
        print(f"💥 Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = run_tests()
    
    if not success:
        print("\n💡 Troubleshooting tips:")
        print("1. Make sure Django server is running: python manage.py runserver")
        print("2. Activate virtual environment: .\\venv\\Scripts\\Activate.ps1")
        print("3. Install dependencies: pip install -r requirements.txt")
        sys.exit(1)
    else:
        print("\n🎉 All done! Happy coding!")