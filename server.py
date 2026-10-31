import json
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uuid

app = FastAPI()

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
    except:
        return []

def save_reviews(reviews):
    with open(REVIEWS_FILE, "w", encoding="utf-8") as f:
        json.dump(reviews, f, ensure_ascii=False, indent=2)

class Review(BaseModel):
    name: str = "Клиент"
    text: str
    rating: int = 5
    image: str = None
    link: str = None
    photo: str = None

@app.get("/api/reviews")
@app.get("/reviews")
def get_reviews():
    return load_reviews()

@app.post("/api/reviews")
@app.post("/reviews")
def add_review(review: Review):
    reviews = load_reviews()
    new_review = {
        "id": str(uuid.uuid4()),
        "name": review.name,
        "text": review.text,
        "rating": review.rating,
        "image": review.image,
        "link": review.link,
        "photo": review.photo
    }
    reviews.append(new_review)
    save_reviews(reviews)
    return {"status": "success", "review": new_review}

@app.delete("/api/reviews/{review_id}")
@app.delete("/reviews/{review_id}")
def delete_review(review_id: str):
    reviews = load_reviews()
    updated_reviews = [r for r in reviews if r.get("id") != review_id]
    if len(updated_reviews) == len(reviews):
        raise HTTPException(status_code=404, detail="Отзыв не найден")
    save_reviews(updated_reviews)
    return {"status": "deleted"}
    
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("server:app", host="0.0.0.0", port=port)
