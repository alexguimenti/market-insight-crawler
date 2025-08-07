from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return jsonify({'status': 'ok', 'message': 'Flask app is running'})

@app.route('/test_analyze', methods=['POST'])
def test_analyze():
    return jsonify({'result': 'Test analysis completed successfully'})

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000, threaded=True)
