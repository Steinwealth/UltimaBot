from fastapi import APIRouter, HTTPException

router = APIRouter()

# Static model registry (can be upgraded to DB or dynamic loading)
MODEL_REGISTRY = [
    {"name": "alphacoin", "label": "Alphacoin", "type": "crypto", "mode": "Hard"},
    {"name": "antimatter", "label": "Antimatter", "type": "crypto", "mode": "Hard"},
    {"name": "hexacoin", "label": "Hexacoin", "type": "crypto", "mode": "Easy"},
    {"name": "dianastone", "label": "Dianastone", "type": "stock", "mode": "Easy"},
    {"name": "radiant", "label": "Radiant", "type": "stock", "mode": "Hard"},
    {"name": "titanfusion", "label": "TitanFusion", "type": "stock", "mode": "Hard"}
]

@router.get("/")
def list_models():
    return {"models": MODEL_REGISTRY}

@router.get("/{model_name}")
def get_model(model_name: str):
    model = next((m for m in MODEL_REGISTRY if m["name"] == model_name), None)
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    return model
