import pandas as pd
import sys
import os
sys.path.append('backend')
from utils.mba_analysis import perform_mba_analysis

def test_mba_logic():
    """Test the MBA analysis logic directly"""
    
    # Load the dataset
    df = pd.read_csv('dataset/transactions.csv')
    print(f"Dataset loaded: {len(df)} records")
    print(f"Unique transactions: {len(df['Transaction_ID'].unique())}")
    print(f"Unique items: {len(df['Item_Name'].unique())}")
    print(f"Sample items: {df['Item_Name'].unique()[:10]}")
    
    # Test with lower thresholds to ensure results
    min_support = 0.005  # Lower support
    min_confidence = 0.1  # Lower confidence  
    min_lift = 1.0
    
    print(f"\nTesting with: support={min_support}, confidence={min_confidence}, lift={min_lift}")
    
    try:
        # Test Apriori
        results = perform_mba_analysis(df, min_support, min_confidence, min_lift, "Apriori")
        
        print(f"\nApriori Results:")
        print(f"Algorithm: {results['algorithm']}")
        print(f"Frequent items: {len(results['frequent_items'])}")
        print(f"Association rules: {len(results['rules'])}")
        
        if results['frequent_items']:
            print(f"Top 5 frequent items:")
            for item in results['frequent_items'][:5]:
                print(f"  {item['item']}: {item['frequency']}")
        
        if results['rules']:
            print(f"Top 3 rules:")
            for rule in results['rules'][:3]:
                print(f"  {rule['antecedent']} -> {rule['consequent']} (lift: {rule['lift']})")
        
        # Test FP-Growth
        results2 = perform_mba_analysis(df, min_support, min_confidence, min_lift, "FP-Growth")
        
        print(f"\nFP-Growth Results:")
        print(f"Algorithm: {results2['algorithm']}")
        print(f"Frequent items: {len(results2['frequent_items'])}")
        print(f"Association rules: {len(results2['rules'])}")
        
        return True
        
    except Exception as e:
        print(f"Error in MBA analysis: {e}")
        return False

if __name__ == "__main__":
    test_mba_logic()