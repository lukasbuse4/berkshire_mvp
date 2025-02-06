
import os
from src.pdf_processor import PDFProcessor
from dotenv import load_dotenv

def main():
    load_dotenv()
    
    processor = PDFProcessor()
    
    # Example usage
    current_pdf = "data/earnings_2024.pdf"
    previous_pdf = "data/earnings_2023.pdf"
    
    # Process current report
    current_chunks = processor.load_pdf(current_pdf)
    current_metrics = processor.extract_financials(current_chunks)
    
    # Process previous report
    previous_chunks = processor.load_pdf(previous_pdf)
    previous_metrics = processor.extract_financials(previous_chunks)
    
    # Compare reports
    comparison = processor.compare_reports(current_metrics, previous_metrics)
    print("\nYear-over-Year Comparison:")
    print(comparison)

if __name__ == "__main__":
    main()
