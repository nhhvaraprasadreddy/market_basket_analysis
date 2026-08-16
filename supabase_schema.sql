-- =======================================================
-- Supabase Schema for Market Basket Analysis Project
-- Project: https://ewvjojmexowbiswqffnu.supabase.co
-- =======================================================

-- 1. Create the analyses storage table
CREATE TABLE IF NOT EXISTS market_basket_analyses (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    dataset_name TEXT NOT NULL,
    algorithm TEXT NOT NULL,
    min_support FLOAT NOT NULL,
    min_confidence FLOAT NOT NULL,
    min_lift FLOAT NOT NULL,
    total_rules INT DEFAULT 0,
    total_items INT DEFAULT 0,
    total_transactions INT DEFAULT 0,
    results JSONB NOT NULL
);

-- 2. Enable Row Level Security (RLS)
ALTER TABLE market_basket_analyses ENABLE ROW LEVEL SECURITY;

-- 3. Allow anonymous public read and insert access for dashboard app
CREATE POLICY "Allow public read access" 
ON market_basket_analyses FOR SELECT 
USING (true);

CREATE POLICY "Allow public insert access" 
ON market_basket_analyses FOR INSERT 
WITH CHECK (true);

CREATE POLICY "Allow public delete access" 
ON market_basket_analyses FOR DELETE 
USING (true);
