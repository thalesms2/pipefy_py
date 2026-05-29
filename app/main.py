from fastapi import FastAPI

from app.routers import clientes, webhook

app = FastAPI(title="Mundo Invest API", version="1.0.0")

app.include_router(clientes.router)
app.include_router(webhook.router)


@app.get("/health")
async def health():
    return {"status": "ok"}
