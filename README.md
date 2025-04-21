THis Readme is for the development of Ultima Bot.


ultima-bot/
├── backend/
│   ├── models/
│   │   ├── __init__.py
│   │   ├── model_config.json      # Stores metadata: names, types, defaults
│   │   ├── hexacoin.py            # Logic for Hexacoin model
│   │   ├── antimatter.py          # Logic for Antimatter model
│   │   ├── dianastone.py          # Logic for Dianastone model
│   │   ├── titanfusion.py         # Logic for TitanFusion model
│   │   ├── radiant.py             # Logic for Radiant model
│   │   └── model_loader.py        # Dynamically loads models from JSON/config
