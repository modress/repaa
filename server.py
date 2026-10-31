import os
import json
import uuid
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Настройка CORS, чтобы сайт с GitHub Pages мог свободно отправлять запросы
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

REVIEWS_FILE = "reviews.json"

def load_reviews():
    if not os.path.exists(REVIEWS_FILE):
        return []
    try:
        with open(REVIEWS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def save_reviews(reviews):
    with open(REVIEWS_FILE, "w", encoding="utf-8") as f:
        json.dump(reviews, f, ensure_ascii=False, indent=4)

@app.get("/api/reviews")
@app.get("/reviews")
async def get_reviews():
    return load_reviews()

@app.post("/api/reviews")
@app.post("/reviews")
async def add_review(request: Request):
    try:
        body = await request.json()
    except Exception:
        body = {}

    reviews = load_reviews()
    new_review = {
        "id": str(uuid.uuid4()),
        "name": body.get("name", "Клиент"),
        "text": body.get("text", ""),
        "rating": body.get("rating", 5),
        "image": body.get("image"),
        "link": body.get("link"),
        "photo": body.get("photo")
    }
    reviews.append(new_review)
    save_reviews(reviews)
    return {"status": "success", "review": new_review}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("server:app", host="0.0.0.0", port=port)
