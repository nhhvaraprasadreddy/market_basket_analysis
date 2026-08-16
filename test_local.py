import requests
import pandas as pd

# Test the local backend
def test_local_backend():
    # Read the sample dataset
    try:
        df = pd.read_csv('dataset/transactions.csv')
        print(f"Dataset loaded: {len(df)} records")
        print(f"Sample data:\n{df.head()}")
    except FileNotFoundError:
        print("❌ Dataset file not found. Please ensure dataset/transactions.csv exists.")
        return
    except Exception as e:
        print(f"❌ Error loading dataset: {str(e)}")
        return
    
    # Test the MBA analysis directly
    from backend.utils.mba_analysis import perform_mba_analysis
    
    try:
        results = perform_mba_analysis(df, min_support=0.005, min_confidence=0.3, min_lift=1.0)
    except Exception as e:
        print(f"❌ Error in MBA analysis: {str(e)}")
        return
    
    try:
        print(f"\nMBA Analysis Results:")
        print(f"Number of rules: {len(results['rules'])}")
        print(f"Number of frequent items: {len(results['frequent_items'])}")
        
        if results['rules']:
            print(f"\nTop 5 Association Rules:")
            for i, rule in enumerate(results['rules'][:5]):
                print(f"{i+1}. {rule['antecedent']} -> {rule['consequent']} "
                      f"(support: {rule['support']:.3f}, confidence: {rule['confidence']:.3f}, lift: {rule['lift']:.3f})")
        
        if results['frequent_items']:
            print(f"\nTop 10 Frequent Items:")
            for i, item in enumerate(results['frequent_items'][:10]):
                print(f"{i+1}. {item['item']}: {item['frequency']}")
    except Exception as e:
        print(f"Error displaying results: {str(e)}")

if __name__ == "__main__":
    test_local_backend()