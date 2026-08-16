from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import pandas as pd
import io
import logging
from utils.mba_analysis import perform_mba_analysis
from mangum import Mangum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Market Basket Analysis API")

# Enable CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
logger.info("CORS middleware configured successfully")

@app.get("/")
async def root():
    return {"message": "Market Basket Analysis API", "status": "running"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/api/analyze")
async def analyze_transactions(
    file: UploadFile = File(...),
    min_support: float = Form(0.01),
    min_confidence: float = Form(0.5),
    min_lift: float = Form(1.0),
    algorithm: str = Form("Apriori")
):
    try:
        # Validate input parameters
        if file is None:
            raise HTTPException(status_code=400, detail="No file provided")
        
        # Validate file object
        if not hasattr(file, 'filename') or not hasattr(file, 'read'):
            raise HTTPException(status_code=400, detail="Invalid file object")
            
        logger.info(f"Received file: {file.filename}")
        logger.info(f"Parameters: support={min_support}, confidence={min_confidence}, lift={min_lift}, algorithm={algorithm}")
        
        # Validate parameters
        if not (0 < min_support <= 1):
            raise HTTPException(status_code=400, detail="min_support must be between 0 and 1")
        if not (0 < min_confidence <= 1):
            raise HTTPException(status_code=400, detail="min_confidence must be between 0 and 1")
        if min_lift < 0:
            raise HTTPException(status_code=400, detail="min_lift must be non-negative")
        
        # Validate file type
        if not file.filename or not file.filename.endswith('.csv'):
            raise HTTPException(status_code=400, detail="Only CSV files are supported")
        
        # Read CSV file
        try:
            contents = await file.read()
            df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
        except UnicodeDecodeError:
            raise HTTPException(status_code=400, detail="File encoding not supported. Please use UTF-8 encoded CSV")
        except pd.errors.EmptyDataError:
            raise HTTPException(status_code=400, detail="CSV file is empty")
        except pd.errors.ParserError as e:
            raise HTTPException(status_code=400, detail=f"Invalid CSV format: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to read CSV file: {str(e)}")
        
        logger.info(f"CSV loaded: {len(df)} rows, columns: {list(df.columns)}")
        
        # Validate required columns
        required_columns = ['Transaction_ID', 'Item_Name']
        if not all(col in df.columns for col in required_columns):
            raise HTTPException(
                status_code=400, 
                detail=f"CSV must contain columns: {required_columns}. Found: {list(df.columns)}"
            )
        
        # Perform MBA analysis
        try:
            results = perform_mba_analysis(df, min_support, min_confidence, min_lift, algorithm)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")
        
        logger.info(f"Analysis complete: {len(results['rules'])} rules, {len(results['frequent_items'])} frequent items")
        
        # Add analysis metadata
        try:
            results['analysis_info'] = {
                'total_transactions': len(df['Transaction_ID'].unique()),
                'total_items': len(df['Item_Name'].unique()),
                'parameters': {
                    'min_support': min_support,
                    'min_confidence': min_confidence,
                    'min_lift': min_lift
                }
            }
        except Exception as e:
            logger.warning(f"Failed to add analysis metadata: {str(e)}")
        
        return JSONResponse(content=results)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

# Lambda handler
handler = Mangum(app)