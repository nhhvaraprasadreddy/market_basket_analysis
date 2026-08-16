import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules, fpgrowth
import logging

logger = logging.getLogger(__name__)

def perform_mba_analysis(df, min_support=0.01, min_confidence=0.5, min_lift=1.0, algorithm="Apriori"):
    """Perform Market Basket Analysis on transaction data with enhanced cross-selling support"""
    
    logger.info(f"Starting MBA analysis with {len(df)} records")
    logger.info(f"Parameters: support={min_support}, confidence={min_confidence}, lift={min_lift}, algorithm={algorithm}")
    
    # Preprocess data - handle case insensitive columns
    try:
        # Normalize column names to handle case variations
        df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
        
        # Map common column variations
        column_mapping = {
            'transaction_id': 'Transaction_ID',
            'item_name': 'Item_Name',
            'transactionid': 'Transaction_ID',
            'itemname': 'Item_Name'
        }
        
        for old_col, new_col in column_mapping.items():
            if old_col in df.columns:
                df = df.rename(columns={old_col: new_col})
        
        # Keep only required columns
        required_cols = ['Transaction_ID', 'Item_Name']
        if not all(col in df.columns for col in required_cols):
            available_cols = list(df.columns)
            raise ValueError(f"Required columns {required_cols} not found. Available: {available_cols}")
        
        df = df[required_cols].copy()
        
        # Clean data
        df = df.dropna()
        df['Transaction_ID'] = df['Transaction_ID'].astype(str)
        df['Item_Name'] = df['Item_Name'].astype(str).str.strip()
        
        # Remove duplicates within the same transaction
        df = df.drop_duplicates()
        
        logger.info(f"Cleaned data: {len(df)} records, {df['Transaction_ID'].nunique()} transactions, {df['Item_Name'].nunique()} unique items")
        
    except Exception as e:
        raise ValueError(f"Failed to preprocess data: {str(e)}")
    
    # Create basket format - one-hot encoding
    try:
        basket = df.pivot_table(
            index='Transaction_ID',
            columns='Item_Name',
            aggfunc=lambda x: 1,
            fill_value=0
        )
        
        # Convert to boolean for better performance
        basket = basket.astype(bool)
        
        logger.info(f"Basket created: {basket.shape[0]} transactions, {basket.shape[1]} items")
    except Exception as e:
        raise ValueError(f"Failed to create basket matrix: {str(e)}")
    
    # Get frequent items with actual counts for display
    try:
        item_counts = df['Item_Name'].value_counts()
        frequent_items = []
        for item, count in item_counts.head(20).items():  # Increased to 20 for better cross-selling
            frequent_items.append({"item": str(item), "frequency": int(count)})
        logger.info(f"Top frequent items: {[item['item'] for item in frequent_items[:5]]}")
    except Exception as e:
        raise ValueError(f"Failed to calculate item frequencies: {str(e)}")
    
    # Find frequent itemsets using selected algorithm
    try:
        if algorithm.lower() in ["fp-growth", "fpgrowth"]:
            frequent_itemsets = fpgrowth(basket, min_support=min_support, use_colnames=True)
            logger.info(f"Using FP-Growth algorithm")
        else:  # Default to Apriori
            frequent_itemsets = apriori(basket, min_support=min_support, use_colnames=True)
            logger.info(f"Using Apriori algorithm")
        
        logger.info(f"Found {len(frequent_itemsets)} frequent itemsets")
    except Exception as e:
        raise ValueError(f"Failed to find frequent itemsets using {algorithm}: {str(e)}")
    
    if frequent_itemsets.empty:
        logger.warning("No frequent itemsets found - try lowering min_support")
        return {
            "algorithm": algorithm,
            "rules": [],
            "frequent_items": frequent_items,
            "cross_selling_data": generate_cross_selling_data([], frequent_items)
        }
    
    # Generate association rules only if we have itemsets with 2+ items
    try:
        itemsets_with_multiple_items = frequent_itemsets[frequent_itemsets['itemsets'].apply(len) >= 2]
        logger.info(f"Itemsets with 2+ items: {len(itemsets_with_multiple_items)}")
    except Exception as e:
        raise ValueError(f"Failed to filter itemsets: {str(e)}")
    
    if itemsets_with_multiple_items.empty:
        logger.warning("No itemsets with multiple items - try lowering min_support")
        return {
            "algorithm": algorithm,
            "rules": [],
            "frequent_items": frequent_items,
            "cross_selling_data": generate_cross_selling_data([], frequent_items)
        }
    
    # Generate association rules
    try:
        rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=min_confidence)
        logger.info(f"Generated {len(rules)} rules before lift filtering")
    except Exception as e:
        raise ValueError(f"Failed to generate association rules: {str(e)}")
    
    # Filter by lift
    try:
        rules = rules[rules['lift'] >= min_lift]
        logger.info(f"Rules after lift filtering: {len(rules)}")
    except Exception as e:
        raise ValueError(f"Failed to filter rules by lift: {str(e)}")
    
    # Format rules for JSON response with enhanced data for cross-selling
    rules_list = []
    for _, rule in rules.iterrows():
        # Calculate additional metrics for cross-selling
        antecedent_items = list(rule['antecedents'])
        consequent_items = list(rule['consequents'])
        
        # Ensure items are strings for network graph compatibility
        antecedent_items = [str(item) for item in antecedent_items]
        consequent_items = [str(item) for item in consequent_items]
        
        # Cross-selling score (confidence * lift)
        cross_selling_score = float(rule['confidence']) * float(rule['lift'])
        
        # Co-occurrence count (approximate)
        co_occurrence = int(float(rule['support']) * len(basket))
        
        # Handle NaN/Inf values for JSON serialization
        support_val = float(rule['support'])
        confidence_val = float(rule['confidence'])
        lift_val = float(rule['lift'])
        conviction_val = float(rule.get('conviction', 1.0)) if 'conviction' in rule else 1.0
        
        # Replace NaN/Inf with safe values
        import math
        if math.isnan(support_val) or math.isinf(support_val):
            support_val = 0.0
        if math.isnan(confidence_val) or math.isinf(confidence_val):
            confidence_val = 0.0
        if math.isnan(lift_val) or math.isinf(lift_val):
            lift_val = 1.0
        if math.isnan(conviction_val) or math.isinf(conviction_val):
            conviction_val = 1.0
        if math.isnan(cross_selling_score) or math.isinf(cross_selling_score):
            cross_selling_score = 0.0
            
        rules_list.append({
            "antecedent": antecedent_items,
            "consequent": consequent_items,
            "support": round(support_val, 4),
            "confidence": round(confidence_val, 4),
            "lift": round(lift_val, 4),
            "cross_selling_score": round(cross_selling_score, 4),
            "co_occurrence_count": co_occurrence,
            "conviction": round(conviction_val, 4)
        })
    
    # Sort rules by cross-selling score (descending)
    rules_list.sort(key=lambda x: x['cross_selling_score'], reverse=True)
    
    # Filter rules for network visualization (top 50 strongest rules)
    network_rules = [rule for rule in rules_list if rule['lift'] > 1.2 or rule['confidence'] > 0.5][:50]
    
    # Generate cross-selling data
    cross_selling_data = generate_cross_selling_data(rules_list, frequent_items)
    
    logger.info(f"Returning {len(rules_list)} rules ({len(network_rules)} for network) and {len(frequent_items)} frequent items")
    
    return {
        "algorithm": algorithm,
        "rules": rules_list,
        "network_rules": network_rules,  # Filtered rules for cleaner network visualization
        "frequent_items": frequent_items,
        "cross_selling_data": cross_selling_data
    }

def generate_cross_selling_data(rules_list, frequent_items):
    """Generate cross-selling recommendations for each product"""
    cross_selling_map = {}
    
    # Create a map of items to their cross-selling partners
    for rule in rules_list:
        # For each antecedent item, add consequent items as cross-sell suggestions
        for ant_item in rule['antecedent']:
            ant_item = str(ant_item)  # Ensure string format
            if ant_item not in cross_selling_map:
                cross_selling_map[ant_item] = []
            
            for cons_item in rule['consequent']:
                cons_item = str(cons_item)  # Ensure string format
                # Ensure all values are JSON serializable
                import math
                confidence = rule['confidence']
                lift = rule['lift']
                score = rule['cross_selling_score']
                
                if math.isnan(confidence) or math.isinf(confidence):
                    confidence = 0.0
                if math.isnan(lift) or math.isinf(lift):
                    lift = 1.0
                if math.isnan(score) or math.isinf(score):
                    score = 0.0
                    
                cross_selling_map[ant_item].append({
                    'item': cons_item,
                    'confidence': round(confidence, 4),
                    'lift': round(lift, 4),
                    'cross_selling_score': round(score, 4),
                    'co_occurrence_count': rule['co_occurrence_count']
                })
        
        # Also add reverse relationships (consequent -> antecedent)
        for cons_item in rule['consequent']:
            cons_item = str(cons_item)  # Ensure string format
            if cons_item not in cross_selling_map:
                cross_selling_map[cons_item] = []
            
            for ant_item in rule['antecedent']:
                ant_item = str(ant_item)  # Ensure string format
                # Ensure all values are JSON serializable
                import math
                confidence = rule['confidence']
                lift = rule['lift']
                score = rule['cross_selling_score']
                
                if math.isnan(confidence) or math.isinf(confidence):
                    confidence = 0.0
                if math.isnan(lift) or math.isinf(lift):
                    lift = 1.0
                if math.isnan(score) or math.isinf(score):
                    score = 0.0
                    
                cross_selling_map[cons_item].append({
                    'item': ant_item,
                    'confidence': round(confidence, 4),
                    'lift': round(lift, 4),
                    'cross_selling_score': round(score, 4),
                    'co_occurrence_count': rule['co_occurrence_count']
                })
    
    # Sort cross-sell suggestions by score and remove duplicates
    for item in cross_selling_map:
        # Remove duplicates and sort by cross-selling score
        seen = set()
        unique_suggestions = []
        for suggestion in cross_selling_map[item]:
            suggestion_item = str(suggestion['item'])  # Ensure string format
            if suggestion_item not in seen:
                seen.add(suggestion_item)
                suggestion['item'] = suggestion_item  # Update with string format
                unique_suggestions.append(suggestion)
        
        # Sort by cross-selling score and take top 10
        unique_suggestions.sort(key=lambda x: x['cross_selling_score'], reverse=True)
        cross_selling_map[item] = unique_suggestions[:10]
    
    return cross_selling_map