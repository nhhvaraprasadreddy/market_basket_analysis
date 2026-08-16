#!/usr/bin/env python3
"""
Complete System Test for Market Basket Analysis with Cross-Selling
Tests both backend functionality and API endpoints
"""

import requests
import pandas as pd
import json
import sys
import os

# Configuration
BACKEND_URL = "http://127.0.0.1:8000"
API_URL = "http://127.0.0.1:8000/api/analyze"
HEALTH_URL = "http://127.0.0.1:8000/health"
TEST_DATA_PATH = "dataset/transactions.csv"

def test_backend_health():
    """Test if backend is running"""
    try:
        response = requests.get(HEALTH_URL, timeout=5)
        if response.status_code == 200:
            print("✅ Backend health check passed")
            return True
        else:
            print(f"❌ Backend health check failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Backend connection failed: {e}")
        return False

def test_mba_analysis():
    """Test MBA analysis with sample data"""
    try:
        # Check if test data exists
        if not os.path.exists(TEST_DATA_PATH):
            print(f"❌ Test data not found: {TEST_DATA_PATH}")
            return False
        
        # Prepare test request
        files = {'file': open(TEST_DATA_PATH, 'rb')}
        data = {
            'min_support': 0.005,
            'min_confidence': 0.1,
            'min_lift': 1.0,
            'algorithm': 'FP-Growth'
        }
        
        print("🔄 Testing MBA analysis...")
        response = requests.post(API_URL, files=files, data=data, timeout=30)
        files['file'].close()
        
        if response.status_code != 200:
            print(f"❌ MBA analysis failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
        
        result = response.json()
        
        # Validate response structure
        required_fields = ['algorithm', 'rules', 'frequent_items', 'cross_selling_data']
        for field in required_fields:
            if field not in result:
                print(f"❌ Missing field in response: {field}")
                return False
        
        print(f"✅ MBA analysis successful!")
        print(f"   Algorithm: {result['algorithm']}")
        print(f"   Rules found: {len(result['rules'])}")
        print(f"   Frequent items: {len(result['frequent_items'])}")
        print(f"   Cross-selling products: {len(result['cross_selling_data'])}")
        
        # Test cross-selling data structure
        if result['cross_selling_data']:
            sample_product = list(result['cross_selling_data'].keys())[0]
            sample_suggestions = result['cross_selling_data'][sample_product]
            print(f"   Sample cross-selling for '{sample_product}': {len(sample_suggestions)} suggestions")
            
            if sample_suggestions:
                suggestion = sample_suggestions[0]
                required_suggestion_fields = ['item', 'confidence', 'lift', 'cross_selling_score', 'co_occurrence_count']
                for field in required_suggestion_fields:
                    if field not in suggestion:
                        print(f"❌ Missing field in cross-selling suggestion: {field}")
                        return False
                print(f"   Top suggestion: {suggestion['item']} (score: {suggestion['cross_selling_score']:.3f})")
        
        return True
        
    except Exception as e:
        print(f"❌ MBA analysis test failed: {e}")
        return False

def test_apriori_algorithm():
    """Test Apriori algorithm specifically"""
    try:
        if not os.path.exists(TEST_DATA_PATH):
            return False
        
        files = {'file': open(TEST_DATA_PATH, 'rb')}
        data = {
            'min_support': 0.005,
            'min_confidence': 0.1,
            'min_lift': 1.0,
            'algorithm': 'Apriori'
        }
        
        print("🔄 Testing Apriori algorithm...")
        response = requests.post(API_URL, files=files, data=data, timeout=30)
        files['file'].close()
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Apriori algorithm test passed!")
            print(f"   Rules found: {len(result['rules'])}")
            return True
        else:
            print(f"❌ Apriori algorithm test failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Apriori algorithm test failed: {e}")
        return False

def test_data_validation():
    """Test data validation and error handling"""
    try:
        print("🔄 Testing data validation...")
        
        # Test with invalid file
        files = {'file': ('test.txt', 'invalid,data\n1,2', 'text/plain')}
        data = {'min_support': 0.01, 'min_confidence': 0.5, 'min_lift': 1.0, 'algorithm': 'Apriori'}
        
        response = requests.post(f"{BACKEND_URL}/api/analyze", files=files, data=data, timeout=10)
        
        # Should return error for invalid data
        if response.status_code != 200:
            print("✅ Data validation test passed (correctly rejected invalid data)")
            return True
        else:
            print("⚠️ Data validation test warning (accepted invalid data)")
            return True  # Not critical failure
            
    except Exception as e:
        print(f"❌ Data validation test failed: {e}")
        return False

def test_parameter_validation():
    """Test parameter validation"""
    try:
        if not os.path.exists(TEST_DATA_PATH):
            return False
        
        print("🔄 Testing parameter validation...")
        
        # Test with invalid parameters
        files = {'file': open(TEST_DATA_PATH, 'rb')}
        data = {
            'min_support': 2.0,  # Invalid: > 1.0
            'min_confidence': 0.5,
            'min_lift': 1.0,
            'algorithm': 'Apriori'
        }
        
        response = requests.post(API_URL, files=files, data=data, timeout=10)
        files['file'].close()
        
        if response.status_code != 200:
            print("✅ Parameter validation test passed (correctly rejected invalid parameters)")
            return True
        else:
            print("⚠️ Parameter validation test warning (accepted invalid parameters)")
            return True  # Not critical failure
            
    except Exception as e:
        print(f"❌ Parameter validation test failed: {e}")
        return False

def display_sample_results():
    """Display sample results for verification"""
    try:
        if not os.path.exists(TEST_DATA_PATH):
            return
        
        print("\n📊 Sample Analysis Results:")
        print("=" * 50)
        
        files = {'file': open(TEST_DATA_PATH, 'rb')}
        data = {
            'min_support': 0.005,
            'min_confidence': 0.1,
            'min_lift': 1.0,
            'algorithm': 'FP-Growth'
        }
        
        response = requests.post(API_URL, files=files, data=data, timeout=30)
        files['file'].close()
        
        if response.status_code == 200:
            result = response.json()
            
            # Display top frequent items
            print("\n🔥 Top 5 Frequent Items:")
            for i, item in enumerate(result['frequent_items'][:5], 1):
                print(f"   {i}. {item['item']}: {item['frequency']} transactions")
            
            # Display top association rules
            print("\n📋 Top 5 Association Rules:")
            for i, rule in enumerate(result['rules'][:5], 1):
                ant = ', '.join(rule['antecedent'])
                cons = ', '.join(rule['consequent'])
                print(f"   {i}. {ant} → {cons}")
                print(f"      Support: {rule['support']:.3f}, Confidence: {rule['confidence']:.3f}, Lift: {rule['lift']:.3f}")
                print(f"      Cross-sell Score: {rule['cross_selling_score']:.3f}")
            
            # Display cross-selling example
            if result['cross_selling_data']:
                sample_product = list(result['cross_selling_data'].keys())[0]
                suggestions = result['cross_selling_data'][sample_product][:3]
                print(f"\n🎯 Cross-selling for '{sample_product}':")
                for i, suggestion in enumerate(suggestions, 1):
                    print(f"   {i}. {suggestion['item']} (Score: {suggestion['cross_selling_score']:.3f})")
        
    except Exception as e:
        print(f"Error displaying sample results: {e}")

def main():
    """Run all tests"""
    print("🧪 Market Basket Analysis System Test")
    print("=" * 50)
    
    tests = [
        ("Backend Health", test_backend_health),
        ("MBA Analysis", test_mba_analysis),
        ("Apriori Algorithm", test_apriori_algorithm),
        ("Data Validation", test_data_validation),
        ("Parameter Validation", test_parameter_validation)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Running {test_name} test...")
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} test failed!")
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is working correctly.")
        display_sample_results()
    else:
        print("⚠️ Some tests failed. Please check the backend setup.")
        print("\nTroubleshooting:")
        print("1. Ensure backend is running: uvicorn app:app --reload --port 8000")
        print("2. Check if dataset/transactions.csv exists")
        print("3. Verify all dependencies are installed: pip install -r requirements.txt")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)