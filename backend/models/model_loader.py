# backend/models/model_loader.py

from models.hexacoin import HexacoinModel
from models.antimatter import AntimatterModel
from models.alphlacoin_v4 import AlphlacoinV4Model
from models.dianastone import DianastoneModel
from models.radiant import RadiantModel
from models.titanfusion import TitanFusionModel

def load_model(model_name: str):
    if model_name == "hexacoin":
        return HexacoinModel()
    elif model_name == "antimatter":
        return AntimatterModel()
    elif model_name == "alphlacoin_v4":
        return AlphlacoinV4Model()
    elif model_name == "dianastone":
        return DianastoneModel()
    elif model_name == "radiant":
        return RadiantModel()
    elif model_name == "titanfusion":
        return TitanFusionModel()
    else:
        raise ValueError(f"Unknown model name: {model_name}")
