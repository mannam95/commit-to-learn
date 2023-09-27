from flask import Flask, request, jsonify
import backend.util as util

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello World!"


@app.route('/get_translated_text', methods=['POST'])
def get_translated_text():
    response = jsonify({
        'trans_text': util.get_translated_text(request)
    })
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response

if __name__ == '__main__':
    print("Starting Python Flask Server For Text Detection and Translation...")
    app.run(debug=True, host='0.0.0.0', port=80)