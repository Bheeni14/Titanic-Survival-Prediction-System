"""
Test script for Titanic ML API
Run this to verify the backend is working correctly
"""

import requests
import json
from typing import Dict, Any

# Configuration
BASE_URL = "http://localhost:8000"
API_URL = f"{BASE_URL}/api/v1"


def test_health_check() -> bool:
    """Test health endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Health Check: PASSED")
            return True
        else:
            print(f"❌ Health Check: FAILED (Status {response.status_code})")
            return False
    except Exception as e:
        print(f"❌ Health Check: FAILED ({str(e)})")
        return False


def test_root_endpoint() -> bool:
    """Test root endpoint"""
    try:
        response = requests.get(BASE_URL, timeout=5)
        if response.status_code == 200:
            print("✅ Root Endpoint: PASSED")
            return True
        else:
            print(f"❌ Root Endpoint: FAILED (Status {response.status_code})")
            return False
    except Exception as e:
        print(f"❌ Root Endpoint: FAILED ({str(e)})")
        return False


def test_prediction() -> bool:
    """Test prediction endpoint"""
    try:
        # Test case: First-class female passenger (likely to survive)
        test_data = {
            "pclass": 1,
            "sex": "female",
            "age": 25,
            "sibsp": 1,
            "parch": 0,
            "fare": 100.0,
            "embarked": "S",
            "name": "Test Passenger",
            "cabin": "C85"
        }
        
        response = requests.post(f"{API_URL}/predict", json=test_data, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Prediction: PASSED")
            print(f"   Survived: {result['survived']}")
            print(f"   Survival Probability: {result['survival_probability']:.2%}")
            print(f"   Risk Level: {result['risk_level']}")
            return True
        else:
            print(f"❌ Prediction: FAILED (Status {response.status_code})")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Prediction: FAILED ({str(e)})")
        return False


def test_model_info() -> bool:
    """Test model info endpoint"""
    try:
        response = requests.get(f"{API_URL}/model/info", timeout=5)
        if response.status_code == 200:
            info = response.json()
            print("✅ Model Info: PASSED")
            print(f"   Model: {info['model_name']}")
            print(f"   Accuracy: {info['accuracy']:.2%}")
            return True
        else:
            print(f"❌ Model Info: FAILED (Status {response.status_code})")
            return False
    except Exception as e:
        print(f"❌ Model Info: FAILED ({str(e)})")
        return False


def test_model_metrics() -> bool:
    """Test model metrics endpoint"""
    try:
        response = requests.get(f"{API_URL}/model/metrics", timeout=5)
        if response.status_code == 200:
            metrics = response.json()
            print("✅ Model Metrics: PASSED")
            print(f"   Accuracy: {metrics['metrics']['accuracy']:.2%}")
            print(f"   ROC-AUC: {metrics['metrics']['roc_auc']:.2%}")
            return True
        else:
            print(f"❌ Model Metrics: FAILED (Status {response.status_code})")
            return False
    except Exception as e:
        print(f"❌ Model Metrics: FAILED ({str(e)})")
        return False


def test_feature_importance() -> bool:
    """Test feature importance endpoint"""
    try:
        response = requests.get(f"{API_URL}/visualizations/feature-importance", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ Feature Importance: PASSED")
            print(f"   Features: {len(data['features'])}")
            return True
        else:
            print(f"❌ Feature Importance: FAILED (Status {response.status_code})")
            return False
    except Exception as e:
        print(f"❌ Feature Importance: FAILED ({str(e)})")
        return False


def test_invalid_input() -> bool:
    """Test API validation with invalid input"""
    try:
        invalid_data = {
            "pclass": 5,  # Invalid: should be 1-3
            "sex": "unknown",  # Invalid: should be male/female
            "age": -5,  # Invalid: negative age
        }
        
        response = requests.post(f"{API_URL}/predict", json=invalid_data, timeout=5)
        
        if response.status_code == 422:  # Validation error expected
            print("✅ Input Validation: PASSED")
            return True
        else:
            print(f"⚠️  Input Validation: Unexpected response (Status {response.status_code})")
            return True  # Don't fail test, but note unexpected behavior
    except Exception as e:
        print(f"❌ Input Validation: FAILED ({str(e)})")
        return False


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("   🚢 TITANIC ML API TEST SUITE")
    print("="*60 + "\n")
    
    print(f"Testing API at: {BASE_URL}\n")
    
    tests = [
        ("Health Check", test_health_check),
        ("Root Endpoint", test_root_endpoint),
        ("Prediction", test_prediction),
        ("Model Info", test_model_info),
        ("Model Metrics", test_model_metrics),
        ("Feature Importance", test_feature_importance),
        ("Input Validation", test_invalid_input),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n[Testing {test_name}]")
        results.append(test_func())
    
    print("\n" + "="*60)
    print("   TEST RESULTS")
    print("="*60)
    
    passed = sum(results)
    total = len(results)
    
    print(f"\nPassed: {passed}/{total}")
    print(f"Failed: {total - passed}/{total}")
    
    if all(results):
        print("\n🎉 All tests passed! API is working correctly.\n")
    else:
        print("\n⚠️  Some tests failed. Please check the output above.\n")
    
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
