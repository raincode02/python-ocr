import uvicorn

# FastAPI 앱 실행
if __name__ == "__main__":
    uvicorn.run("controller.api:app", host="0.0.0.0", port=8000, reload=True)
