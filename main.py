# main.py
from fastapi import FastAPI
from router import router as hr_router

app = FastAPI()
app.include_router(hr_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
