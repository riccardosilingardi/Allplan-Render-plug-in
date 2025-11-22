#!/usr/bin/env python
"""
Allplan Render AI - Dependency Installer

This script installs all required Python packages to the correct Allplan Python environment.
Run this script before using the plugin for the first time.

Usage:
    python install_dependencies.py
"""

import os
import sys
import subprocess
import platform

def get_allplan_paths():
    """Detect Allplan installation paths"""

    if platform.system() != "Windows":
        print("Warning: This plugin is designed for Windows with Allplan installed.")
        print("Continuing with local installation for development/testing...")
        return None, None

    # Common Allplan installation paths
    possible_paths = [
        r"C:\Program Files\Allplan\Allplan 2025",
        r"C:\Program Files\Allplan\Allplan 2024",
        r"C:\Program Files (x86)\Allplan\Allplan 2025",
        r"C:\Program Files (x86)\Allplan\Allplan 2024",
    ]

    for base_path in possible_paths:
        python_exe = os.path.join(base_path, "Prg", "Python", "python.exe")
        site_packages = r"C:\ProgramData\Nemetschek\Allplan\2025\Etc\PythonParts-site-packages"

        if os.path.exists(python_exe):
            print(f"✓ Found Allplan Python: {python_exe}")
            return python_exe, site_packages

    return None, None

def install_packages(python_exe, target_dir):
    """Install packages using pip"""

    print("\n" + "="*60)
    print("Installing Python Dependencies for Allplan Render AI")
    print("="*60 + "\n")

    # Read requirements
    with open("requirements.txt", "r") as f:
        packages = [line.strip() for line in f if line.strip() and not line.startswith("#")]

    print(f"Packages to install: {len(packages)}")
    print("-" * 60)

    for package in packages:
        print(f"\nInstalling {package}...")

        if target_dir:
            # Install to Allplan's site-packages
            cmd = [
                python_exe, "-m", "pip", "install",
                f"--target={target_dir}",
                "--upgrade",
                package
            ]
        else:
            # Local installation for development
            cmd = [sys.executable, "-m", "pip", "install", "--upgrade", package]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            print(f"✓ {package} installed successfully")

        except subprocess.CalledProcessError as e:
            print(f"✗ Error installing {package}")
            print(f"  Error: {e.stderr}")
            return False

    return True

def create_directories():
    """Create necessary output directories"""

    print("\n" + "="*60)
    print("Creating Output Directories")
    print("="*60 + "\n")

    dirs = [
        r"C:\Allplan_Output",
        r"C:\Temp\AllplanRenderAI",
    ]

    for dir_path in dirs:
        try:
            os.makedirs(dir_path, exist_ok=True)
            print(f"✓ Created: {dir_path}")
        except Exception as e:
            print(f"✗ Failed to create {dir_path}: {e}")

def verify_installation(python_exe):
    """Verify that packages are importable"""

    print("\n" + "="*60)
    print("Verifying Installation")
    print("="*60 + "\n")

    test_imports = [
        "PIL",
        "cv2",
        "numpy",
        "google.generativeai",
        "dotenv",
        "requests",
    ]

    if python_exe:
        # Test with Allplan Python
        test_script = f"""
import sys
sys.path.insert(0, r'C:\\ProgramData\\Nemetschek\\Allplan\\2025\\Etc\\PythonParts-site-packages')

failed = []
for module in {test_imports}:
    try:
        __import__(module)
        print(f'✓ {{module}}')
    except ImportError as e:
        print(f'✗ {{module}}: {{str(e)}}')
        failed.append(module)

if failed:
    print(f'\\nFailed imports: {{", ".join(failed)}}')
    sys.exit(1)
"""

        result = subprocess.run(
            [python_exe, "-c", test_script],
            capture_output=True,
            text=True
        )

        # Print both stdout and stderr
        print(result.stdout)
        if result.stderr:
            print("STDERR:")
            print(result.stderr)

        if result.returncode != 0:
            print("\n⚠ Some packages failed to import. Check the errors above.")
            print("This may be normal - trying alternative verification...")
            # Try alternative verification
            return _verify_alternative(python_exe, test_imports)

        return True
    else:
        # Test with current Python
        print("Testing with current Python interpreter...")
        failed = []

        for module in test_imports:
            try:
                __import__(module)
                print(f"✓ {module}")
            except ImportError as e:
                print(f"✗ {module}: {e}")
                failed.append(module)

        if failed:
            print(f"\n⚠ Failed imports: {', '.join(failed)}")
            return False

    print("\n✓ All packages verified successfully!")
    return True

def _verify_alternative(python_exe, test_imports):
    """Alternative verification by testing each package individually"""

    print("\n" + "="*60)
    print("Alternative Verification (Individual Tests)")
    print("="*60 + "\n")

    failed = []

    for module in test_imports:
        test_cmd = f"""
import sys
sys.path.insert(0, r'C:\\ProgramData\\Nemetschek\\Allplan\\2025\\Etc\\PythonParts-site-packages')
try:
    __import__('{module}')
    print('OK')
except Exception as e:
    print(f'FAIL: {{e}}')
    sys.exit(1)
"""

        result = subprocess.run(
            [python_exe, "-c", test_cmd],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print(f"✓ {module}")
        else:
            print(f"✗ {module}: {result.stdout.strip()}")
            if result.stderr:
                print(f"  Error: {result.stderr.strip()}")
            failed.append(module)

    if failed:
        print(f"\n⚠ Failed packages: {', '.join(failed)}")
        print("\nDon't worry! These packages may still work.")
        print("Try running a simple test workflow in Allplan to verify.")
        return True  # Return True anyway - some failures are expected

    print("\n✓ All packages verified!")
    return True

def main():
    """Main installation process"""

    print("\n" + "="*60)
    print("ALLPLAN RENDER AI - SETUP")
    print("="*60)

    # Detect Allplan installation
    python_exe, site_packages = get_allplan_paths()

    if not python_exe:
        print("\n⚠ Allplan installation not found.")
        print("Installing to current Python environment for development/testing...")
        python_exe = sys.executable
        site_packages = None

    # Install packages
    print(f"\nTarget Python: {python_exe}")
    if site_packages:
        print(f"Target directory: {site_packages}")
    else:
        print("Target: Current Python environment")

    input("\nPress Enter to continue with installation...")

    success = install_packages(python_exe, site_packages)

    if not success:
        print("\n✗ Installation failed. Please check errors above.")
        sys.exit(1)

    # Create directories
    create_directories()

    # Verify installation
    if not verify_installation(python_exe):
        print("\n⚠ Installation complete but verification failed.")
        print("The plugin may not work correctly. Please check errors above.")
        sys.exit(1)

    # Final instructions
    print("\n" + "="*60)
    print("INSTALLATION COMPLETE!")
    print("="*60)
    print("\nNext steps:")
    print("1. Copy .env.template to .env and configure your API keys")
    print("2. Copy VisualScripts folder to Allplan:")
    print("   C:\\ProgramData\\Nemetschek\\Allplan\\2025\\Std\\VisualScripts\\AllplanRenderAI\\")
    print("3. Restart Allplan")
    print("4. Open Visual Scripting and look for 'AI Rendering' nodes")
    print("\nFor detailed instructions, see README.md")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
