/ultima-bot
├── /backend
│   ├── /routers
│   │   ├── place_order.py            # Route for placing trades
│   │   ├── websocket_marquee.py      # WebSocket route for broadcasting messages
│   │   └── (other routes...)
│   ├── /engines
│   │   ├── auto_close_engine.py      # Logic for closing trades (TP/SL)
│   │   ├── auto_close_scheduler.py  # Scheduler for monitoring open trades
│   │   ├── compounding_engine.py     # Logic for compounding trades based on streaks
│   │   ├── confidence_engine.py     # Confidence scoring system
│   │   ├── forecast_engine.py       # TP/SL prediction logic
│   │   ├── strategy_engine.py       # Strategy execution logic
│   │   └── risk_engine.py           # Risk management (position sizing, drawdown)
│   ├── /services
│   │   ├── broker_clients
│   │   │   ├── place_order.py       # Broker-specific order execution logic
│   │   │   ├── coinbase_place.py    # Coinbase order handling
│   │   │   ├── etrade_place.py      # E*TRADE order handling
│   │   │   └── (other brokers...)
│   ├── /utils
│   │   └── logger.py                # Logging utility for backend
│   ├── /models
│   │   ├── trade_model.py           # Data models for trades, brokers, etc.
│   │   └── (other models...)
│   └── main.py                      # FastAPI entry point (backend setup)
├── /frontend
│   ├── /components
│   │   ├── DashboardDarkFlip.jsx    # Dashboard for Dark theme (Flip functionality)
│   │   ├── DashboardLightFlip.jsx   # Dashboard for Light theme (Flip functionality)
│   │   ├── MarqueeBar.jsx           # Scrolling Marquee component
│   │   ├── TradeStatusCard.jsx      # Displays live trade data (TP/SL tracking)
│   │   └── (other components...)
│   ├── /context
│   │   └── ThemeProvider.js         # Manages theme state (Light/Dark)
│   ├── /hooks
│   │   ├── useTradePanels.js       # Hook for managing trade panels (Open/History)
│   │   ├── useBrokers.js           # Hook for managing brokers (login, info)
│   │   ├── useToasts.js            # Toasts and Marquee message handling
│   │   └── useLiveTradeDisplay.js  # Handles real-time price and confidence updates
│   ├── /services
│   │   ├── submitTrade.js           # Function for submitting trades (frontend)
│   │   └── (other services...)
│   ├── /assets
│   │   ├── /images
│   │   └── /icons
│   ├── App.js                       # Main app component (Frontend setup)
│   └── index.js                     # React entry point
├── .env                             # Environment variables (API keys, secrets, etc.)
├── requirements.txt                 # Backend dependencies
├── package.json                     # Frontend dependencies and scripts
└── README.md                        # Project documentation
