from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Welcome to CI/CD Demo"}

@app.get("/health")
def health():
    return {"status": "Healthy"}