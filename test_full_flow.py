import requests
import pandas as pd
import time

def test_full_mba_flow():
    """Test the complete MBA flow with actual file upload"""
    base_url = "http://127.0.0.1:8000"
    
    print("Testing Complete MBA Flow...")
    print("=" * 40)
    
    # Test 1: Backend health
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print("[PASS] Backend is running")
        else:
            print("[FAIL] Backend health check failed")
            return False
    except requests.exceptions.RequestException:
        print("[FAIL] Backend is not running")
        print("[INFO] Start backend: uvicorn app:app --reload --host 127.0.0.1 --port 8000")
        return False
    
    # Test 2: File upload and analysis
    try:
        # Prepare test file
        csv_file_path = "dataset/transactions.csv"
        
        with open(csv_file_path, 'rb') as f:
            files = {'file': ('transactions.csv', f, 'text/csv')}
            data = {
                'min_support': 0.005,
                'min_confidence': 0.3,
                'min_lift': 1.0
            }
            
            print("[INFO] Uploading CSV and running analysis...")
            response = requests.post(f"{base_url}/api/analyze", files=files, data=data, timeout=30)
            
            if response.status_code == 200:
                results = response.json()
                print("[PASS] MBA Analysis completed successfully")
                print(f"[INFO] Found {len(results['rules'])} association rules")
                print(f"[INFO] Found {len(results['frequent_items'])} frequent items")
                
                if results['rules']:
                    print("[INFO] Sample rule:", results['rules'][0])
                if results['frequent_items']:
                    print("[INFO] Top item:", results['frequent_items'][0])
                
                return True
            else:
                print(f"[FAIL] Analysis failed with status: {response.status_code}")
                print(f"[ERROR] Response: {response.text}")
                return False
                
    except FileNotFoundError:
        print("[FAIL] Sample dataset not found at dataset/transactions.csv")
        return False
    except requests.exceptions.RequestException as e:
        print(f"[FAIL] Request failed: {e}")
        return False
    except Exception as e:
        print(f"[FAIL] Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = test_full_mba_flow()
    if success:
        print("\n[SUCCESS] All tests passed! Frontend should work correctly.")
    else:
        print("\n[ERROR] Tests failed. Please check backend setup.")