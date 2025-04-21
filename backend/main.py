from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, trading, dashboard, models
import uvicorn

app = FastAPI(title="Ultima Bot API", version="1.0")

# Middleware for CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(trading.router, prefix="/trade", tags=["Trading"])
app.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])
app.include_router(models.router, prefix="/models", tags=["Models"])

@app.get("/")
def root():
    return {"message": "Ultima Bot API is live."}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
