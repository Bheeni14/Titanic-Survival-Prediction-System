"""
Minimal test to identify the crash point
"""
import sys

print("Step 1: Basic Python works")

try:
    import warnings
    warnings.filterwarnings('ignore')
    print("Step 2: Warnings module works")
except Exception as e:
    print(f"FAILED at warnings: {e}")
    sys.exit(1)

try:
    print("Step 3: Attempting numpy import...")
    import numpy as np
    print(f"Step 4: Numpy imported successfully! Version: {np.__version__}")
except Exception as e:
    print(f"FAILED at numpy: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

try:
    print("Step 5: Attempting pandas import...")
    import pandas as pd
    print(f"Step 6: Pandas imported successfully! Version: {pd.__version__}")
except Exception as e:
    print(f"FAILED at pandas: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

try:
    print("Step 7: Attempting sklearn import...")
    import sklearn
    print(f"Step 8: Sklearn imported successfully! Version: {sklearn.__version__}")
except Exception as e:
    print(f"FAILED at sklearn: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "="*60)
print("ALL IMPORTS SUCCESSFUL!")
print("="*60)
print("\nThe issue is with numpy's Windows compatibility.")
print("Recommendation: Use Python 3.11 instead of 3.13")
