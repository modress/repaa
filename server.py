from fastapi import Request

@app.post("/api/reviews")
@app.post("/reviews")
async def add_review(request: Request):
    try:
        body = await request.json()
    except:
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
