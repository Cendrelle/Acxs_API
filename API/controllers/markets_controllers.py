import pandas as pd
from flask import jsonify, request
from services import filter, download, treatment

def download_markets():
    try:
        download.download_files()
        return jsonify({"status": "success", "message": "Files downloaded."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
def filter_markets():
    try:
        result= filter.filter_files()
        return jsonify({"status": "success", "message": "Files processed.", "data": result})
    except Exception as e:
        return jsonify({"error": str(e), "message": "Erreur au niveau du serveur"}), 500

def get_upcoming_markets():
    pass

def get_past_markets():
    pass
