from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "ИС Расписание работает"}

@app.get("/health")
def health():
    return {"status": "ok"}
