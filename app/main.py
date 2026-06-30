import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from app.database.db import Base, engine
from app.routes.url_routes import router

Base.metadata.create_all(bind=engine)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

app = FastAPI(title="URL Shortener", docs_url=None)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/")
def root():
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))

@app.get("/docs", include_in_schema=False)
def custom_docs():
    docs_path = os.path.join(STATIC_DIR, "docs.html")
    html = open(docs_path, encoding="utf-8").read()
    return HTMLResponse(html)

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(router)