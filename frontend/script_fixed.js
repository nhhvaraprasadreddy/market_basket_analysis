// Global variables
let analysisResults = null;
let frequentItemsChart = null;

// API configuration
const API_CONFIG = {
    BASE_URL: 'http://127.0.0.1:8000',
    ENDPOINTS: {
        ANALYZE: '/api/analyze',
        HEALTH: '/health'
    }
};
const API_ENDPOINT = `${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.ANALYZE}`;

// DOM elements
const form = document.getElementById('analysisForm');
const analyzeText = document.getElementById('analyzeText');
const loadingSpinner = document.getElementById('loadingSpinner');
const downloadBtn = document.getElementById('downloadBtn');
const alertContainer = document.getElementById('alertContainer');

// Event listeners
form.addEventListener('submit', handleFormSubmit);
downloadBtn.addEventListener('click', downloadResults);
window.addEventListener('load', testBackendConnection);

async function testBackendConnection() {
    try {
        const response = await fetch(`${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.HEALTH}`);
        if (response.ok) {
            console.log('✅ Backend connection successful');
        }
    } catch (error) {
        console.error('❌ Backend connection failed:', error.message);
        showAlert('⚠️ Backend server not reachable. Please start the backend server.', 'warning');
    }
}

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
        
        const response = await fetch(API_ENDPOINT, {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        analysisResults = await response.json();
        console.log('✅ Analysis results received:', analysisResults);
        
        // Debug the exact structure
        console.log('frequent_items:', analysisResults.frequent_items);
        console.log('rules:', analysisResults.rules);
        
        displayResults(analysisResults);
        
        const rulesCount = analysisResults.rules.length;
        const itemsCount = analysisResults.frequent_items.length;
        
        let message = `✅ Analysis completed using ${analysisResults.algorithm}! Found ${rulesCount} association rules and ${itemsCount} frequent items.`;
        
        if (analysisResults.analysis_info) {
            const info = analysisResults.analysis_info;
            message += ` Dataset: ${info.total_transactions} transactions, ${info.total_items} unique items.`;
        }
        
        showAlert(message, rulesCount > 0 ? 'success' : 'warning');
        downloadBtn.classList.remove('d-none');
        
    } catch (error) {
        console.error('Error:', error);
        showAlert(`❌ ${error.message}`, 'danger');
    } finally {
        setLoading(false);
    }
}

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

function showAlert(message, type) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.setAttribute('role', 'alert');
    alertDiv.textContent = message;
    
    const closeBtn = document.createElement('button');
    closeBtn.type = 'button';
    closeBtn.className = 'btn-close';
    closeBtn.setAttribute('data-bs-dismiss', 'alert');
    
    alertDiv.appendChild(closeBtn);
    alertContainer.innerHTML = '';
    alertContainer.appendChild(alertDiv);
}

function clearResults() {
    const tbody = document.querySelector('#rulesTable tbody');
    if (tbody) tbody.innerHTML = '';
    
    if (frequentItemsChart) {
        frequentItemsChart.destroy();
        frequentItemsChart = null;
    }
    
    d3.select('#networkGraph').selectAll('*').remove();
    downloadBtn.classList.add('d-none');
}

function displayResults(results) {
    console.log('🎯 Displaying results:', results);
    
    // Display all components
    displayRulesTable(results.rules);
    drawFrequentItemsChart(results.frequent_items);
    drawNetworkGraph(results.rules);
}

function displayRulesTable(rules) {
    const tbody = document.querySelector('#rulesTable tbody');
    tbody.innerHTML = '';
    
    if (!rules || rules.length === 0) {
        const row = tbody.insertRow();
        const cell = row.insertCell();
        cell.colSpan = 5;
        cell.className = 'text-center text-muted py-4';
        cell.innerHTML = '<em>No association rules found.</em>';
        return;
    }
    
    rules.slice(0, 100).forEach(rule => {
        const row = tbody.insertRow();
        row.insertCell().textContent = rule.antecedent.join(', ');
        row.insertCell().textContent = rule.consequent.join(', ');
        row.insertCell().textContent = rule.support.toFixed(4);
        row.insertCell().textContent = rule.confidence.toFixed(4);
        row.insertCell().textContent = rule.lift.toFixed(4);
    });
}

function drawFrequentItemsChart(frequent_items) {
    console.log('📊 Drawing frequent items chart:', frequent_items);
    
    const ctx = document.getElementById('frequentItemsChart');
    if (!ctx) {
        console.error('❌ Canvas element not found');
        return;
    }
    
    if (frequentItemsChart) {
        frequentItemsChart.destroy();
    }
    
    if (!frequent_items || frequent_items.length === 0) {
        console.warn('⚠️ No frequent items data');
        return;
    }
    
    // Extract data for chart
    const labels = frequent_items.map(item => item.item);
    const data = frequent_items.map(item => item.frequency);
    
    console.log('📊 Chart labels:', labels);
    console.log('📊 Chart data:', data);
    
    frequentItemsChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Frequency',
                data: data,
                backgroundColor: 'rgba(13, 110, 253, 0.8)',
                borderColor: 'rgba(13, 110, 253, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true
                }
            },
            plugins: {
                legend: {
                    display: false
                }
            }
        }
    });
    
    console.log('✅ Chart created successfully');
}

function drawNetworkGraph(rules) {
    console.log('🔗 Drawing network graph with rules:', rules.length);
    
    const container = d3.select('#networkGraph');
    container.selectAll('*').remove();
    
    if (!rules || rules.length === 0) {
        container.append('div')
            .style('text-align', 'center')
            .style('padding', '50px')
            .style('color', '#6c757d')
            .html('<em>No item relationships to display</em>');
        return;
    }
    
    const width = 400;
    const height = 300;
    
    const svg = container.append('svg')
        .attr('width', width)
        .attr('height', height);
    
    // Create nodes and links from rules (limit to top 20 rules for performance)
    const nodes = new Map();
    const links = [];
    
    rules.slice(0, 20).forEach(rule => {
        // Add antecedent items as nodes
        rule.antecedent.forEach(item => {
            if (!nodes.has(item)) {
                nodes.set(item, { id: item, group: 1 });
            }
        });
        
        // Add consequent items as nodes
        rule.consequent.forEach(item => {
            if (!nodes.has(item)) {
                nodes.set(item, { id: item, group: 2 });
            }
        });
        
        // Create links between antecedent and consequent items
        rule.antecedent.forEach(ant => {
            rule.consequent.forEach(cons => {
                links.push({
                    source: ant,
                    target: cons,
                    value: rule.lift,
                    support: rule.support,
                    confidence: rule.confidence
                });
            });
        });
    });
    
    const nodeArray = Array.from(nodes.values());
    console.log('🔗 Nodes:', nodeArray.length, 'Links:', links.length);
    
    // Create force simulation
    const simulation = d3.forceSimulation(nodeArray)
        .force('link', d3.forceLink(links).id(d => d.id).distance(80))
        .force('charge', d3.forceManyBody().strength(-300))
        .force('center', d3.forceCenter(width / 2, height / 2));
    
    // Create links
    const link = svg.append('g')
        .selectAll('line')
        .data(links)
        .enter().append('line')
        .attr('class', 'network-link')
        .attr('stroke', '#999')
        .attr('stroke-opacity', 0.6)
        .attr('stroke-width', d => Math.sqrt(d.value));
    
    // Create nodes
    const node = svg.append('g')
        .selectAll('circle')
        .data(nodeArray)
        .enter().append('circle')
        .attr('class', 'network-node')
        .attr('r', 12)
        .attr('fill', d => d.group === 1 ? '#0d6efd' : '#198754')
        .attr('stroke', '#fff')
        .attr('stroke-width', 2)
        .call(d3.drag()
            .on('start', dragstarted)
            .on('drag', dragged)
            .on('end', dragended));
    
    // Create text labels
    const text = svg.append('g')
        .selectAll('text')
        .data(nodeArray)
        .enter().append('text')
        .attr('class', 'network-text')
        .attr('text-anchor', 'middle')
        .attr('font-size', '10px')
        .attr('font-weight', '500')
        .attr('pointer-events', 'none')
        .text(d => d.id.length > 8 ? d.id.substring(0, 8) + '...' : d.id);
    
    // Update positions on tick
    simulation.on('tick', () => {
        link
            .attr('x1', d => d.source.x)
            .attr('y1', d => d.source.y)
            .attr('x2', d => d.target.x)
            .attr('y2', d => d.target.y);
        
        node
            .attr('cx', d => d.x)
            .attr('cy', d => d.y);
        
        text
            .attr('x', d => d.x)
            .attr('y', d => d.y + 4);
    });
    
    function dragstarted(event, d) {
        if (!event.active) simulation.alphaTarget(0.3).restart();
        d.fx = d.x;
        d.fy = d.y;
    }
    
    function dragged(event, d) {
        d.fx = event.x;
        d.fy = event.y;
    }
    
    function dragended(event, d) {
        if (!event.active) simulation.alphaTarget(0);
        d.fx = null;
        d.fy = null;
    }
    
    console.log('✅ Network graph created successfully');
}

function downloadResults() {
    if (!analysisResults) return;
    
    const csv = convertToCSV(analysisResults.rules);
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'mba_results.csv';
    a.click();
    window.URL.revokeObjectURL(url);
}

function convertToCSV(rules) {
    const headers = ['Antecedent', 'Consequent', 'Support', 'Confidence', 'Lift'];
    const rows = rules.map(rule => [
        rule.antecedent.join('; '),
        rule.consequent.join('; '),
        rule.support,
        rule.confidence,
        rule.lift
    ]);
    
    return [headers, ...rows].map(row => row.join(',')).join('\n');
}