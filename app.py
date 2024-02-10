from flask import Flask, render_template, request, jsonify
import backend.util as util

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route('/get_dashboard_stats', methods=['GET'])
def get_dashboard_stats():
    response = jsonify({
        'stats': util.get_dashboard_stats()
    })
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    # app.run(debug=True)