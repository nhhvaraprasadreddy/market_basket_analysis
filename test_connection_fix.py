#!/usr/bin/env python3
"""
Simple connection test to verify backend is working
"""
import requests
import json
import time

def test_backend_connection():
    """Test if backend is running and accessible"""
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
            
    except requests.exceptions.ConnectionError:
        print("❌ Backend connection: FAILED - Server not reachable")
        print("   Make sure to run: start_backend.bat")
        return False
    except requests.exceptions.Timeout:
        print("❌ Backend connection: TIMEOUT")
        return False
    except Exception as e:
        print(f"❌ Backend connection: ERROR - {e}")
        return False
    
    try:
        # Test root endpoint
        response = requests.get(f"{backend_url}/", timeout=5)
        if response.status_code == 200:
            print("✅ Backend root endpoint: PASSED")
        else:
            print(f"⚠️ Backend root endpoint: Status {response.status_code}")
            
    except Exception as e:
        print(f"⚠️ Backend root endpoint: {e}")
    
    print("✅ Backend is running correctly!")
    return True

def test_cors():
    """Test CORS configuration"""
    print("\n🔍 Testing CORS configuration...")
    
    try:
        response = requests.options("http://127.0.0.1:8000/api/analyze", 
                                  headers={
                                      'Origin': 'http://127.0.0.1:3000',
                                      'Access-Control-Request-Method': 'POST'
                                  })
        
        cors_headers = {
            'Access-Control-Allow-Origin': response.headers.get('Access-Control-Allow-Origin'),
            'Access-Control-Allow-Methods': response.headers.get('Access-Control-Allow-Methods'),
            'Access-Control-Allow-Headers': response.headers.get('Access-Control-Allow-Headers')
        }
        
        print("✅ CORS headers received:")
        for header, value in cors_headers.items():
            if value:
                print(f"   {header}: {value}")
        
        return True
        
    except Exception as e:
        print(f"❌ CORS test failed: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("  Market Basket Analysis - Connection Test")
    print("=" * 50)
    
    # Test backend
    backend_ok = test_backend_connection()
    
    if backend_ok:
        # Test CORS
        test_cors()
        
        print("\n🎉 All tests passed! System is ready.")
        print("\nNext steps:")
        print("1. Open browser to: http://127.0.0.1:3000")
        print("2. Upload a CSV file with Transaction_ID and Item_Name columns")
        print("3. Run the analysis")
        
    else:
        print("\n❌ Backend not ready. Please:")
        print("1. Run: start_backend.bat")
        print("2. Wait for 'Application startup complete' message")
        print("3. Run this test again")
    
    print("\n" + "=" * 50)