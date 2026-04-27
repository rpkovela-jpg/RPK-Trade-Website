// API Configuration
const API_BASE_URL = 'http://localhost:5001/api';

// Portfolio Management
let portfolio = {};
let transactionHistory = [];

// Initialize on page load
$(document).ready(function() {
    loadTrendingStocks();
    loadScreenerResults();
    loadPortfolio();
});

// ============ DASHBOARD FUNCTIONS ============

function loadTrendingStocks() {
    $.ajax({
        url: `${API_BASE_URL}/stock/trending`,
        method: 'GET',
        success: function(data) {
            let html = '';
            if (data.trending && data.trending.length > 0) {
                data.trending.forEach(stock => {
                    const signalClass = getSignalClass(stock.signal);
                    const signalBadge = getSignalBadge(stock.signal);
                    const changeColor = stock.daily_change >= 0 ? 'text-success' : 'text-danger';
                    const changeSign = stock.daily_change >= 0 ? '+' : '';
                    
                    html += `
                        <div class="col-md-4 mb-3">
                            <div class="trending-card">
                                <div class="trending-symbol">${stock.symbol}</div>
                                <div class="trending-price">$${stock.price.toFixed(2)}</div>
                                <div class="trending-change ${changeColor}">
                                    ${changeSign}${stock.daily_change.toFixed(2)}%
                                </div>
                                <div style="margin-top: 10px;">
                                    <span class="badge ${signalBadge}">${stock.signal}</span>
                                </div>
                            </div>
                        </div>
                    `;
                });
            } else {
                html = '<div class="col-12 text-center text-white">No data available</div>';
            }
            $('#trendingContainer').html(html);
        },
        error: function(error) {
            $('#trendingContainer').html('<div class="alert alert-danger">Error loading trending stocks</div>');
        }
    });
}

function loadScreenerResults() {
    $.ajax({
        url: `${API_BASE_URL}/stock/screener`,
        method: 'GET',
        success: function(data) {
            let html = '<div class="table-responsive"><table class="table screener-table">';
            html += '<thead><tr><th>Symbol</th><th>Price</th><th>Signal</th><th>Score</th><th>Momentum</th><th>RSI</th><th>10d Momentum</th></tr></thead><tbody>';
            
            if (data.screener_results && data.screener_results.length > 0) {
                data.screener_results.forEach(stock => {
                    const signalBadge = getSignalBadge(stock.signal);
                    html += `
                        <tr>
                            <td><strong>${stock.symbol}</strong></td>
                            <td>$${stock.price.toFixed(2)}</td>
                            <td><span class="badge ${signalBadge}">${stock.signal}</span></td>
                            <td>${stock.score}</td>
                            <td>${stock.momentum.toFixed(2)}</td>
                            <td>${stock.rsi ? stock.rsi.toFixed(2) : 'N/A'}</td>
                            <td>${stock.price_momentum_10d.toFixed(2)}%</td>
                        </tr>
                    `;
                });
            } else {
                html += '<tr><td colspan="7" class="text-center">No data available</td></tr>';
            }
            
            html += '</tbody></table></div>';
            $('#screenerContainer').html(html);
        },
        error: function(error) {
            $('#screenerContainer').html('<div class="alert alert-danger">Error loading screener results</div>');
        }
    });
}

// ============ STOCK ANALYZER FUNCTIONS ============

function analyzeStock() {
    const symbol = $('#stockSymbol').val().toUpperCase();
    const period = $('#analysisPeriod').val();
    
    if (!symbol) {
        alert('Please enter a stock symbol');
        return;
    }
    
    $.ajax({
        url: `${API_BASE_URL}/stock/analyze`,
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            symbol: symbol,
            period: period,
            interval: '1d'
        }),
        success: function(data) {
            displayAnalysisResults(data);
            $('#analysisResults').show();
        },
        error: function(error) {
            const errorMsg = error.responseJSON?.error || 'Error analyzing stock';
            alert('Error: ' + errorMsg);
        }
    });
}

function displayAnalysisResults(data) {
    $('#analyzeSymbol').text(`${data.symbol} Analysis`);
    
    // Update current stats
    $('#currentPrice').text(`$${data.current_price.toFixed(2)}`);
    $('#dailyChange').html(`<span class="${data.technical_indicators.rsi < 30 ? 'text-danger' : 'text-success'}">${data.technical_indicators.daily_change || 0}%</span>`);
    $('#signal').text(data.signal).removeClass().addClass(`signal-${data.signal.toLowerCase()}`);
    $('#momentum').text(`${data.momentum.rsi_momentum.toFixed(2)}`);
    
    // Update technical indicators
    $('#sma20').text(`$${data.technical_indicators.sma_20?.toFixed(2) || 'N/A'}`);
    $('#sma50').text(`$${data.technical_indicators.sma_50?.toFixed(2) || 'N/A'}`);
    $('#rsi').text(`${data.technical_indicators.rsi?.toFixed(2) || 'N/A'}`);
    $('#macd').text(`${data.technical_indicators.macd?.toFixed(4) || 'N/A'}`);
    $('#bbUpper').text(`$${data.technical_indicators.bollinger_upper?.toFixed(2) || 'N/A'}`);
    $('#bbLower').text(`$${data.technical_indicators.bollinger_lower?.toFixed(2) || 'N/A'}`);
    $('#atr').text(`$${data.technical_indicators.atr?.toFixed(2) || 'N/A'}`);
    $('#priceMotum').text(`${data.momentum.price_momentum_5d?.toFixed(2) || 'N/A'}%`);
    
    // Display signal details
    let signalHtml = '';
    const signals = data.signal_details.individual_scores;
    Object.entries(signals).forEach(([key, value]) => {
        const signalValue = value > 0 ? 'BUY' : value < 0 ? 'SELL' : 'NEUTRAL';
        const className = value > 0 ? 'buy' : value < 0 ? 'sell' : 'neutral';
        signalHtml += `
            <div class="col-md-6">
                <div class="signal-detail-box ${className}">
                    <strong>${key}</strong>
                    <p class="mb-0">${signalValue}</p>
                </div>
            </div>
        `;
    });
    $('#signalDetails').html(signalHtml);
    
    // Display stock info
    if (data.stock_info) {
        let infoHtml = '<div class="info-grid">';
        Object.entries(data.stock_info).forEach(([key, value]) => {
            if (key !== 'symbol') {
                const label = key.replace(/_/g, ' ').toUpperCase();
                infoHtml += `
                    <div class="info-item">
                        <div class="info-item-label">${label}</div>
                        <div class="info-item-value">${value || 'N/A'}</div>
                    </div>
                `;
            }
        });
        infoHtml += '</div>';
        $('#stockInfo').html(infoHtml);
    }
}

// ============ EXIT STRATEGY FUNCTIONS ============

function planExit() {
    const entryPrice = parseFloat($('#entryPrice').val());
    const currentPrice = parseFloat($('#currentExitPrice').val());
    const quantity = parseFloat($('#quantity').val());
    const capital = parseFloat($('#capital').val());
    
    if (entryPrice <= 0) {
        alert('Please enter a valid entry price');
        return;
    }
    
    $.ajax({
        url: `${API_BASE_URL}/stock/exit-plan`,
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            entry_price: entryPrice,
            current_price: currentPrice || entryPrice,
            quantity: quantity || 0,
            capital_allocated: capital || 0
        }),
        success: function(data) {
            displayExitPlan(data);
        },
        error: function(error) {
            alert('Error generating exit plan');
        }
    });
}

function displayExitPlan(data) {
    let html = '';
    
    // Current stats
    html += `
        <div class="mb-3">
            <h6>Current Position Stats</h6>
            <table class="table table-sm">
                <tr>
                    <td><strong>Entry Price:</strong></td>
                    <td>$${data.current_stats.entry_price.toFixed(2)}</td>
                </tr>
                <tr>
                    <td><strong>Current Price:</strong></td>
                    <td>$${data.current_stats.current_price.toFixed(2)}</td>
                </tr>
                <tr>
                    <td><strong>P/L:</strong></td>
                    <td class="${data.current_stats.profit_loss >= 0 ? 'text-success' : 'text-danger'}">
                        $${data.current_stats.profit_loss.toFixed(2)} (${data.current_stats.profit_loss_percent.toFixed(2)}%)
                    </td>
                </tr>
            </table>
        </div>
    `;
    
    // Exit points
    if (data.exit_points) {
        html += `
            <div class="mb-3">
                <h6>Exit Points & Targets</h6>
                <table class="table table-sm table-striped">
                    <thead>
                        <tr>
                            <th>Target</th>
                            <th>Price</th>
                            <th>Return</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><strong>Stop Loss</strong></td>
                            <td>$${data.exit_points.stop_loss.price.toFixed(2)}</td>
                            <td class="text-danger">${data.exit_points.stop_loss.loss_percent.toFixed(2)}%</td>
                        </tr>
        `;
        
        Object.entries(data.exit_points.take_profit_targets).forEach(([key, target]) => {
            html += `
                        <tr>
                            <td><strong>${key}</strong></td>
                            <td>$${target.price.toFixed(2)}</td>
                            <td class="text-success">+${target.return_percent.toFixed(2)}%</td>
                        </tr>
            `;
        });
        
        html += '</tbody></table></div>';
    }
    
    $('#exitPlanContent').html(html);
    $('#exitPlanResults').show();
    
    // Display pyramiding strategy
    if (data.pyramiding_strategy) {
        displayPyramidingStrategy(data.pyramiding_strategy);
    }
    
    // Display scaling out strategy
    if (data.scaling_out_strategy) {
        displayScalingOutStrategy(data.scaling_out_strategy);
    }
    
    // Display risk management
    if (data.risk_management) {
        displayRiskManagement(data.risk_management);
    }
}

function displayPyramidingStrategy(pyramiding) {
    let html = `
        <div class="mb-3">
            <h6>Strategy Overview</h6>
            <p class="small text-muted">Average Entry Price: <strong>$${pyramiding.average_entry_price.toFixed(2)}</strong></p>
            <p class="small text-muted">Total Quantity: <strong>${pyramiding.total_quantity.toFixed(2)}</strong></p>
        </div>
        <div class="table-responsive">
            <table class="table table-sm">
                <thead>
                    <tr>
                        <th>Tranche</th>
                        <th>Entry Price</th>
                        <th>Quantity</th>
                        <th>Capital</th>
                    </tr>
                </thead>
                <tbody>
    `;
    
    pyramiding.pyramiding_plan.forEach(tranche => {
        html += `
                    <tr>
                        <td>${tranche.tranche}</td>
                        <td>$${tranche.entry_price.toFixed(2)}</td>
                        <td>${tranche.quantity.toFixed(2)}</td>
                        <td>$${tranche.capital_allocated.toFixed(2)}</td>
                    </tr>
        `;
    });
    
    html += '</tbody></table></div>';
    
    $('#pyramidingDiv').show();
    $('#pyramidingContent').html(html);
}

function displayScalingOutStrategy(scaling) {
    let html = `
        <div class="mb-3">
            <h6>Scaling Plan</h6>
            <p class="small text-muted">Entry Price: <strong>$${scaling.entry_price.toFixed(2)}</strong></p>
            <p class="small text-muted">Total Quantity: <strong>${scaling.total_quantity.toFixed(2)}</strong></p>
        </div>
        <div class="table-responsive">
            <table class="table table-sm">
                <thead>
                    <tr>
                        <th>Target</th>
                        <th>Price</th>
                        <th>Qty Sell</th>
                        <th>Profit</th>
                    </tr>
                </thead>
                <tbody>
    `;
    
    scaling.scaling_plan.forEach(level => {
        html += `
                    <tr>
                        <td>${level.target}</td>
                        <td>$${level.target_price.toFixed(2)}</td>
                        <td>${level.quantity_to_sell.toFixed(2)}</td>
                        <td class="text-success">$${level.total_profit.toFixed(2)}</td>
                    </tr>
        `;
    });
    
    html += '</tbody></table></div>';
    
    $('#scalingDiv').show();
    $('#scalingContent').html(html);
}

function displayRiskManagement(riskMgmt) {
    console.log('Risk Management:', riskMgmt);
}

// ============ PORTFOLIO FUNCTIONS ============

function simulateBuy() {
    const symbol = $('#buySymbol').val().toUpperCase();
    const qty = parseFloat($('#buyQty').val());
    
    if (!symbol || qty <= 0) {
        alert('Please enter valid symbol and quantity');
        return;
    }
    
    // Get current price
    $.ajax({
        url: `${API_BASE_URL}/stock/analyze`,
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            symbol: symbol,
            period: '1d'
        }),
        success: function(data) {
            const price = data.current_price;
            const cost = price * qty;
            
            if (!portfolio[symbol]) {
                portfolio[symbol] = { qty: 0, avgPrice: 0 };
            }
            
            // Calculate new average price
            const totalCost = (portfolio[symbol].qty * portfolio[symbol].avgPrice) + cost;
            portfolio[symbol].qty += qty;
            portfolio[symbol].avgPrice = totalCost / portfolio[symbol].qty;
            
            // Record transaction
            transactionHistory.push({
                type: 'BUY',
                symbol: symbol,
                qty: qty,
                price: price,
                date: new Date().toLocaleDateString()
            });
            
            $('#buySymbol').val('');
            $('#buyQty').val('');
            
            alert(`Bought ${qty} shares of ${symbol} at $${price.toFixed(2)}`);
            loadPortfolio();
        },
        error: function() {
            alert('Error fetching stock price');
        }
    });
}

function simulateSell() {
    const symbol = $('#sellSymbol').val().toUpperCase();
    const qty = parseFloat($('#sellQty').val());
    
    if (!symbol || qty <= 0 || !portfolio[symbol] || portfolio[symbol].qty < qty) {
        alert('Invalid sell operation');
        return;
    }
    
    $.ajax({
        url: `${API_BASE_URL}/stock/analyze`,
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            symbol: symbol,
            period: '1d'
        }),
        success: function(data) {
            const price = data.current_price;
            const profit = (price - portfolio[symbol].avgPrice) * qty;
            
            portfolio[symbol].qty -= qty;
            if (portfolio[symbol].qty <= 0) {
                delete portfolio[symbol];
            }
            
            transactionHistory.push({
                type: 'SELL',
                symbol: symbol,
                qty: qty,
                price: price,
                profit: profit,
                date: new Date().toLocaleDateString()
            });
            
            $('#sellSymbol').val('');
            $('#sellQty').val('');
            
            alert(`Sold ${qty} shares of ${symbol} at $${price.toFixed(2)}\nProfit: $${profit.toFixed(2)}`);
            loadPortfolio();
        },
        error: function() {
            alert('Error fetching stock price');
        }
    });
}

function loadPortfolio() {
    let totalValue = 0;
    let totalCost = 0;
    let html = '<div class="table-responsive"><table class="table"><thead><tr><th>Symbol</th><th>Quantity</th><th>Avg Price</th><th>Current Value</th><th>P/L</th></tr></thead><tbody>';
    
    let hasHoldings = false;
    
    Object.entries(portfolio).forEach(([symbol, data]) => {
        hasHoldings = true;
        const cost = data.avgPrice * data.qty;
        totalCost += cost;
        
        // In a real app, we'd fetch current price
        const currentValue = cost; // Simplified
        totalValue += currentValue;
        const pl = currentValue - cost;
        const plPercent = (pl / cost) * 100;
        
        html += `
            <tr>
                <td><strong>${symbol}</strong></td>
                <td>${data.qty.toFixed(2)}</td>
                <td>$${data.avgPrice.toFixed(2)}</td>
                <td>$${currentValue.toFixed(2)}</td>
                <td class="${pl >= 0 ? 'text-success' : 'text-danger'}">
                    $${pl.toFixed(2)} (${plPercent.toFixed(2)}%)
                </td>
            </tr>
        `;
    });
    
    if (!hasHoldings) {
        html += '<tr><td colspan="5" class="text-center text-muted">No holdings yet</td></tr>';
    }
    
    html += '</tbody></table></div>';
    
    if (hasHoldings) {
        html += `<hr><div class="alert alert-info">
            <strong>Total Portfolio Value:</strong> $${totalValue.toFixed(2)}<br>
            <strong>Total Cost:</strong> $${totalCost.toFixed(2)}<br>
            <strong>Total P/L:</strong> $${(totalValue - totalCost).toFixed(2)}
        </div>`;
    }
    
    $('#portfolioTable').html(html);
}

// ============ UTILITY FUNCTIONS ============

function getSignalClass(signal) {
    const classes = {
        'STRONG_BUY': 'strong-buy',
        'BUY': 'buy',
        'WEAK_BUY': 'buy',
        'NEUTRAL': 'neutral',
        'WEAK_SELL': 'sell',
        'SELL': 'sell',
        'STRONG_SELL': 'strong-sell'
    };
    return classes[signal] || 'neutral';
}

function getSignalBadge(signal) {
    const badges = {
        'STRONG_BUY': 'badge-strong-buy',
        'BUY': 'badge-buy',
        'WEAK_BUY': 'badge-buy',
        'NEUTRAL': 'badge-neutral',
        'WEAK_SELL': 'badge-sell',
        'SELL': 'badge-sell',
        'STRONG_SELL': 'badge-strong-sell'
    };
    return badges[signal] || 'badge-neutral';
}
