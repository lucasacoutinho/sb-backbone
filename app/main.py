from fastapi import FastAPI

from app.routes.book import router as book_router

app = FastAPI()

# Include routers
app.include_router(book_router)  # /book


@app.get("/health-check")
async def root():
    return {"message": "OK"}
