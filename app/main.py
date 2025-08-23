import os
from fastAPI import FasatAPI
from fastapi.response import FileResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="Doc Q&A (Local)")

app.mount("/static", StaticFiles(directory="static"), name"static")

@app.get("/")
def root():
    return FileResponse("static/index.html")

