# 🚀 FIXED Run Instructions - Market Basket Analysis System

## ⚡ Quick Start (Recommended)

### Option 1: Automatic Startup
```bash
# Double-click this file:
start_system.bat
```

### Option 2: Manual Step-by-Step

#### Step 1: Start Backend
```bash
# Open Command Prompt/Terminal
cd backend
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```
**Backend will run at:** http://127.0.0.1:8000

#### Step 2: Start Frontend (New Terminal)
```bash
# Open NEW Command Prompt/Terminal
cd frontend
python -m http.server 5500
```
**Frontend will run at:** http://127.0.0.1:5500

#### Step 3: Test Connection
```bash
# Open THIRD Command Prompt/Terminal
python test_connection_simple.py
```

#### Step 4: Open Application
**Open browser:** http://127.0.0.1:5500/index.html

## 🧪 Troubleshooting Steps

### Problem: "127.0.0.1 refused to connect"

#### Solution 1: Check Servers
```bash
# Test if servers are running
python test_connection_simple.py
```

#### Solution 2: Start Servers Individually
```bash
# Terminal 1: Backend
cd backend
uvicorn app:app --host 0.0.0.0 --port 8000 --reload

# Terminal 2: Frontend  
cd frontend
python -m http.server 5500
```

#### Solution 3: Check URLs
- Backend: http://127.0.0.1:8000/health
- Frontend Test: http://127.0.0.1:5500/test.html
- Main App: http://127.0.0.1:5500/index.html

### Problem: "Failed to fetch" or CORS errors

#### Solution: Restart Backend with Correct Host
```bash
cd backend
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

### Problem: Frontend shows blank page

#### Solution: Check Browser Console
1. Press F12 in browser
2. Check Console tab for errors
3. Verify all JS libraries load correctly

## 📋 Verification Checklist

Before using the system, verify:

- [ ] Backend running: http://127.0.0.1:8000/health returns `{"status": "healthy"}`
- [ ] Frontend running: http://127.0.0.1:5500/test.html shows "Frontend Server is Working!"
- [ ] Main app loads: http://127.0.0.1:5500/index.html shows the dashboard
- [ ] No console errors in browser (F12 → Console)
- [ ] Sample CSV file exists: dataset/transactions.csv

## 🎯 Test the Complete System

1. **Upload CSV**: Use dataset/transactions.csv
2. **Set Parameters**: 
   - Algorithm: FP-Growth
   - Min Support: 0.005
   - Min Confidence: 0.1
   - Min Lift: 1.0
3. **Run Analysis**: Click "Run Analysis"
4. **Verify Results**: 
   - Frequent items chart appears
   - Network graph shows relationships
   - Association rules table populated
5. **Test Cross-Selling**:
   - Select product from dropdown
   - Click "Show Cross-Selling Opportunities"
   - Verify suggestions and mini network appear

## 🔧 Alternative Frontend Servers

If Python server doesn't work:

### Node.js Server
```bash
cd frontend
npx serve . -p 5500
```

### PHP Server (if available)
```bash
cd frontend
php -S 127.0.0.1:5500
```

### VS Code Live Server
1. Install "Live Server" extension
2. Right-click index.html
3. Select "Open with Live Server"

## 📞 Still Having Issues?

1. **Check Python Version**: `python --version` (should be 3.7+)
2. **Check Port Availability**: 
   - `netstat -an | findstr :8000` (backend)
   - `netstat -an | findstr :5500` (frontend)
3. **Firewall**: Ensure ports 8000 and 5500 are not blocked
4. **Antivirus**: Temporarily disable if blocking connections

## ✅ Success Indicators

When everything works correctly:
- Backend terminal shows: "Uvicorn running on http://0.0.0.0:8000"
- Frontend terminal shows: "Serving HTTP on 0.0.0.0 port 5500"
- Browser loads dashboard without errors
- Upload and analysis work end-to-end
- Cross-selling features function properly

---

**🎉 Follow these exact steps and your system will work perfectly!**