# backend/app/models/model_registry.py

from app.models.alphacoin import AlphacoinModel
from app.models.antimatter import AntimatterModel
from app.models.hexacoin import HexacoinModel
from app.models.dianastone import DianastoneModel
from app.models.radiant import RadiantModel
from app.models.cryptanium import CryptaniumModel
from app.models.cryptomite import CryptomiteModel
from app.models.einsteinium import EinsteiniumModel
from app.models.titanfusion import TitanFusionModel
from app.models.sophiaprimex import SophiaPrimeXModel
from app.models.californium import CaliforniumModel

class ModelRegistry:
    def __init__(self):
        self.registry = {
           # 'Alphacoin': {'type': 'crypto', 'instance': AlphacoinModel(), 'performance': {}},
            'Antimatter': {'type': 'crypto', 'instance': AntimatterModel(), 'performance': {}},
            'Hexacoin': {'type': 'crypto', 'instance': HexacoinModel(), 'performance': {}},
            'Radiant': {'type': 'crypto', 'instance': RadiantModel(), 'performance': {}},
            'Cryptanium': {'type': 'crypto', 'instance': CryptaniumModel(), 'performance': {}},
            'Cryptomite': {'type': 'crypto', 'instance': CryptomiteModel(), 'performance': {}},
            'Einsteinium': {'type': 'stock', 'instance': EinsteiniumModel(), 'performance': {}},
            'Dianastone': {'type': 'stock', 'instance': DianastoneModel(), 'performance': {}},
            'TitanFusion': {'type': 'stock', 'instance': TitanFusionModel(), 'performance': {}},
            'SophiaPrimeX': {'type': 'stock', 'instance': SophiaPrimeXModel(), 'performance': {}},
            'Californium': {'type': 'stock', 'instance': CaliforniumModel(), 'performance': {}},
        }

    def get_model(self, model_name):
        entry = self.registry.get(model_name)
        return entry['instance'] if entry else None

    def list_models(self, model_type=None):
        if model_type:
            return [name for name, meta in self.registry.items() if meta['type'] == model_type]
        return list(self.registry.keys())

    def log_trade(self, model_name, result, confidence):
        if model_name not in self.registry:
            return
        perf = self.registry[model_name].setdefault('performance', {'trades': 0, 'wins': 0, 'confidence_scores': []})
        perf['trades'] += 1
        if result:
            perf['wins'] += 1
        perf['confidence_scores'].append(confidence)
        perf['win_rate'] = perf['wins'] / perf['trades']
        perf['avg_confidence'] = sum(perf['confidence_scores']) / len(perf['confidence_scores'])

    def get_model_stats(self, model_name):
        return self.registry.get(model_name, {}).get('performance', {})

    def get_default_model(self, asset_class: str):
        if asset_class == 'crypto':
            return self.get_model('Antimatter')
        elif asset_class == 'stock':
            return self.get_model('Dianastone')
        return None

_model_registry = ModelRegistry()
get_default_model = _model_registry.get_default_model
