# sentiment_analyzer.py
from transformers import pipeline
import torch
import logging

logger = logging.getLogger(__name__)

class SentimentAnalyzer:
    def __init__(self, model_name='distilbert-base-uncased-finetuned-sst-2-english'):
        logger.info(f"Initializing SentimentAnalyzer with model: {model_name}")
        self.model = pipeline("sentiment-analysis", model=model_name, device=0 if torch.cuda.is_available() else -1)

    def analyze(self, text):
        logger.info("Performing sentiment analysis")
        result = self.model(text)[0]
        return result['label'], result['score']
