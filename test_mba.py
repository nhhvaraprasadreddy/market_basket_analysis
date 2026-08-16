#!/usr/bin/env python3

import pandas as pd
import sys
import os

# Add the backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from utils.mba_analysis import perform_mba_analysis

def test_mba_analysis():
    """Test the MBA analysis with sample data"""
    
    # Create sample transaction data
    sample_data = {
        'Transaction_ID': ['T001', 'T001', 'T001', 'T002', 'T002', 'T003', 'T003', 'T003', 'T004', 'T004'],
        'Item_Name': ['Bread', 'Butter', 'Milk', 'Bread', 'Butter', 'Bread', 'Milk', 'Cookies', 'Butter', 'Milk']
    }
    
    df = pd.DataFrame(sample_data)
    print("Sample Data:")
    print(df)
    print("\n" + "="*50 + "\n")
    
    # Test MBA analysis
    try:
        results = perform_mba_analysis(df, min_support=0.1, min_confidence=0.1, min_lift=1.0)
        
        print("MBA Analysis Results:")
        print(f"Number of rules found: {len(results['rules'])}")
        print(f"Number of frequent items: {len(results['frequent_items'])}")
        
        print("\nFrequent Items:")
        for item in results['frequent_items']:
            print(f"  {item['item']}: {item['frequency']}")
        
        print("\nAssociation Rules:")
        for rule in results['rules']:
            print(f"  {rule['antecedent']} -> {rule['consequent']}")
            print(f"    Support: {rule['support']:.4f}, Confidence: {rule['confidence']:.4f}, Lift: {rule['lift']:.4f}")
        
        return results
        
    except Exception as e:
        print(f"Error in MBA analysis: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    test_mba_analysis()