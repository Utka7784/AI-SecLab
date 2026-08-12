from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def index():
    return {"name": "First Date"}


@app.get("/health")
def new_index():
    return {
            "status": "ok"
            }

