from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma  # Updated import
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
import pandas as pd
from typing import List, Dict
from langchain_huggingface import HuggingFaceEmbeddings


class PDFProcessor:

    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000,
                                                            chunk_overlap=100)
        # In your PDFProcessor class
        self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    def load_pdf(self, file_path: str) -> List[str]:
        """Load and split PDF into chunks"""
        loader = PyPDFLoader(file_path)
        pages = loader.load()
        return self.text_splitter.split_documents(pages)

    def extract_financials(self, chunks: List[str]) -> Dict:
        """Extract key financial metrics"""
        db = Chroma.from_documents(chunks, self.embeddings)

        # Query for key metrics
        metrics = {
            'revenue': self._query_metric(db, 'revenue or sales figures'),
            'net_income': self._query_metric(db, 'net income or profit'),
            'operating_cash_flow': self._query_metric(db, 'operating cash flow or cash from operations'),
            'retained_earnings': self._query_metric(db, 'retained earnings or accumulated earnings'),
            'risk_factors': self._query_metric(db, 'risk factors or material risks'),
            'guidance': self._query_metric(db, 'future guidance or outlook')
        }
        return metrics

    def _query_metric(self, db, query: str) -> str:
        results = db.similarity_search(query, k=2)
        return ' '.join([doc.page_content for doc in results])

    def compare_reports(self, current_metrics: Dict,
                        previous_metrics: Dict) -> pd.DataFrame:
        """Compare two financial reports"""
        comparison = pd.DataFrame({
            'Metric': list(current_metrics.keys()),
            'Current': list(current_metrics.values()),
            'Previous': list(previous_metrics.values())
        })
        return comparison
