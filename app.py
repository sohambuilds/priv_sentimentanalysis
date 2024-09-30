# app.py
from flask import Flask, request, render_template_string, jsonify
import logging

logger = logging.getLogger(__name__)

def create_app(analyzer, privacy_preserver):
    app = Flask(__name__)

    @app.route('/', methods=['GET', 'POST'])
    def index():
        if request.method == 'POST':
            text = request.form['text']
            privacy_method = request.form['privacy_method']
            
            # Original analysis
            original_sentiment, original_score = analyzer.analyze(text)
            
            # Privacy-preserved analysis
            preserved_text = privacy_preserver.apply_privacy(text, method=privacy_method)
            preserved_sentiment, preserved_score = analyzer.analyze(preserved_text)
            
            result = {
                'original': {'text': text, 'sentiment': original_sentiment, 'score': original_score},
                'preserved': {'text': preserved_text, 'sentiment': preserved_sentiment, 'score': preserved_score},
                'privacy_method': privacy_method
            }
            
            logger.info(f"Analysis completed. Original sentiment: {original_sentiment}, Preserved sentiment: {preserved_sentiment}")
            return jsonify(result)
        
        return render_template_string('''
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Privacy-Preserving Sentiment Analyzer</title>
                <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
                <style>
                    body { font-family: Arial, sans-serif; line-height: 1.6; padding: 20px; max-width: 800px; margin: 0 auto; }
                    h1 { color: #333; }
                    form { margin-bottom: 20px; }
                    textarea { width: 100%; height: 100px; }
                    .result { margin-top: 20px; border: 1px solid #ddd; padding: 10px; }
                    #comparisonChart { max-width: 500px; margin: 20px auto; }
                </style>
            </head>
            <body>
                <h1>Privacy-Preserving Sentiment Analyzer</h1>
                <form id="analysisForm">
                    <textarea name="text" placeholder="Enter text to analyze" required></textarea><br>
                    <select name="privacy_method">
                        <option value="token_dropping">Token Dropping</option>
                        <option value="differential_privacy">Differential Privacy</option>
                        <option value="combined">Combined</option>
                    </select>
                    <button type="submit">Analyze</button>
                </form>
                <div id="result" class="result"></div>
                <canvas id="comparisonChart"></canvas>
                <script>
                    document.getElementById('analysisForm').addEventListener('submit', async (e) => {
                        e.preventDefault();
                        const formData = new FormData(e.target);
                        const response = await fetch('/', { method: 'POST', body: formData });
                        const result = await response.json();
                        
                        document.getElementById('result').innerHTML = `
                            <h2>Results:</h2>
                            <h3>Original Text:</h3>
                            <p>${result.original.text}</p>
                            <p>Sentiment: ${result.original.sentiment} (Score: ${result.original.score.toFixed(2)})</p>
                            <h3>Privacy-Preserved Text (${result.privacy_method}):</h3>
                            <p>${result.preserved.text}</p>
                            <p>Sentiment: ${result.preserved.sentiment} (Score: ${result.preserved.score.toFixed(2)})</p>
                        `;
                        
                        new Chart(document.getElementById('comparisonChart'), {
                            type: 'bar',
                            data: {
                                labels: ['Original', 'Privacy-Preserved'],
                                datasets: [{
                                    label: 'Sentiment Score',
                                    data: [result.original.score, result.preserved.score],
                                    backgroundColor: ['rgba(75, 192, 192, 0.6)', 'rgba(255, 99, 132, 0.6)']
                                }]
                            },
                            options: {
                                scales: {
                                    y: {
                                        beginAtZero: true,
                                        max: 1
                                    }
                                }
                            }
                        });
                    });
                </script>
            </body>
            </html>
        ''')

    return app
