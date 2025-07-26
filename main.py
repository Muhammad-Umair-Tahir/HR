# main.py
from fastapi import FastAPI
from router import router as hr_router

app = FastAPI()
app.include_router(hr_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
