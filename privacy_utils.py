# privacy_utils.py
import random
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
import logging
from collections import Counter
import re

logger = logging.getLogger(__name__)

class PrivacyPreserver:
    def __init__(self, epsilon=2.0, token_drop_rate=0.15, vocab_size=10000):
        self.epsilon = epsilon
        self.token_drop_rate = token_drop_rate
        self.vectorizer = CountVectorizer(max_features=vocab_size)
        logger.info(f"Initializing PrivacyPreserver with epsilon={epsilon}, token_drop_rate={token_drop_rate}")
        
        # List of sentiment-carrying words to preserve
        self.sentiment_words = set([
            'happy', 'sad', 'angry', 'excited', 'worried', 'relieved', 'anxious', 'hopeful',
            'stressed', 'comfortable', 'concerned', 'appreciated', 'fear', 'hope', 'optimism',
            'apprehension', 'challenging', 'positive', 'negative', 'good', 'bad', 'great', 'terrible'
        ])

    def apply_privacy(self, text, method='combined'):
        if method == 'token_dropping':
            return self._token_dropping(text)
        elif method == 'differential_privacy':
            return self._improved_differential_privacy(text)
        elif method == 'combined':
            text = self._token_dropping(text)
            return self._improved_differential_privacy(text)
        else:
            raise ValueError("Invalid privacy method")

    def _token_dropping(self, text):
        logger.info("Applying token dropping")
        words = text.split()
        preserved_words = [word for word in words if random.random() > self.token_drop_rate or word.lower() in self.sentiment_words]
        return ' '.join(preserved_words)

    def _improved_differential_privacy(self, text):
        logger.info("Applying improved differential privacy")
        sentences = re.split('(?<=[.!?]) +', text)
        preserved_sentences = []

        for sentence in sentences:
            words = sentence.split()
            word_counts = Counter(words)
            
            # Add Laplace noise to word counts, with less noise for sentiment words
            noisy_counts = {}
            for word, count in word_counts.items():
                if word.lower() in self.sentiment_words:
                    noisy_counts[word] = count + np.random.laplace(0, 0.5 / self.epsilon)
                else:
                    noisy_counts[word] = count + np.random.laplace(0, 1.0 / self.epsilon)
            
            # Ensure non-negative counts and round to integers
            noisy_counts = {word: max(0, int(round(count))) for word, count in noisy_counts.items()}
            
            # Reconstruct sentence with noisy word frequencies
            noisy_words = []
            for word in words:
                if noisy_counts[word] > 0:
                    noisy_words.append(word)
                    noisy_counts[word] -= 1
            
            preserved_sentences.append(' '.join(noisy_words))

        return ' '.join(preserved_sentences)

    def _anonymize_sensitive_info(self, text):
        # Simple regex patterns for sensitive information
        patterns = {
            'name': r'\b[A-Z][a-z]+ (?:[A-Z][a-z]+ )?[A-Z][a-z]+\b',
            'age': r'\b\d{1,2}(?:-year-old)?\b',
            'location': r'\b[A-Z][a-z]+ (?:[A-Z][a-z]+ )?(?:Street|Avenue|Road|Place)\b',
            'money': r'\$\d+(?:,\d{3})*(?:\.\d{2})?'
        }
        
        for info_type, pattern in patterns.items():
            text = re.sub(pattern, f'[{info_type.upper()}]', text)
        
        return text

    def apply_privacy(self, text, method='combined'):
        text = self._anonymize_sensitive_info(text)
        if method == 'token_dropping':
            return self._token_dropping(text)
        elif method == 'differential_privacy':
            return self._improved_differential_privacy(text)
        elif method == 'combined':
            text = self._token_dropping(text)
            return self._improved_differential_privacy(text)
        else:
            raise ValueError("Invalid privacy method")