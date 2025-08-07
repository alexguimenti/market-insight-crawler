from flask import Flask, render_template, request, jsonify, Response, stream_template
from flask_cors import CORS
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
CORS(app)  # Enable CORS for all routes

# Global error handler
@app.errorhandler(Exception)
def handle_exception(e):
    logger.exception("Unhandled exception:")
    return jsonify({'error': 'Internal server error'}), 500

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

@app.route('/test')
def test():
    return render_template('test_frontend.html')

@app.route('/health')
def health():
    """Health check endpoint for debugging"""
    import os
    return jsonify({
        'status': 'ok',
        'openai_key': 'set' if os.getenv('OPENAI_API_KEY') else 'missing',
        'gemini_key': 'set' if os.getenv('GEMINI_API_KEY') else 'missing',
        'llm_provider': LLM_PROVIDER
    })

@app.route('/test_simple')
def test_simple():
    """Simple test endpoint that doesn't require external APIs"""
    return jsonify({
        'status': 'ok',
        'message': 'Server is responding correctly',
        'timestamp': time.time()
    })

@app.route('/debug')
def debug():
    """Debug page for testing endpoints"""
    return render_template('debug.html')

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

    logger.info(f"Starting analysis for validated URL: {url}")
    
    # Add memory management
    import gc
    gc.collect()
    
    # Check available memory (simple check)
    try:
        import psutil
        memory = psutil.virtual_memory()
        if memory.percent > 90:
            logger.warning(f"High memory usage: {memory.percent}%")
            return jsonify({'error': 'Server is under high load. Please try again later.'}), 503
    except ImportError:
        # psutil not available, skip memory check
        pass

    try:
        from io import StringIO
        import sys
        import threading
        import time

        # Timeout implementation for Windows compatibility
        def run_with_timeout(func, timeout_seconds):
            result = [None]
            exception = [None]
            
            def target():
                try:
                    result[0] = func()
                except Exception as e:
                    exception[0] = e
            
            thread = threading.Thread(target=target)
            thread.daemon = True
            thread.start()
            thread.join(timeout_seconds)
            
            if thread.is_alive():
                # Thread is still running, timeout occurred
                raise TimeoutError("Analysis timed out")
            
            if exception[0]:
                raise exception[0]
            
            return result[0]

        old_stdout = sys.stdout
        sys.stdout = mystdout = StringIO()

        try:
            logger.info("Starting analysis...")
            
            def analysis_func():
                summarize_company_from_site(url)
                return True
            
            run_with_timeout(analysis_func, ANALYSIS_TIMEOUT)
            logger.info("Analysis completed successfully")
            
        except TimeoutError:
            logger.error("Analysis timed out")
            return jsonify({'error': 'Analysis timed out. The website might be too large or slow to analyze.'}), 408
        except Exception as e:
            logger.error(f"Error during analysis: {str(e)}")
            return jsonify({'error': f'Analysis failed: {str(e)}'}), 500
        finally:
            sys.stdout = old_stdout

        output = mystdout.getvalue()
        logger.info(f"Analysis output length: {len(output)} characters")

        if not output.strip():
            return jsonify({'error': 'No analysis output generated. Please try a different URL.'}), 500

        return jsonify({'result': output})

    except Exception as e:
        logger.exception("Unexpected error in analyze_stream:")
        return jsonify({'error': f'Server error: {str(e)}'}), 500

    except KeyboardInterrupt:
        logger.warning("Analysis interrupted by user")
        return jsonify({'error': 'Analysis was interrupted'}), 500

    except SystemExit:
        logger.warning("System exit requested")
        return jsonify({'error': 'System exit requested'}), 500

if __name__ == '__main__':
    # Production settings
    app.run(
        debug=False,  # Disable debug in production
        host='0.0.0.0', 
        port=5000,
        threaded=True  # Enable threading for concurrent requests
    ) 