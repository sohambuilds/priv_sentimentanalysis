# main.py
import logging
from sentiment_analyzer import SentimentAnalyzer
from privacy_utils import PrivacyPreserver
from app import create_app

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    logger.info("Initializing Privacy-Preserving Sentiment Analyzer")
    analyzer = SentimentAnalyzer()
    privacy_preserver = PrivacyPreserver()
    
    app = create_app(analyzer, privacy_preserver)
    logger.info("Starting the Flask application")
    app.run(debug=True)

if __name__ == "__main__":
    main()
