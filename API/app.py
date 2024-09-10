from flask import Flask, jsonify
from controllers import markets_controllers 
from services import treatment

app = Flask(__name__)

@app.route("/markets", methods = ['POST'])
def download_markets():
    return markets_controllers.download_markets()

@app.route("/filter_markets", methods = ['POST'])
def filter_markets():
    return markets_controllers.filter_markets()

@app.route("/past_markets", methods = ['GET'])
def get_past_markets():
    return markets_controllers.get_past_markets()

@app.route("/upcoming_markets", methods = ['GET'])
def get_upcoming_markets():
    return markets_controllers.get_upcoming_markets()

@app.route("/treat_markets", methods= ['GET'])
def treat_markets():
    try:
        treatment.traiter_fichier_excel_et_inserer_db()
        return jsonify({"status": "success", "message": "Files downloaded."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)