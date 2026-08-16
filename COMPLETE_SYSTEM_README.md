# 🛒 Complete Market Basket Analysis & Cross-Selling System

A comprehensive web application for Market Basket Analysis with advanced cross-selling features, supporting both Apriori and FP-Growth algorithms.

## 🚀 Key Features

### ✅ Core MBA Features
- **Dual Algorithm Support**: Apriori (traditional) and FP-Growth (fast)
- **Real-time Analysis**: Process CSV files instantly
- **Interactive Dashboard**: Bootstrap 5 responsive UI
- **Configurable Parameters**: Adjust min_support, min_confidence, min_lift

### 🎯 Cross-Selling Features (NEW)
- **Product Selector**: Choose any product for cross-selling analysis
- **Smart Recommendations**: AI-powered suggestions with confidence scores
- **Mini Network Graph**: Visualize product relationships
- **Cross-Selling Table**: Detailed metrics and co-occurrence data
- **Strategic Recommendations**: Actionable business insights

### 📊 Enhanced Visualizations
- **Frequent Items Chart**: Top 15 items with Chart.js
- **Main Network Graph**: Item relationships with vis-network
- **Mini Cross-Sell Graph**: Product-specific relationship network
- **Interactive Tables**: Sortable association rules and cross-sell data

## 🏗️ System Architecture

```
market-basket-analysis/
├── backend/
│   ├── app.py                 # FastAPI application with CORS
│   ├── requirements.txt       # Python dependencies
│   └── utils/
│       └── mba_analysis.py    # Enhanced MBA with cross-selling
├── frontend/
│   ├── index.html            # Complete dashboard with cross-selling
│   ├── script.js             # Full functionality + cross-selling
│   └── style.css             # Enhanced styling
├── dataset/
│   └── transactions.csv      # Sample dataset
└── COMPLETE_SYSTEM_README.md # This file
```

## 🛠️ Quick Start Guide

### 1. Backend Setup
```bash
cd backend
pip install -r requirements.txt
uvicorn app:app --reload --port 8000
```

### 2. Frontend Setup
```bash
cd frontend
# Option 1: Python server
python -m http.server 5500

# Option 2: Node.js server
npx serve . -p 5500

# Option 3: Live Server (VS Code extension)
# Right-click index.html -> "Open with Live Server"
```

### 3. Access Application
- Open browser: `http://localhost:5500`
- Backend API: `http://localhost:8000`
- API Docs: `http://localhost:8000/docs`

## 📋 CSV Data Format

Your CSV file must contain these columns:
```csv
Transaction_ID,Item_Name
T001,Bread
T001,Butter
T002,Milk
T002,Eggs
```

**Optional columns** (will be ignored):
- Date_of_Purchase, Time_of_Purchase, Customer_ID, Item_ID, Quantity, Price

## 🎯 How to Use Cross-Selling Features

### Step 1: Run Analysis
1. Upload your CSV file
2. Choose algorithm (Apriori or FP-Growth)
3. Set parameters (support: 0.005, confidence: 0.1, lift: 1.0)
4. Click "Run Analysis"

### Step 2: Cross-Selling Analysis
1. After analysis completes, the "Cross-Selling Analysis" card appears
2. Select a product from the dropdown
3. Click "Show Cross-Selling Opportunities"

### Step 3: Review Results
- **Top Recommendations**: Best cross-selling products with scores
- **Mini Network**: Visual relationships for selected product
- **Detailed Table**: Complete metrics (confidence, lift, co-occurrence)
- **Strategic Recommendations**: Actionable business insights

## 📊 Understanding Cross-Selling Metrics

### Cross-Selling Score
- **Formula**: Confidence × Lift
- **Range**: 0.0 to ∞
- **Interpretation**:
  - > 2.0: Excellent cross-selling opportunity
  - 1.0-2.0: Good potential
  - < 1.0: Limited potential

### Confidence
- **Definition**: P(Consequent|Antecedent)
- **Range**: 0% to 100%
- **Example**: 80% of customers who buy Bread also buy Butter

### Lift
- **Definition**: Confidence / Expected Confidence
- **Range**: 0.0 to ∞
- **Interpretation**:
  - > 1.0: Positive correlation
  - = 1.0: No correlation
  - < 1.0: Negative correlation

### Co-occurrence Count
- **Definition**: Number of transactions containing both items
- **Use**: Indicates absolute frequency of the relationship

## 🔧 API Endpoints

### POST /api/analyze
**Request:**
```bash
curl -X POST "http://localhost:8000/api/analyze" \
  -F "file=@transactions.csv" \
  -F "min_support=0.005" \
  -F "min_confidence=0.1" \
  -F "min_lift=1.0" \
  -F "algorithm=FP-Growth"
```

**Response:**
```json
{
  "algorithm": "FP-Growth",
  "frequent_items": [
    {"item": "Bread", "frequency": 350}
  ],
  "rules": [
    {
      "antecedent": ["Bread"],
      "consequent": ["Butter"],
      "support": 0.02,
      "confidence": 0.7,
      "lift": 2.8,
      "cross_selling_score": 1.96,
      "co_occurrence_count": 45
    }
  ],
  "cross_selling_data": {
    "Bread": [
      {
        "item": "Butter",
        "confidence": 0.7,
        "lift": 2.8,
        "cross_selling_score": 1.96,
        "co_occurrence_count": 45
      }
    ]
  }
}
```

## 🐛 Troubleshooting

### Backend Issues
```bash
# Check if backend is running
curl http://localhost:8000/health

# Common fixes
pip install --upgrade mlxtend pandas fastapi
uvicorn app:app --reload --port 8000 --host 0.0.0.0
```

### Frontend Issues
```bash
# Check browser console for errors
# Ensure backend URL is correct in script.js
# Try different local server
```

### Data Issues
- **No rules found**: Lower min_support (try 0.001)
- **No frequent items**: Check CSV format
- **Empty charts**: Verify data has Transaction_ID and Item_Name columns

## 📈 Performance Optimization

### Algorithm Selection
- **Apriori**: Better for small datasets (< 1K transactions)
- **FP-Growth**: Better for large datasets (> 1K transactions)

### Parameter Tuning
- **min_support**: Start with 0.005, lower if no results
- **min_confidence**: Start with 0.1, adjust based on business needs
- **min_lift**: Keep at 1.0 for meaningful associations

### Data Preprocessing
- Remove duplicate transactions
- Clean item names (trim whitespace)
- Ensure consistent Transaction_ID format

## 🚀 Advanced Features

### Export Results
- Click "Export Results" to download CSV
- Includes all association rules with cross-selling scores
- Import into Excel or other analytics tools

### Network Visualization
- **Main Network**: Shows top 20 association rules
- **Mini Network**: Shows relationships for selected product
- **Interactive**: Hover for details, drag to rearrange

### Real-time Updates
- Results update automatically after analysis
- Cross-selling data refreshes when selecting different products
- No page reload required

## 🔒 Security Features

- CORS enabled for cross-origin requests
- File type validation (CSV only)
- Input parameter validation
- Error handling with user feedback
- No sensitive data storage

## 📊 Sample Business Use Cases

### Grocery Store
1. **Product Placement**: Place frequently associated items near each other
2. **Bundle Offers**: Create bundles based on high lift values
3. **Inventory Management**: Stock complementary items together

### E-commerce
1. **Recommendation Engine**: "Customers who bought X also bought Y"
2. **Cross-selling Campaigns**: Email campaigns for related products
3. **Website Layout**: Show related products on product pages

### Restaurant
1. **Menu Design**: Group complementary dishes
2. **Upselling**: Train staff on high-confidence associations
3. **Combo Meals**: Create combos based on frequent patterns

## 🎯 Next Steps

1. **Test with Sample Data**: Use included transactions.csv
2. **Upload Your Data**: Format your transaction data as CSV
3. **Experiment with Parameters**: Find optimal thresholds for your business
4. **Implement Recommendations**: Use insights for business decisions
5. **Monitor Performance**: Track impact of cross-selling strategies

## 📞 Support

For issues or questions:
1. Check browser console for errors
2. Verify backend is running on port 8000
3. Ensure CSV format matches requirements
4. Try different parameter values
5. Check network connectivity between frontend and backend

---

**🎉 You now have a complete Market Basket Analysis system with advanced cross-selling capabilities!**