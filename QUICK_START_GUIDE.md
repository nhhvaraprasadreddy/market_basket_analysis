# 🚀 QUICK START GUIDE - Market Basket Analysis

## ⚡ FASTEST WAY TO RUN

### Option 1: Automatic Startup (Recommended)
```bash
# Double-click this file or run in terminal:
start_system.bat
```

### Option 2: Manual Startup
```bash
# Terminal 1 - Backend
cd backend
uvicorn app:app --host 0.0.0.0 --port 8000 --reload

# Terminal 2 - Frontend  
cd frontend
python -m http.server 5500
```

## 🌐 ACCESS URLS

- **Frontend**: http://127.0.0.1:5500
- **Backend API**: http://127.0.0.1:8000
- **Backend Health**: http://127.0.0.1:8000/health

## 🧪 TEST CONNECTION

```bash
python test_connection.py
```

## 📋 PREREQUISITES

1. **Python 3.9+** installed
2. **Backend dependencies** installed:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

## 🔧 TROUBLESHOOTING

### ❌ "127.0.0.1 refused to connect"

**Problem**: Frontend not loading
**Solution**: 
```bash
cd frontend
python -m http.server 5500
```
Then open: http://127.0.0.1:5500

### ❌ "Failed to fetch" / CORS Error

**Problem**: Backend not reachable
**Solution**:
```bash
cd backend
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

### ❌ Backend Import Errors

**Problem**: Missing dependencies
**Solution**:
```bash
cd backend
pip install fastapi uvicorn pandas mlxtend python-multipart
```

## ✅ SUCCESS CHECKLIST

- [ ] Backend running at http://127.0.0.1:8000
- [ ] Frontend running at http://127.0.0.1:5500  
- [ ] Can upload CSV file
- [ ] Analysis runs without errors
- [ ] Results display correctly

## 🎯 QUICK TEST

1. Open http://127.0.0.1:5500
2. Upload `dataset/transactions.csv`
3. Click "Run Analysis"
4. Should see results in ~5-10 seconds

## 📞 STILL HAVING ISSUES?

Run the connection test:
```bash
python test_connection.py
```

This will tell you exactly what's wrong and how to fix it.