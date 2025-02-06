
from flask import Flask, render_template
import os
from src.pdf_processor import PDFProcessor
from dotenv import load_dotenv

app = Flask(__name__)

@app.route('/')
def index():
    load_dotenv()
    processor = PDFProcessor()
    
    current_pdf = "data/brkdata/earnings_2022.pdf"
    previous_pdf = "data/brkdata/earnings_2023.pdf"

    # Process reports
    current_chunks = processor.load_pdf(current_pdf)
    current_metrics = processor.extract_financials(current_chunks)
    
    previous_chunks = processor.load_pdf(previous_pdf)
    previous_metrics = processor.extract_financials(previous_chunks)
    
    # Compare reports
    comparison = processor.compare_reports(current_metrics, previous_metrics)
    return comparison.to_html()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000)
