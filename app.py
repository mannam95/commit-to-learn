from flask import Flask, render_template, request, jsonify
import backend.util as util

app = Flask(__name__)


@app.route('/get_translated_text', methods=['GET'])
def get_translated_text():
    response = jsonify({
        'trans_text': util.get_translated_text()
    })
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    # app.run(debug=True)