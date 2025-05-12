# backend/app/api/routes/models.py

from fastapi import APIRouter, HTTPException
from app.services.model_service import ModelService  

router = APIRouter()

@router.get("/models")
async def list_models():
    """
    List available trading models.
    """
    return ModelService.get_all_models()

@router.get("/models/{model_id}")
async def get_model_details(model_id: str):
    """
    Get details for a specific trading model.
    """
    model = ModelService.get_model_by_id(model_id)
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    return model

@router.post("/models/{model_id}/select")
async def select_model_for_broker(model_id: str, broker_id: str):
    """
    Pair a model with a broker for trading.
    """
    try:
        return ModelService.select_model_for_broker(model_id, broker_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
