#!/usr/bin/env python3

import pandas as pd
import sys
import os

# Add the backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from utils.mba_analysis import perform_mba_analysis

def test_with_lower_thresholds():
    """Test the MBA analysis with much lower thresholds"""
    
    # Load the real dataset
    try:
        df = pd.read_csv('dataset/transactions.csv')
        print(f"Dataset: {len(df)} rows, {df['Transaction_ID'].nunique()} transactions, {df['Item_Name'].nunique()} items")
        
        # Analyze item frequencies
        try:
            item_counts = df['Item_Name'].value_counts()
            print("\nTop 10 most frequent items:")
            for item, count in item_counts.head(10).items():
                support = count / df['Transaction_ID'].nunique()
                print(f"  {item}: {count} transactions ({support:.4f} support)")
        except Exception as e:
            print(f"Error analyzing item frequencies: {str(e)}")
            return
        
        print("\n" + "="*50 + "\n")
        
        # Test with very low thresholds
        test_cases = [
            {"min_support": 0.001, "min_confidence": 0.1, "min_lift": 1.0},
            {"min_support": 0.002, "min_confidence": 0.2, "min_lift": 1.0},
            {"min_support": 0.005, "min_confidence": 0.1, "min_lift": 1.0}
        ]
        
        for i, params in enumerate(test_cases, 1):
            print(f"Test Case {i}: {params}")
            try:
                results = perform_mba_analysis(df, **params)
                
                print(f"  Rules found: {len(results['rules'])}")
                print(f"  Frequent items: {len(results['frequent_items'])}")
                
                if results['rules']:
                    print("  Top 5 rules by lift:")
                    # Sort rules by lift and show top 5
                    sorted_rules = sorted(results['rules'], key=lambda x: x['lift'], reverse=True)
                    for rule in sorted_rules[:5]:
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
    test_with_lower_thresholds()