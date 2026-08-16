#!/usr/bin/env python3
"""Quick test script to verify backend connection"""

import requests
import time

def test_backend():
    """Test if backend is running and responding"""
    backend_url = "http://127.0.0.1:8000"
    
    print("🔍 Testing backend connection...")
    
    try:
        # Test health endpoint
        response = requests.get(f"{backend_url}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend health check: PASSED")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Backend health check: FAILED (Status: {response.status_code})")
            return False
            
        # Test root endpoint
        response = requests.get(f"{backend_url}/", timeout=5)
        if response.status_code == 200:
            print("✅ Backend root endpoint: PASSED")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Backend root endpoint: FAILED (Status: {response.status_code})")
            return False
            
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Backend connection: FAILED - Server not reachable")
        print("   Make sure backend is running: uvicorn app:app --host 0.0.0.0 --port 8000 --reload")
        return False
    except requests.exceptions.Timeout:
        print("❌ Backend connection: TIMEOUT")
        return False
    except Exception as e:
        print(f"❌ Backend connection: ERROR - {str(e)}")
        return False

def test_frontend():
    """Test if frontend is accessible"""
    frontend_url = "http://127.0.0.1:5500"
    
    print("\n🔍 Testing frontend connection...")
    
    try:
        response = requests.get(frontend_url, timeout=5)
        if response.status_code == 200:
            print("✅ Frontend server: ACCESSIBLE")
            print(f"   Status: {response.status_code}")
            return True
        else:
            print(f"❌ Frontend server: FAILED (Status: {response.status_code})")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Frontend connection: FAILED - Server not reachable")
        print("   Make sure frontend is running: python -m http.server 5500")
        return False
    except Exception as e:
        print(f"❌ Frontend connection: ERROR - {str(e)}")
        return False

if __name__ == "__main__":
    print("Market Basket Analysis - Connection Test")
    print("=" * 50)
    
    backend_ok = test_backend()
    frontend_ok = test_frontend()
    
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS:")
    print(f"   Backend:  {'✅ PASS' if backend_ok else '❌ FAIL'}")
    print(f"   Frontend: {'✅ PASS' if frontend_ok else '❌ FAIL'}")
    
    if backend_ok and frontend_ok:
        print("\n🎉 ALL TESTS PASSED!")
        print("   You can now open: http://127.0.0.1:5500")
    else:
        print("\n⚠️  SOME TESTS FAILED!")
        print("   Check the error messages above and fix the issues.")
        
        if not backend_ok:
            print("\n🔧 To fix backend:")
            print("   1. cd backend")
            print("   2. pip install -r requirements.txt")
            print("   3. uvicorn app:app --host 0.0.0.0 --port 8000 --reload")
            
        if not frontend_ok:
            print("\n🔧 To fix frontend:")
            print("   1. cd frontend")
            print("   2. python -m http.server 5500")