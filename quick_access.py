#!/usr/bin/env python3
"""
🚀 Quick Access Script for Movie Recommendation API
Provides easy access to scripts and tests from the project root.
"""

import subprocess
import sys
import os
from pathlib import Path

def show_menu():
    """Display the main menu."""
    print("\n🎬 Movie Recommendation API - Quick Access")
    print("=" * 50)
    print("1. 🛠️  Run Setup (Windows)")
    print("2. 🧪  Run Tests")
    print("3. 🏗️  Build for Production")
    print("4. 📖  View Documentation")
    print("5. 🚪  Exit")
    print("=" * 50)

def run_choice(choice):
    """Execute the selected choice."""
    if choice == "1":
        # Run Windows setup
        script_path = Path("scripts/setup.ps1")
        if script_path.exists():
            subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", str(script_path)])
        else:
            print("❌ Setup script not found!")
    
    elif choice == "2":
        # Run tests
        test_path = Path("tests/run_tests.py")
        if test_path.exists():
            subprocess.run([sys.executable, str(test_path)])
        else:
            print("❌ Test runner not found!")
    
    elif choice == "3":
        # Build for production
        build_path = Path("scripts/build.sh")
        if build_path.exists():
            subprocess.run(["bash", str(build_path)])
        else:
            print("❌ Build script not found!")
    
    elif choice == "4":
        # View documentation
        docs_path = Path("docs")
        if docs_path.exists():
            print(f"📖 Documentation available in: {docs_path.absolute()}")
            print("Files:")
            for file in docs_path.iterdir():
                if file.is_file():
                    print(f"  - {file.name}")
        else:
            print("❌ Documentation directory not found!")
    
    elif choice == "5":
        print("👋 Goodbye!")
        sys.exit(0)
    
    else:
        print("❌ Invalid choice! Please select 1-5.")

def main():
    """Main function."""
    while True:
        show_menu()
        choice = input("\nSelect an option (1-5): ").strip()
        run_choice(choice)
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()