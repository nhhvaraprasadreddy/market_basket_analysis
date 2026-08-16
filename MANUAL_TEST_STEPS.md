# 🧪 Manual Test Steps - Fix Connection Issues

## 🚨 EXACT STEPS TO FIX "127.0.0.1 refused to connect"

### Step 1: Open 2 Command Prompts

**Command Prompt 1 (Backend):**
```bash
cd "c:\Users\santh\OneDrive\Desktop\PRASAD REDDY\III-I\APPLIED DATA SCIENCE AND STATISTICAL ANALYSIS\MARKET BASKET ANALYSIS AND CROSS-SELLING ANALYTICS FOR GROCERY CHAIN\market-basket-analysis\backend"
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

**Command Prompt 2 (Frontend):**
```bash
cd "c:\Users\santh\OneDrive\Desktop\PRASAD REDDY\III-I\APPLIED DATA SCIENCE AND STATISTICAL ANALYSIS\MARKET BASKET ANALYSIS AND CROSS-SELLING ANALYTICS FOR GROCERY CHAIN\market-basket-analysis\frontend"
python -m http.server 5500
```

### Step 2: Verify Servers Are Running

**Backend Check:**
- Open: http://127.0.0.1:8000/health
- Should show: `{"status": "healthy"}`

**Frontend Check:**
- Open: http://127.0.0.1:5500/test.html
- Should show: "✅ Frontend Server is Working!"

### Step 3: Open Main Application

**Main App:**
- Open: http://127.0.0.1:5500/index.html
- Should show the Market Basket Analysis dashboard

### Step 4: Test End-to-End

1. **Upload File**: Select `dataset/transactions.csv`
2. **Set Parameters**: 
   - Algorithm: FP-Growth
   - Min Support: 0.005
   - Min Confidence: 0.1
   - Min Lift: 1.0
3. **Run Analysis**: Click "Run Analysis" button
4. **Verify Results**: Charts and tables should populate
5. **Test Cross-Selling**: Select a product and click "Show Cross-Selling Opportunities"

## 🔧 Common Fixes

### Fix 1: Port Already in Use
```bash
# Kill processes on ports
taskkill /f /im python.exe
taskkill /f /im uvicorn.exe

# Or use different ports
uvicorn app:app --host 0.0.0.0 --port 8001 --reload
python -m http.server 5501
```

### Fix 2: Python Not Found
```bash
# Try python3 instead of python
python3 -m http.server 5500

# Or use full path
C:\Python39\python.exe -m http.server 5500
```

### Fix 3: Directory Issues
```bash
# Verify you're in the right directory
dir
# Should show index.html, script.js, etc.

# If not, navigate correctly
cd frontend
dir
```

### Fix 4: Firewall/Antivirus
- Temporarily disable Windows Firewall
- Add Python.exe to antivirus exceptions
- Allow ports 8000 and 5500 through firewall

## ✅ Success Indicators

**Backend Terminal Should Show:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**Frontend Terminal Should Show:**
```
Serving HTTP on 0.0.0.0 port 5500 (http://0.0.0.0:5500/) ...
```

**Browser Should Show:**
- Dashboard loads without errors
- No "refused to connect" messages
- Charts and graphs display correctly
- Upload and analysis work properly

---

**🎯 Follow these exact steps to fix all connection issues!**