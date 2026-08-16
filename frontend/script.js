// Global variables
let analysisResults = null;
let frequentItemsChart = null;
let mainNetwork = null;
let miniNetwork = null;
let crossSellingData = null;

// API configuration (Adaptive for local & Vercel deployment)
const isLocal = window.location.hostname === '127.0.0.1' || window.location.hostname === 'localhost';
const BACKEND_BASE = isLocal ? 'http://127.0.0.1:8000' : window.location.origin;
const API_URL = `${BACKEND_BASE}/api/analyze`;
const HEALTH_URL = `${BACKEND_BASE}/health`;

// Supabase Configuration
const SUPABASE_URL = 'https://ewvjojmexowbiswqffnu.supabase.co';
const SUPABASE_KEY = 'sb_publishable_OdkqfkLCfHp_ZNutK85R6Q_oCH9tfcV';
let supabaseClient = null;

try {
    if (window.supabase && typeof window.supabase.createClient === 'function') {
        supabaseClient = window.supabase.createClient(SUPABASE_URL, SUPABASE_KEY);
        console.log('✅ Supabase client connected successfully');
    }
} catch (e) {
    console.warn('⚠️ Supabase init notice:', e);
}

// DOM elements
const form = document.getElementById('analysisForm');
const analyzeText = document.getElementById('analyzeText');
const loadingSpinner = document.getElementById('loadingSpinner');
const downloadBtn = document.getElementById('downloadBtn');
const saveSupabaseBtn = document.getElementById('saveSupabaseBtn');
const openHistoryModalBtn = document.getElementById('openHistoryModalBtn');
const alertContainer = document.getElementById('alertContainer');
const crossSellingCard = document.getElementById('crossSellingCard');
const productSelector = document.getElementById('productSelector');
const showCrossBtn = document.getElementById('showCrossBtn');
const crossSellingResults = document.getElementById('crossSellingResults');

// Event listeners
form.addEventListener('submit', handleFormSubmit);
downloadBtn.addEventListener('click', downloadResults);
if (saveSupabaseBtn) saveSupabaseBtn.addEventListener('click', saveAnalysisToSupabase);
if (openHistoryModalBtn) openHistoryModalBtn.addEventListener('click', openHistoryModal);
productSelector.addEventListener('change', handleProductSelection);
showCrossBtn.addEventListener('click', showCrossSellingAnalysis);
window.addEventListener('load', testBackendConnection);

// Test backend connection
async function testBackendConnection() {
    try {
        const response = await fetch(HEALTH_URL);
        if (response.ok) {
            console.log('✅ Backend connection successful');
        }
    } catch (error) {
        console.error('❌ Backend connection failed:', error.message);
        showAlert('⚠️ Backend server not reachable. Please start the backend server.', 'warning');
    }
}

// Handle form submission
async function handleFormSubmit(e) {
    e.preventDefault();
    
    const fileInput = document.getElementById('csvFile');
    const file = fileInput.files[0];
    
    if (!file) {
        showAlert('Please select a CSV file', 'danger');
        return;
    }
    
    setLoading(true);
    clearResults();
    
    try {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('min_support', document.getElementById('minSupport').value);
        formData.append('min_confidence', document.getElementById('minConfidence').value);
        formData.append('min_lift', document.getElementById('minLift').value);
        formData.append('algorithm', document.getElementById('algorithm').value);
        
        const response = await fetch(API_URL, {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
        }
        
        analysisResults = await response.json();
        crossSellingData = analysisResults.cross_selling_data || {};
        
        console.log('✅ Analysis results received:', analysisResults);
        
        displayResults(analysisResults);
        setupCrossSellingInterface();
        
        const rulesCount = analysisResults.rules.length;
        const itemsCount = analysisResults.frequent_items.length;
        
        let message = `✅ Analysis completed using ${analysisResults.algorithm}! Found ${rulesCount} association rules and ${itemsCount} frequent items.`;
        
        if (analysisResults.analysis_info) {
            const info = analysisResults.analysis_info;
            message += ` Dataset: ${info.total_transactions} transactions, ${info.total_items} unique items.`;
        }
        
        if (rulesCount === 0) {
            message += " Try lowering min_support, min_confidence, or min_lift values.";
        }
        
        showAlert(message, rulesCount > 0 ? 'success' : 'warning');
        downloadBtn.classList.remove('d-none');
        if (saveSupabaseBtn) saveSupabaseBtn.classList.remove('d-none');
        
    } catch (error) {
        console.error('Error:', error);
        let errorMessage = 'Unknown error occurred';
        
        if (error.message.includes('Failed to fetch')) {
            errorMessage = `Cannot connect to backend server. Please ensure the backend is running at http://127.0.0.1:8000`;
        } else {
            errorMessage = error.message;
        }
        
        showAlert(`❌ ${errorMessage}`, 'danger');
    } finally {
        setLoading(false);
    }
}

// Set loading state
function setLoading(loading) {
    if (loading) {
        analyzeText.classList.add('d-none');
        loadingSpinner.classList.remove('d-none');
        form.querySelector('button[type="submit"]').disabled = true;
    } else {
        analyzeText.classList.remove('d-none');
        loadingSpinner.classList.add('d-none');
        form.querySelector('button[type="submit"]').disabled = false;
    }
}

// Show alert
function showAlert(message, type) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show alert-custom`;
    alertDiv.setAttribute('role', 'alert');
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    alertContainer.innerHTML = '';
    alertContainer.appendChild(alertDiv);
    
    // Auto-dismiss after 10 seconds for success messages
    if (type === 'success') {
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, 10000);
    }
}

// Clear all results
function clearResults() {
    // Clear rules table
    const tbody = document.querySelector('#rulesTable tbody');
    if (tbody) tbody.innerHTML = '';
    
    // Clear cross-sell table
    const crossTbody = document.querySelector('#crossSellTable tbody');
    if (crossTbody) crossTbody.innerHTML = '';
    
    // Clear chart
    if (frequentItemsChart) {
        frequentItemsChart.destroy();
        frequentItemsChart = null;
    }
    
    // Clear networks
    if (mainNetwork) {
        mainNetwork.destroy();
        mainNetwork = null;
    }
    
    if (miniNetwork) {
        miniNetwork.destroy();
        miniNetwork = null;
    }
    
    // Hide cross-selling interface
    crossSellingCard.classList.add('d-none');
    crossSellingResults.classList.add('d-none');
    
    // Reset selectors
    productSelector.innerHTML = '<option value="">Choose a product...</option>';
    showCrossBtn.disabled = true;
    
    // Hide download button
    downloadBtn.classList.add('d-none');
    
    console.log('🧹 Results cleared');
}

// Display all results
function displayResults(results) {
    console.log('🎯 Displaying results:', results);
    
    displayRulesTable(results.rules);
    drawFrequentItemsChart(results.frequent_items);
    // Use pre-filtered network_rules if available, otherwise filter on frontend
    drawMainNetworkGraph(results.network_rules || results.rules);
}

// Display rules table
function displayRulesTable(rules) {
    const tbody = document.querySelector('#rulesTable tbody');
    tbody.innerHTML = '';
    
    if (!rules || rules.length === 0) {
        const row = tbody.insertRow();
        const cell = row.insertCell();
        cell.colSpan = 6;
        cell.className = 'text-center text-muted py-4';
        cell.innerHTML = '<em>No association rules found. Try lowering the thresholds.</em>';
        return;
    }
    
    rules.slice(0, 100).forEach(rule => {
        const row = tbody.insertRow();
        row.insertCell().textContent = rule.antecedent.join(', ');
        row.insertCell().textContent = rule.consequent.join(', ');
        row.insertCell().textContent = rule.support.toFixed(4);
        row.insertCell().textContent = rule.confidence.toFixed(4);
        row.insertCell().textContent = rule.lift.toFixed(4);
        row.insertCell().innerHTML = `<span class="badge bg-primary">${rule.cross_selling_score.toFixed(3)}</span>`;
    });
}

// Draw frequent items chart
function drawFrequentItemsChart(frequent_items) {
    console.log('📊 Drawing frequent items chart:', frequent_items);
    
    const ctx = document.getElementById('frequentItemsChart');
    const emptyState = document.getElementById('chartEmptyState');
    
    if (!ctx) {
        console.error('❌ Canvas element not found');
        return;
    }
    
    // Destroy existing chart
    if (frequentItemsChart) {
        frequentItemsChart.destroy();
        frequentItemsChart = null;
    }
    
    if (!frequent_items || frequent_items.length === 0) {
        console.warn('⚠️ No frequent items data');
        ctx.style.display = 'none';
        emptyState.classList.remove('d-none');
        return;
    }
    
    ctx.style.display = 'block';
    emptyState.classList.add('d-none');
    
    // Take top 15 items
    const topItems = frequent_items.slice(0, 15);
    const labels = topItems.map(item => item.item);
    const data = topItems.map(item => item.frequency);
    
    console.log('📊 Chart labels:', labels);
    console.log('📊 Chart data:', data);
    
    try {
        frequentItemsChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Frequency',
                    data: data,
                    backgroundColor: 'rgba(102, 126, 234, 0.8)',
                    borderColor: 'rgba(102, 126, 234, 1)',
                    borderWidth: 1,
                    borderRadius: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return `${context.label}: ${context.parsed.y} transactions`;
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Frequency'
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Items'
                        },
                        ticks: {
                            maxRotation: 45
                        }
                    }
                }
            }
        });
        
        console.log('✅ Chart created successfully with', labels.length, 'items');
    } catch (error) {
        console.error('❌ Chart creation failed:', error);
        ctx.style.display = 'none';
        emptyState.classList.remove('d-none');
    }
}

// Draw main network graph - clean and minimal
function drawMainNetworkGraph(rules) {
    const container = document.getElementById('networkGraph');
    const emptyState = document.getElementById('networkEmptyState');
    
    if (mainNetwork) {
        mainNetwork.destroy();
        mainNetwork = null;
    }
    
    if (!rules || rules.length === 0) {
        emptyState.classList.remove('d-none');
        return;
    }
    
    emptyState.classList.add('d-none');
    
    // Filter top 30 strongest rules (lift > 1.2)
    const topRules = rules
        .filter(r => r.lift > 1.2)
        .sort((a, b) => b.lift - a.lift)
        .slice(0, 30);
    
    if (topRules.length === 0) {
        emptyState.classList.remove('d-none');
        return;
    }
    
    const nodeSet = new Set();
    const edgeMap = new Map();
    
    // Collect nodes and create unique edges
    topRules.forEach(rule => {
        rule.antecedent.forEach(a => {
            nodeSet.add(a);
            rule.consequent.forEach(c => {
                if (a !== c) {
                    nodeSet.add(c);
                    const key = `${a}-${c}`;
                    if (!edgeMap.has(key) || edgeMap.get(key).lift < rule.lift) {
                        edgeMap.set(key, { from: a, to: c, ...rule });
                    }
                }
            });
        });
    });
    
    // Limit to top 20 nodes
    const nodes = Array.from(nodeSet).slice(0, 20).map(item => ({
        id: item,
        label: item,
        shape: 'dot',
        size: 18,
        color: '#667eea',
        font: { size: 11 }
    }));
    
    const nodeIds = new Set(nodes.map(n => n.id));
    const edges = Array.from(edgeMap.values())
        .filter(e => nodeIds.has(e.from) && nodeIds.has(e.to))
        .slice(0, 25)
        .map(e => ({
            from: e.from,
            to: e.to,
            width: Math.min(e.lift, 4),
            color: '#666',
            arrows: 'to',
            smooth: false,
            title: `${e.from} → ${e.to}\nLift: ${e.lift.toFixed(2)}\nConfidence: ${(e.confidence * 100).toFixed(1)}%`
        }));
    
    const data = { nodes: new vis.DataSet(nodes), edges: new vis.DataSet(edges) };
    const options = {
        physics: {
            enabled: true,
            stabilization: { iterations: 100 },
            barnesHut: { springLength: 200, avoidOverlap: 1 }
        },
        interaction: { hover: true, tooltipDelay: 200 }
    };
    
    mainNetwork = new vis.Network(container, data, options);
    mainNetwork.once('stabilizationIterationsDone', () => {
        mainNetwork.setOptions({ physics: false });
    });
}

// Setup cross-selling interface
function setupCrossSellingInterface() {
    if (!analysisResults || !analysisResults.frequent_items) return;
    
    // Populate product selector
    productSelector.innerHTML = '<option value="">Choose a product...</option>';
    
    analysisResults.frequent_items.forEach(item => {
        const option = document.createElement('option');
        option.value = item.item;
        option.textContent = `${item.item} (${item.frequency} transactions)`;
        productSelector.appendChild(option);
    });
    
    crossSellingCard.classList.remove('d-none');
}

// Handle product selection
function handleProductSelection() {
    const selectedProduct = productSelector.value;
    showCrossBtn.disabled = !selectedProduct;
}

// Show cross-selling analysis
function showCrossSellingAnalysis() {
    const selectedProduct = productSelector.value;
    if (!selectedProduct || !crossSellingData) return;
    
    console.log('🎯 Showing cross-selling for:', selectedProduct);
    
    // Get cross-selling suggestions for the selected product
    const suggestions = crossSellingData[selectedProduct] || [];
    
    // Update selected product info
    const productInfo = document.getElementById('selectedProductInfo');
    const productFreq = analysisResults.frequent_items.find(item => item.item === selectedProduct);
    productInfo.innerHTML = `
        <div class="alert alert-info">
            <strong>Selected Product:</strong> ${selectedProduct}<br>
            <strong>Frequency:</strong> ${productFreq ? productFreq.frequency : 'N/A'} transactions
        </div>
    `;
    
    // Display suggestions
    displayCrossSellSuggestions(suggestions, selectedProduct);
    
    // Draw mini network
    drawMiniNetworkGraph(selectedProduct, suggestions);
    
    // Generate recommendation text
    generateRecommendationText(selectedProduct, suggestions);
    
    // Display cross-sell table
    displayCrossSellTable(suggestions);
    
    crossSellingResults.classList.remove('d-none');
    
    // Scroll to results
    crossSellingResults.scrollIntoView({ behavior: 'smooth' });
}

// Display cross-sell suggestions
function displayCrossSellSuggestions(suggestions, selectedProduct) {
    const container = document.getElementById('crossSellSuggestions');
    
    if (!suggestions || suggestions.length === 0) {
        container.innerHTML = `
            <div class="alert alert-warning">
                <i class="fas fa-exclamation-triangle me-2"></i>
                No cross-selling opportunities found for ${selectedProduct}.
                Try lowering the analysis thresholds.
            </div>
        `;
        return;
    }
    
    const topSuggestions = suggestions.slice(0, 5);
    let html = '';
    
    topSuggestions.forEach((suggestion, index) => {
        html += `
            <div class="suggestion-item">
                <div class="d-flex justify-content-between align-items-center">
                    <div>
                        <strong>#${index + 1} ${suggestion.item}</strong>
                    </div>
                    <div>
                        <span class="metric-badge">Score: ${suggestion.cross_selling_score.toFixed(3)}</span>
                    </div>
                </div>
                <div class="mt-2">
                    <span class="metric-badge">Confidence: ${(suggestion.confidence * 100).toFixed(1)}%</span>
                    <span class="metric-badge">Lift: ${suggestion.lift.toFixed(2)}</span>
                    <span class="metric-badge">Co-occurrence: ${suggestion.co_occurrence_count}</span>
                </div>
            </div>
        `;
    });
    
    container.innerHTML = html;
}

// Draw mini network graph - clean radial layout
function drawMiniNetworkGraph(selectedProduct, suggestions) {
    const container = document.getElementById('miniNetworkGraph');
    
    if (miniNetwork) {
        miniNetwork.destroy();
        miniNetwork = null;
    }
    
    if (!suggestions || suggestions.length === 0) {
        container.innerHTML = '<div class="text-center text-muted py-4">No relationships to display</div>';
        return;
    }
    
    const nodes = [{
        id: selectedProduct,
        label: selectedProduct,
        size: 25,
        color: '#f5576c',
        x: 0, y: 0, fixed: true
    }];
    
    const edges = [];
    const topSuggestions = suggestions.slice(0, 6);
    const angleStep = (2 * Math.PI) / topSuggestions.length;
    
    topSuggestions.forEach((s, i) => {
        const angle = i * angleStep;
        nodes.push({
            id: s.item,
            label: s.item,
            size: 18,
            color: '#4facfe',
            x: 120 * Math.cos(angle),
            y: 120 * Math.sin(angle),
            fixed: true
        });
        
        edges.push({
            from: selectedProduct,
            to: s.item,
            width: Math.min(s.lift, 4),
            color: '#666',
            arrows: 'to',
            title: `Lift: ${s.lift.toFixed(2)}\nConfidence: ${(s.confidence * 100).toFixed(1)}%`
        });
    });
    
    const data = { nodes: new vis.DataSet(nodes), edges: new vis.DataSet(edges) };
    const options = {
        physics: { enabled: false },
        interaction: { hover: true, dragNodes: false, dragView: false, zoomView: false }
    };
    
    miniNetwork = new vis.Network(container, data, options);
}

// Generate recommendation text
function generateRecommendationText(selectedProduct, suggestions) {
    const container = document.getElementById('recommendationText');
    
    if (!suggestions || suggestions.length === 0) {
        container.innerHTML = `
            <h6><i class="fas fa-lightbulb me-2"></i>Recommendations</h6>
            <p>No specific cross-selling recommendations available for ${selectedProduct}. Consider analyzing with lower thresholds or collecting more transaction data.</p>
        `;
        return;
    }
    
    const topSuggestions = suggestions.slice(0, 3).map(s => s.item);
    const bestScore = suggestions[0].cross_selling_score;
    
    let recommendation = `
        <h6><i class="fas fa-lightbulb me-2"></i>Strategic Recommendations</h6>
        <p><strong>${selectedProduct}</strong> shows strong cross-selling potential with <strong>${topSuggestions.join(', ')}</strong>.</p>
    `;
    
    if (bestScore > 2.0) {
        recommendation += `<p><strong>High Priority:</strong> The cross-selling score of ${bestScore.toFixed(2)} indicates excellent bundling opportunities. Consider creating product bundles or placing these items near each other.</p>`;
    } else if (bestScore > 1.0) {
        recommendation += `<p><strong>Moderate Priority:</strong> Good cross-selling potential exists. Consider promotional campaigns or strategic product placement.</p>`;
    } else {
        recommendation += `<p><strong>Low Priority:</strong> Limited cross-selling potential. Focus on other product combinations or gather more data.</p>`;
    }
    
    recommendation += `<p><strong>Action Items:</strong> Place ${selectedProduct} near ${topSuggestions[0]}, offer bundle discounts, and track customer purchase patterns.</p>`;
    
    container.innerHTML = recommendation;
}

// Display cross-sell table
function displayCrossSellTable(suggestions) {
    const tbody = document.querySelector('#crossSellTable tbody');
    tbody.innerHTML = '';
    
    if (!suggestions || suggestions.length === 0) {
        const row = tbody.insertRow();
        const cell = row.insertCell();
        cell.colSpan = 5;
        cell.className = 'text-center text-muted py-4';
        cell.innerHTML = '<em>No cross-selling data available.</em>';
        return;
    }
    
    suggestions.forEach(suggestion => {
        const row = tbody.insertRow();
        row.insertCell().textContent = suggestion.item;
        
        const scoreCell = row.insertCell();
        scoreCell.innerHTML = `<span class="badge bg-primary">${suggestion.cross_selling_score.toFixed(3)}</span>`;
        
        row.insertCell().textContent = (suggestion.confidence * 100).toFixed(1) + '%';
        row.insertCell().textContent = suggestion.lift.toFixed(2);
        row.insertCell().textContent = suggestion.co_occurrence_count;
    });
}

// Download results
function downloadResults() {
    if (!analysisResults) return;
    
    try {
        const csv = convertToCSV(analysisResults.rules);
        const blob = new Blob([csv], { type: 'text/csv' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `mba_results_${new Date().toISOString().split('T')[0]}.csv`;
        a.click();
        window.URL.revokeObjectURL(url);
        
        showAlert('✅ Results exported successfully!', 'success');
    } catch (error) {
        console.error('Error downloading results:', error);
        showAlert('❌ Failed to export results', 'danger');
    }
}

// Convert results to CSV
function convertToCSV(rules) {
    const headers = ['Antecedent', 'Consequent', 'Support', 'Confidence', 'Lift', 'Cross_Sell_Score', 'Co_Occurrence_Count'];
    const rows = rules.map(rule => [
        rule.antecedent.join('; '),
        rule.consequent.join('; '),
        rule.support,
        rule.confidence,
        rule.lift,
        rule.cross_selling_score,
        rule.co_occurrence_count
    ]);
    
    return [headers, ...rows].map(row => row.join(',')).join('\n');
}

// Utility function to format numbers
function formatNumber(num, decimals = 2) {
    return parseFloat(num).toFixed(decimals);
}

// Escape HTML utility
function escapeHtml(text) {
    if (!text) return '';
    return String(text)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

// Local storage backup functions
function saveToLocalBackup(record) {
    try {
        const local = getLocalBackup();
        local.unshift({ ...record, id: 'local_' + Date.now(), created_at: new Date().toISOString() });
        localStorage.setItem('mba_local_history', JSON.stringify(local.slice(0, 20)));
    } catch(e) {}
}

function getLocalBackup() {
    try {
        const data = localStorage.getItem('mba_local_history');
        return data ? JSON.parse(data) : [];
    } catch(e) {
        return [];
    }
}

// Save Analysis to Supabase Cloud
async function saveAnalysisToSupabase() {
    if (!analysisResults) {
        showAlert('⚠️ No analysis results to save. Please run an analysis first.', 'warning');
        return;
    }
    
    const saveBtn = document.getElementById('saveSupabaseBtn');
    if (saveBtn) {
        saveBtn.disabled = true;
        saveBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-1"></span> Saving...';
    }
    
    try {
        const fileInput = document.getElementById('csvFile');
        const fileName = (fileInput && fileInput.files[0]) ? fileInput.files[0].name : 'Transaction_Dataset.csv';
        
        const record = {
            dataset_name: fileName,
            algorithm: analysisResults.algorithm || document.getElementById('algorithm').value,
            min_support: parseFloat(document.getElementById('minSupport').value),
            min_confidence: parseFloat(document.getElementById('minConfidence').value),
            min_lift: parseFloat(document.getElementById('minLift').value),
            total_rules: analysisResults.rules ? analysisResults.rules.length : 0,
            total_items: analysisResults.frequent_items ? analysisResults.frequent_items.length : 0,
            total_transactions: analysisResults.analysis_info ? analysisResults.analysis_info.total_transactions : 0,
            results: analysisResults
        };
        
        let savedToCloud = false;
        
        if (supabaseClient) {
            try {
                const { data, error } = await supabaseClient
                    .from('market_basket_analyses')
                    .insert([record])
                    .select();
                    
                if (!error) {
                    savedToCloud = true;
                } else {
                    console.warn('Supabase DB notice:', error.message);
                }
            } catch (sbErr) {
                console.warn('Supabase request error:', sbErr);
            }
        }
        
        // Always maintain local copy
        saveToLocalBackup(record);
        
        if (savedToCloud) {
            showAlert('☁️ Analysis successfully saved to Supabase Cloud!', 'success');
        } else {
            showAlert('💾 Analysis saved to your History! (To sync to Supabase table, run supabase_schema.sql in Supabase SQL editor)', 'info');
        }
    } catch (err) {
        console.error('Save error:', err);
        showAlert(`❌ Failed to save: ${err.message}`, 'danger');
    } finally {
        if (saveBtn) {
            saveBtn.disabled = false;
            saveBtn.innerHTML = '<i class="fas fa-cloud-arrow-up me-1"></i>Save to Cloud';
        }
    }
}

// Open and Load Cloud History Modal
async function openHistoryModal() {
    const modalEl = document.getElementById('historyModal');
    if (!modalEl) return;
    
    const modal = new bootstrap.Modal(modalEl);
    modal.show();
    
    const loadingEl = document.getElementById('historyLoading');
    const listContainer = document.getElementById('historyListContainer');
    const emptyEl = document.getElementById('historyEmpty');
    const tbody = document.getElementById('historyTableBody');
    
    if (loadingEl) loadingEl.classList.remove('d-none');
    if (listContainer) listContainer.classList.add('d-none');
    if (emptyEl) emptyEl.classList.add('d-none');
    if (tbody) tbody.innerHTML = '';
    
    let records = [];
    
    if (supabaseClient) {
        try {
            const { data, error } = await supabaseClient
                .from('market_basket_analyses')
                .select('*')
                .order('created_at', { ascending: false })
                .limit(25);
                
            if (!error && data && data.length > 0) {
                records = data;
            }
        } catch (e) {
            console.warn('Could not fetch from Supabase:', e);
        }
    }
    
    // Fallback to local records if cloud is empty or uninitialized
    if (records.length === 0) {
        const local = getLocalBackup();
        if (local && local.length > 0) {
            records = local;
        }
    }
    
    if (loadingEl) loadingEl.classList.add('d-none');
    
    if (records.length === 0) {
        if (emptyEl) emptyEl.classList.remove('d-none');
        return;
    }
    
    if (listContainer) listContainer.classList.remove('d-none');
    window._cachedHistory = records;
    
    records.forEach((rec, idx) => {
        const row = tbody.insertRow();
        const dateStr = rec.created_at ? new Date(rec.created_at).toLocaleString() : 'Recently';
        row.innerHTML = `
            <td>
                <i class="fas fa-file-csv text-primary me-1"></i>
                <span class="fw-semibold">${escapeHtml(rec.dataset_name || 'Dataset')}</span>
            </td>
            <td><span class="badge bg-secondary">${escapeHtml(rec.algorithm || 'Apriori')}</span></td>
            <td><span class="badge bg-success">${rec.total_rules || (rec.results && rec.results.rules ? rec.results.rules.length : 0)} rules</span></td>
            <td class="small text-muted">${dateStr}</td>
            <td>
                <button type="button" class="btn btn-sm btn-primary" onclick="loadSavedAnalysis(${idx})">
                    <i class="fas fa-arrow-rotate-right me-1"></i> Load
                </button>
            </td>
        `;
    });
}

// Load a specific historical analysis
function loadSavedAnalysis(index) {
    if (!window._cachedHistory || !window._cachedHistory[index]) return;
    const record = window._cachedHistory[index];
    const results = record.results;
    if (!results) return;
    
    analysisResults = results;
    crossSellingData = results.cross_selling_data || {};
    
    displayResults(results);
    setupCrossSellingInterface();
    
    // Sync parameter fields if available
    if (record.min_support) document.getElementById('minSupport').value = record.min_support;
    if (record.min_confidence) document.getElementById('minConfidence').value = record.min_confidence;
    if (record.min_lift) document.getElementById('minLift').value = record.min_lift;
    if (record.algorithm) document.getElementById('algorithm').value = record.algorithm;
    
    downloadBtn.classList.remove('d-none');
    if (saveSupabaseBtn) saveSupabaseBtn.classList.remove('d-none');
    
    const modalEl = document.getElementById('historyModal');
    const modalInstance = bootstrap.Modal.getInstance(modalEl);
    if (modalInstance) modalInstance.hide();
    
    showAlert(`✅ Loaded analysis for "${escapeHtml(record.dataset_name)}" (${record.total_rules || results.rules.length} rules, ${record.algorithm || results.algorithm})`, 'success');
}

// Initialize tooltips
document.addEventListener('DOMContentLoaded', function() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});