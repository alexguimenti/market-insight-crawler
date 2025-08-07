from flask import Flask, render_template, request, jsonify, Response, stream_template
import os
import sys
from dotenv import load_dotenv
import threading
import queue
import time
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import functions from script.py
from script import WebScraper, get_relevant_links_from_url, get_full_content_from_site, summarize_company_from_site

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Production settings
REQUEST_TIMEOUT = 300  # 5 minutes total timeout
ANALYSIS_TIMEOUT = 240  # 4 minutes for analysis

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
    logger.info(f"Received analysis request for URL: {url}")

    if not url:
        logger.warning("URL is missing in request")
        return jsonify({'error': 'URL is required'}), 400

    # Validate URL
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url

    try:
        from io import StringIO
        import sys
        import signal

        # Set up timeout handler
        def timeout_handler(signum, frame):
            raise TimeoutError("Analysis timed out")

        # Set timeout for the entire analysis
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(ANALYSIS_TIMEOUT)

        old_stdout = sys.stdout
        sys.stdout = mystdout = StringIO()

        try:
            logger.info("Starting analysis...")
            summarize_company_from_site(url)
            logger.info("Analysis completed successfully")
        except TimeoutError:
            logger.error("Analysis timed out")
            return jsonify({'error': 'Analysis timed out. The website might be too large or slow to analyze.'}), 408
        except Exception as e:
            logger.error(f"Error during analysis: {str(e)}")
            return jsonify({'error': f'Analysis failed: {str(e)}'}), 500
        finally:
            sys.stdout = old_stdout
            signal.alarm(0)  # Cancel timeout

        output = mystdout.getvalue()
        logger.info(f"Analysis output length: {len(output)} characters")

        if not output.strip():
            return jsonify({'error': 'No analysis output generated. Please try a different URL.'}), 500

        return jsonify({'result': output})

    except Exception as e:
        logger.exception("Unexpected error in analyze_stream:")
        return jsonify({'error': f'Server error: {str(e)}'}), 500

if __name__ == '__main__':
    # Production settings
    app.run(
        debug=False,  # Disable debug in production
        host='0.0.0.0', 
        port=5000,
        threaded=True,  # Enable threading for concurrent requests
        # Add timeout settings for production
        request_timeout=REQUEST_TIMEOUT
    ) 