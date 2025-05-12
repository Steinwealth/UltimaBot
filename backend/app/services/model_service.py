# backend/app/services/model_service.py

import os
import json
from datetime import datetime
import logging

class ModelService:
    MODEL_DIR = "backend/app/models/joblib"
    PERFORMANCE_FILE = "backend/app/models/performance.json"

    @staticmethod
    def get_all_models():
        try:
            with open(ModelService.PERFORMANCE_FILE, 'r') as f:
                perf_data = json.load(f)
        except FileNotFoundError:
            logging.warning("[ModelService] performance.json not found.")
            perf_data = {}

        try:
            files = os.listdir(ModelService.MODEL_DIR)
            models = []
            for f in files:
                if f.endswith(".joblib"):
                    name = f.replace('.joblib', '')
                    perf = perf_data.get(name, {})
                    models.append({
                        "name": name,
                        "performance": perf.get("performance", 0.0),
                        "last_trained": perf.get("last_trained", "N/A")
                    })
            return sorted(models, key=lambda m: m["performance"], reverse=True)
        except FileNotFoundError:
            logging.error(f"[ModelService] Model directory not found: {ModelService.MODEL_DIR}")
            return []

    @staticmethod
    def get_model_by_id(model_id: str):
        try:
            with open(ModelService.PERFORMANCE_FILE, 'r') as f:
                perf_data = json.load(f)
            perf = perf_data.get(model_id, {})
            return {
                "name": model_id,
                "performance": perf.get("performance", 0.0),
                "last_trained": perf.get("last_trained", "N/A")
            }
        except Exception as e:
            logging.error(f"[ModelService] Error reading model info: {e}")
            return {
                "name": model_id,
                "performance": 0.0,
                "last_trained": "N/A"
            }

    @staticmethod
    def select_model_for_broker(model_id: str, broker_id: str):
        # In production, this would persist the pairing in a DB or memory map
        logging.info(f"[ModelService] Model {model_id} paired with broker {broker_id}")
        return {
            "status": "paired",
            "model": model_id,
            "broker": broker_id,
            "timestamp": datetime.utcnow().isoformat()
        }
