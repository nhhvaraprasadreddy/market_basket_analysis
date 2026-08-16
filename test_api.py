#!/usr/bin/env python3

import requests
import json

def test_api():
    """Test the API endpoint with the sample dataset"""
    
    url = "http://127.0.0.1:8000/api/analyze"
    
    # Test with the sample dataset
    try:
        files = {'file': open('dataset/transactions.csv', 'rb')}
    except FileNotFoundError:
        print("❌ Dataset file not found. Please ensure dataset/transactions.csv exists.")
        return
    
    data = {
        'min_support': 0.005,
        'min_confidence': 0.2,
        'min_lift': 1.0
    }
    
    try:
        print("Testing API endpoint...")
        response = requests.post(url, files=files, data=data)
        
        if response.status_code == 200:
            results = response.json()
            print("✅ API call successful!")
            print(f"Rules found: {len(results['rules'])}")
            print(f"Frequent items: {len(results['frequent_items'])}")
            
            if results['rules']:
                print("\nTop 3 association rules:")
                for i, rule in enumerate(results['rules'][:3], 1):
                    print(f"{i}. {rule['antecedent']} -> {rule['consequent']}")
                    print(f"   Support: {rule['support']:.4f}, Confidence: {rule['confidence']:.4f}, Lift: {rule['lift']:.4f}")
            
            if 'message' in results and results['message']:
                print(f"\nMessage: {results['message']}")
                
            if 'analysis_info' in results:
                info = results['analysis_info']
                print(f"\nDataset info: {info['total_transactions']} transactions, {info['total_items']} items")
                
        else:
            print(f"❌ API call failed with status {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to API. Make sure the backend server is running on http://127.0.0.1:8000")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    finally:
        files['file'].close()

if __name__ == "__main__":
    test_api()