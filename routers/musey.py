from fastapi import APIRouter, HTTPException, Body
from models import Museum, Comment, Rating, Ticket
from database import database, museum_collection, comment_collection, rating_collection, ticket_collection
from typing import Optional
from pymongo.collection import Collection

router = APIRouter()

@router.post("/museums/")
async def add_museum(museum: Museum):
    if museum_collection.find_one({"name": museum.name, "location": museum.location}):
        raise HTTPException(status_code=400, detail="Museum already exists")
    museum_collection.insert_one(museum.dict())
    return {"message": "Museum added successfully"}

@router.post("/museums/{museum_id}/comment/")
async def add_comment(museum_id: str, comment: Comment):
    if not museum_collection.find_one({"_id": museum_id}):
        raise HTTPException(status_code=404, detail="Museum not found")
    comment.museum_id = museum_id
    comment_collection.insert_one(comment.dict())
    return {"message": "Comment added successfully"}

@router.post("/museums/{museum_id}/rate/")
async def rate_museum(museum_id: str, rating: Rating):
    if not museum_collection.find_one({"_id": museum_id}):
        raise HTTPException(status_code=404, detail="Museum not found")
    rating.museum_id = museum_id
    rating_collection.insert_one(rating.dict())
    return {"message": "Rating added successfully"}

@router.get("/museums/search/")
async def search_museums(name: Optional[str] = None, location: Optional[str] = None, min_rating: Optional[float] = None):
    query = {}
    if name:
        query["name"] = {"$regex": f".*{name}.*", "$options": "i"}
    if location:
        query["location"] = {"$regex": f".*{location}.*", "$options": "i"}
    if min_rating:
        # This will need to be adjusted based on how ratings are stored and calculated
        pass
    museums = list(museum_collection.find(query))
    return museums

@router.post("/museums/{museum_id}/purchase_ticket/")
async def purchase_ticket(museum_id: str, ticket: Ticket):
    if not museum_collection.find_one({"_id": museum_id}):
        raise HTTPException(status_code=404, detail="Museum not found")
    ticket.museum_id = museum_id
    ticket_collection.insert_one(ticket.dict())
    return {"message": "Ticket purchased successfully"}
