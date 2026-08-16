# 🛒 Real-Time Market Basket Analysis Web Application

A complete web application for performing Market Basket Analysis on transactional data with real-time visualization and AWS deployment.

## 🚨 Problem Statement

**Existing Drawback**: The existing Market Basket Analysis method using Apriori is slow and computationally expensive because it generates a huge number of candidate itemsets, causing exponential growth in computation time. It becomes inefficient and unsuitable for large datasets or real-time analytics.

## ✅ Proposed Solution

**Implement FP-Growth along with Apriori**

FP-Growth overcomes the main drawback because:
- It does NOT generate candidate itemsets
- Uses an FP-tree for compressed pattern representation  
- Runs dramatically faster on datasets with thousands of transactions
- Supports real-time analysis

The system allows users to choose between Apriori and FP-Growth to compare performance and accuracy.

## 🚀 Features

- **CSV Upload & Processing**: Upload transaction data and get instant MBA results
- **Interactive Dashboard**: Responsive UI with Bootstrap 5
- **Real-time Visualizations**: 
  - Bar chart of top frequent items (Chart.js)
  - Network graph of item relationships (D3.js)
  - Dynamic association rules table
- **Configurable Parameters**: Adjust min_support, min_confidence, and min_lift
- **Download Results**: Export analysis results as CSV
- **AWS Deployment**: Serverless architecture with Lambda + API Gateway + S3

## 📁 Project Structure

```
market-basket-analysis/
├── backend/
│   ├── app.py                 # FastAPI application
│   ├── requirements.txt       # Python dependencies
│   └── utils/
│       └── mba_analysis.py    # MBA logic using MLxtend
├── frontend/
│   ├── index.html            # Main dashboard
│   ├── style.css             # Custom styles
│   └── script.js             # Frontend logic
├── dataset/
│   └── transactions.csv      # Sample dataset (2500+ transactions)
├── template.yaml             # AWS SAM deployment template
└── README.md
```

## 🛠️ Local Development

### Prerequisites
- Python 3.9+
- Node.js (for local server)
- AWS CLI (for deployment)
- AWS SAM CLI (for deployment)

### Setup Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app:app --reload --port 8000
```

### Setup Frontend
```bash
cd frontend
# Serve with any local server, e.g.:
python -m http.server 3000
# or
npx serve .
```

## ☁️ AWS Deployment

### 1. Deploy Backend (Lambda + API Gateway)
```bash
# Build and deploy
sam build
sam deploy --guided

# Note the API Gateway URL from outputs
```

### 2. Update Frontend Configuration
Update the `API_ENDPOINT` in `frontend/script.js` with your API Gateway URL:
```javascript
const API_ENDPOINT = 'https://your-api-id.execute-api.region.amazonaws.com/prod/api/analyze';
```

### 3. Deploy Frontend (S3)
```bash
# Upload to S3 bucket (use bucket name from SAM outputs)
aws s3 sync frontend/ s3://your-bucket-name --delete
```

### 4. Access Application
Visit the S3 website URL provided in the SAM outputs.

## 📊 Sample Dataset

The included `dataset/transactions.csv` contains:
- **7,447 transaction records** across **2,500 unique transactions**
- **496 unique customers** over **2 months**
- **15 grocery products** with realistic pricing
- Random quantities (1-5) and purchase patterns

## 🔧 API Usage

### Endpoint
```
POST /api/analyze
```

### Request
- **Content-Type**: `multipart/form-data`
- **file**: CSV file with columns: `Transaction_ID`, `Item_Name`
- **min_support**: Float (default: 0.01)
- **min_confidence**: Float (default: 0.5)
- **min_lift**: Float (default: 1.0)

### Response
```json
{
  "rules": [
    {
      "antecedent": ["Bread"],
      "consequent": ["Butter"],
      "support": 0.22,
      "confidence": 0.8,
      "lift": 1.4
    }
  ],
  "frequent_items": [
    {"item": "Bread", "frequency": 320},
    {"item": "Milk", "frequency": 290}
  ]
}
```

## 🎯 Key Technologies

- **Backend**: FastAPI, Pandas, MLxtend, Uvicorn
- **Frontend**: HTML5, Bootstrap 5, Chart.js, D3.js
- **AWS**: Lambda, API Gateway, S3, CloudFormation (SAM)
- **Analysis**: Apriori algorithm for frequent itemsets and association rules

## 📈 Performance Notes

- Lambda timeout: 30 seconds
- Memory: 512MB
- Supports files up to ~10MB
- Optimized for datasets with 1K-50K transactions

## 🔒 Security Features

- CORS enabled for cross-origin requests
- File type validation (CSV only)
- Input parameter validation
- Error handling and user feedback

## 🚀 Future Enhancements

- AWS Cognito authentication
- S3 storage for upload history
- PDF report generation
- Real-time streaming analysis
- Advanced visualization options