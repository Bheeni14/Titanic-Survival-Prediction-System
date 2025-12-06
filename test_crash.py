"""
Final attempt: Run Python in subprocess to catch crashes
"""
import subprocess
import sys

print("="*60)
print("SUBPROCESS CRASH DETECTOR")
print("="*60)

# Test if numpy crashes by running in subprocess
test_code = """
import warnings
warnings.filterwarnings('ignore')
import numpy as np
print(f"NUMPY_OK:{np.__version__}")
"""

print("\nTesting numpy in subprocess...")
result = subprocess.run(
    [sys.executable, '-c', test_code],
    capture_output=True,
    text=True,
    timeout=10
)

print(f"Return code: {result.returncode}")
print(f"Stdout: {result.stdout}")
print(f"Stderr: {result.stderr[:200] if result.stderr else 'None'}")

if result.returncode != 0:
    print("\n" + "="*60)
    print("CONFIRMED: Python crashes when importing numpy")
    print("="*60)
    print("\nYou MUST install Python 3.11 to proceed.")
    print("\n1. Download from: https://www.python.org/downloads/release/python-3118/")
    print("   Direct link: https://www.python.org/ftp/python/3.11.8/python-3.11.8-amd64.exe")
    print("\n2. Run installer, check 'Add to PATH'")
    print("\n3. After install, run:")
    print("   python --version")
    print("   (should show Python 3.11.x)")
    print("\n4. Then run:")
    print("   rmdir /s /q venv")
    print("   python -m venv venv")
    print("   call venv\\Scripts\\activate")
    print("   pip install -r requirements.txt")
    print("   python train_emergency.py")
else:
    print("\n✓ Numpy works! Continuing with full training...")
    # Import the rest
    exec(open('train_emergency.py').read())
