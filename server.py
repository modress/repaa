from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import os

app = FastAPI()

# Разрешаем запросы с любых сайтов (чтобы GitHub Pages свободно общался с бэкендом)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

REVIEWS_FILE = "reviews.json"

class Review(BaseModel):
    text: str
    rating: int = 5
    image: str = None

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
        json.dump(reviews, f, ensure_ascii=False, indent=4)

@app.get("/api/reviews")
def get_reviews():
    return {"reviews": load_reviews()}

@app.post("/api/reviews")
def add_review(review: Review):
    reviews = load_reviews()
    new_review = {
        "text": review.text,
        "rating": review.rating,
        "image": review.image
    }
    reviews.insert(0, new_review) # Добавляем новый отзыв в самый верх
    save_reviews(reviews)
    return {"status": "success", "reviews": reviews}
