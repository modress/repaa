from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import os

app = FastAPI()

# Разрешаем запросы со всех доменов (чтобы Mini App мог свободно стучаться на сервер)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_FILE = "reviews.json"

class Review(BaseModel):
    name: str
    link: str
    photo: str = ""
    rating: int
    text: str
    image: str = ""

def load_reviews():
    if not os.path.exists(DB_FILE):
        return []
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def save_reviews(reviews):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(reviews, f, ensure_ascii=False, indent=4)

@app.get("/api/reviews")
def get_reviews():
    return load_reviews()

@app.post("/api/reviews")
def add_review(review: Review):
    reviews = load_reviews()
    # Добавляем новый отзыв в самое начало списка
    reviews.insert(0, review.dict())
    save_reviews(reviews)
    return {"status": "success", "reviews": reviews}

@app.delete("/api/reviews/{index}")
def delete_review(index: int, username: str):
    # Проверка прав администратора на бэкенде
    if username.lower() not in ["neleron", "neleronbot"]:
        raise HTTPException(status_code=403, detail="Доступ запрещен")
    
    reviews = load_reviews()
    if 0 <= index < len(reviews):
        reviews.pop(index)
        save_reviews(reviews)
        return {"status": "success", "reviews": reviews}
    raise HTTPException(status_code=404, detail="Отзыв не найден")

if __name__ == "__main__":
    import uvicorn
    # Запускаем сервер на порту 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)