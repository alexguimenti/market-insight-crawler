from flask import Flask, render_template, request, jsonify, Response, stream_template
import os
import sys
from dotenv import load_dotenv
import threading
import queue
import time
import json

# Import functions from script.py
from script import WebScraper, get_relevant_links_from_url, get_full_content_from_site, summarize_company_from_site

# Load environment variables
load_dotenv()

app = Flask(__name__)

# LLM provider configuration
LLM_PROVIDER = 'gemini'  # or 'openai'

# Queue for communication between threads
result_queue = queue.Queue()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    url = request.json.get('url')
    if not url:
        return jsonify({'error': 'URL is required'}), 400
    
    # Validate URL
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    def generate_analysis():
        try:
            # Replace TARGET_URL dynamically
            import script
            script.TARGET_URL = url
            
            # Generate analysis
            summarize_company_from_site(url)
            
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
    
    return Response(generate_analysis(), mimetype='text/event-stream')

@app.route('/analyze_stream', methods=['POST'])
def analyze_stream():
    url = request.json.get('url')
    if not url:
        return jsonify({'error': 'URL is required'}), 400
    
    # Validate URL
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    def generate():
        try:
            # Capture output from summarize_company_from_site
            import io
            import sys
            
            # Capture stdout
            old_stdout = sys.stdout
            sys.stdout = io.StringIO()
            
            try:
                summarize_company_from_site(url)
                output = sys.stdout.getvalue()
            finally:
                sys.stdout = old_stdout
            
            # Send result
            yield f"data: {json.dumps({'result': output})}\n\n"
            
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
    
    return Response(generate(), mimetype='text/event-stream')

#if __name__ == '__main__':
#    app.run(debug=True, host='0.0.0.0', port=5000) 