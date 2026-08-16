#!/usr/bin/env python3

import pandas as pd
import sys
import os

# Add the backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from utils.mba_analysis import perform_mba_analysis

def test_real_dataset():
    """Test the MBA analysis with the real dataset"""
    
    # Load the real dataset
    try:
        df = pd.read_csv('dataset/transactions.csv')
        print(f"Loaded dataset with {len(df)} rows")
        print(f"Columns: {list(df.columns)}")
        print(f"Unique transactions: {df['Transaction_ID'].nunique()}")
        print(f"Unique items: {df['Item_Name'].nunique()}")
        print("\nSample data:")
        print(df.head(10))
        print("\n" + "="*50 + "\n")
        
        # Test with different parameters
        test_cases = [
            {"min_support": 0.01, "min_confidence": 0.5, "min_lift": 1.0},
            {"min_support": 0.02, "min_confidence": 0.3, "min_lift": 1.2},
            {"min_support": 0.005, "min_confidence": 0.4, "min_lift": 1.1}
        ]
        
        for i, params in enumerate(test_cases, 1):
            print(f"Test Case {i}: {params}")
            try:
                results = perform_mba_analysis(df, **params)
                
                print(f"  Rules found: {len(results['rules'])}")
                print(f"  Frequent items: {len(results['frequent_items'])}")
                
                if results['rules']:
                    print("  Sample rules:")
                    for rule in results['rules'][:3]:  # Show first 3 rules
                        print(f"    {rule['antecedent']} -> {rule['consequent']}")
                        print(f"      Support: {rule['support']:.4f}, Confidence: {rule['confidence']:.4f}, Lift: {rule['lift']:.4f}")
                else:
                    print("  No rules found with these parameters")
                
                print()
                
            except Exception as e:
                print(f"  Error: {str(e)}")
                import traceback
                traceback.print_exc()
                print()
        
    except Exception as e:
        print(f"Error loading dataset: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_real_dataset()