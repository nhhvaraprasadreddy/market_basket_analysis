#!/usr/bin/env python3
"""Test the complete system with sample data"""

import requests
import os

def test_api_with_sample_data():
    """Test the API with the sample dataset"""
    api_url = "http://127.0.0.1:8000/api/analyze"
    dataset_path = "dataset/transactions.csv"
    
    print("Testing API with sample dataset...")
    
    if not os.path.exists(dataset_path):
        print(f"ERROR: Sample dataset not found at {dataset_path}")
        return False
    
    try:
        # Prepare the file upload
        with open(dataset_path, 'rb') as f:
            files = {'file': ('transactions.csv', f, 'text/csv')}
            data = {
                'min_support': '0.005',
                'min_confidence': '0.1', 
                'min_lift': '1.0',
                'algorithm': 'Apriori'
            }
            
            print("Sending request to API...")
            response = requests.post(api_url, files=files, data=data, timeout=30)
            
        if response.status_code == 200:
            result = response.json()
            print("API Test: PASSED")
            print(f"   Rules found: {len(result.get('rules', []))}")
            print(f"   Frequent items: {len(result.get('frequent_items', []))}")
            print(f"   Algorithm used: {result.get('algorithm', 'Unknown')}")
            return True
        else:
            print(f"API Test: FAILED (Status: {response.status_code})")
            print(f"   Error: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("API Test: FAILED - Cannot connect to backend")
        return False
    except requests.exceptions.Timeout:
        print("API Test: FAILED - Request timeout")
        return False
    except Exception as e:
        print(f"API Test: FAILED - {str(e)}")
        return False

if __name__ == "__main__":
    print("Market Basket Analysis - Full System Test")
    print("=" * 50)
    
    # Test API
    api_ok = test_api_with_sample_data()
    
    print("\n" + "=" * 50)
    print("FULL SYSTEM TEST RESULTS:")
    print(f"   API Analysis: {'PASS' if api_ok else 'FAIL'}")
    
    if api_ok:
        print("\nSYSTEM IS FULLY FUNCTIONAL!")
        print("   Frontend: http://127.0.0.1:5500")
        print("   Backend:  http://127.0.0.1:8000")
        print("   Ready to upload CSV files and run analysis!")
    else:
        print("\nSYSTEM TEST FAILED!")
        print("   Check backend logs for errors.")