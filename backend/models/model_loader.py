from models.hexacoin import HexacoinModel
from models.antimatter import AntimatterModel
from models.alphacoin import AlphacoinModel
from models.dianastone import DianastoneModel
from models.radiant import RadiantModel
from models.titanfusion import TitanFusionModel

def load_model(model_name: str):
    if model_name == "hexacoin":
        return HexacoinModel()
    elif model_name == "antimatter":
        return AntimatterModel()
    elif model_name == "alphacoin":
        return AlphacoinModel()
    elif model_name == "dianastone":
        return DianastoneModel()
    elif model_name == "radiant":
        return RadiantModel()
    elif model_name == "titanfusion":
        return TitanFusionModel()
    else:
        raise ValueError(f"Unknown model name: {model_name}")
