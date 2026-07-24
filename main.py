import uvicorn
from fastapi import FastAPI

from cities import router as cities_router

if __name__ == "__main__":
    app = FastAPI(root_path="/api/v1")
    app.include_router(cities_router.router)
    uvicorn.run(app, host="localhost", port=8000)
