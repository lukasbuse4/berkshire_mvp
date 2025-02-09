from flask import Flask
import os
from src.pdf_processor import PDFProcessor
from dotenv import load_dotenv
import yfinance as yf

app = Flask(__name__)

def get_stock_data(symbol="BRK-B"):
    stock = yf.Ticker(symbol)
    current_price = stock.info['regularMarketPrice']
    previous_close = stock.info['previousClose']
    price_change = ((current_price - previous_close) / previous_close) * 100
    return current_price, price_change

@app.route('/')
def index():
    try:
        load_dotenv()
        processor = PDFProcessor()

        current_pdf = "data/brkdata/earnings_2022.pdf"
        previous_pdf = "data/brkdata/earnings_2023.pdf"

        # Check if files exist
        if not os.path.exists(current_pdf) or not os.path.exists(previous_pdf):
            return "Error: PDF files not found", 500

        current_chunks = processor.load_pdf(current_pdf)
        current_metrics = processor.extract_financials(current_chunks)

        previous_chunks = processor.load_pdf(previous_pdf)
        previous_metrics = processor.extract_financials(previous_chunks)

    stock_price, price_change = get_stock_data()
    except Exception as e:
        return f"Error: {str(e)}", 500

    def extract_value(text):
        import re
        numbers = re.findall(r'\$?\d+\.?\d*\s*[BMK]?illion?|\$?\d+\.?\d*', text)
        return float(numbers[0].replace('$', '').replace('B', '')) if numbers else 0

    metrics_data = {}
    for key in current_metrics.keys():
        current_val = extract_value(current_metrics[key])
        prev_val = extract_value(previous_metrics[key])
        change = ((current_val - prev_val) / prev_val * 100) if prev_val != 0 else 0
        metrics_data[key] = {
            'current': current_val,
            'change': change
        }

    return f"""
    <html>
        <head>
            <title>Berkshire Hathaway Dashboard</title>
            <meta http-equiv="refresh" content="300">
            <style>
                body {{ font-family: 'Segoe UI', sans-serif; margin: 0; padding: 20px; background: #f0f2f5; }}
                .container {{ max-width: 1200px; margin: 0 auto; }}
                .stock-card {{ 
                    background: #1a237e; 
                    color: white; 
                    padding: 20px; 
                    border-radius: 10px; 
                    margin-bottom: 20px;
                }}
                .stock-price {{ font-size: 32px; font-weight: bold; }}
                .metrics-grid {{ 
                    display: grid; 
                    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); 
                    gap: 20px; 
                }}
                .metric-card {{ 
                    background: white; 
                    padding: 20px; 
                    border-radius: 10px; 
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }}
                .metric-title {{ font-size: 16px; color: #666; margin: 0; }}
                .metric-value {{ font-size: 24px; font-weight: bold; color: #1a237e; margin: 10px 0; }}
                .change {{ font-weight: 500; }}
                .positive {{ color: #00c853; }}
                .negative {{ color: #ff1744; }}
                .inline-price {{ 
                    font-size: 24px;
                    color: #4caf50;
                    margin-left: 10px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="stock-card">
                    <h2>Berkshire Hathaway (BRK.B) <span class="inline-price">${stock_price:.2f}</span></h2>
                    <div class="change {price_change >= 0 and 'positive' or 'negative'}">
                        {price_change >= 0 and '↑' or '↓'} {abs(price_change):.2f}%
                    </div>
                </div>

                <div class="metrics-grid">
                    {"".join([f'''
                    <div class="metric-card">
                        <h3 class="metric-title">{key.replace('_', ' ').title()}</h3>
                        <div class="metric-value">${metrics_data[key]['current']}B</div>
                        <div class="change {metrics_data[key]['change'] >= 0 and 'positive' or 'negative'}">
                            {metrics_data[key]['change'] >= 0 and '↑' or '↓'} {abs(metrics_data[key]['change']):.1f}%
                        </div>
                    </div>
                    ''' for key in metrics_data])}
                </div>
            </div>
        </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000)