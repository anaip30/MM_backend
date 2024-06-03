from fastapi import APIRouter, HTTPException, Body, Query
from models import Museum, Comment, Rating, Ticket, Rating
from database import database, museum_collection, comment_collection, rating_collection, ticket_collection, user_collection
from typing import Optional
from pymongo.collection import Collection
from bson import ObjectId

router = APIRouter()

#dodavanje muzeja 
@router.post("/museums")
async def add_museum(museum: Museum):
    if museum_collection.find_one({"name": museum.name, "location": museum.location}):
        raise HTTPException(status_code=400, detail="Museum already exists")
    museum_collection.insert_one(museum.dict())
    return {"message": "Museum added successfully"}

#komentiranje muzeja 
@router.post("/comment")
async def add_comment(museum_id: str, comment: Comment):

    objInstance = ObjectId(museum_id)
    if not museum_collection.find_one({"_id": objInstance}):
        raise HTTPException(status_code=404, detail="Museum not found")
    
    objInstancea = ObjectId(comment.user_id)
    if not user_collection.find_one({"_id":objInstancea}):
        raise HTTPException(status_code=404, detail="User not found")

    comment_data = comment.dict()
    comment_data["museum_id"] = museum_id 
    comment_collection.insert_one(comment_data)
    return {"message": "Comment added successfully"}



@router.post("/rate")
async def rate_museum(museum_id: str, rating: Rating):
    objInstance = ObjectId(museum_id) 
    if not museum_collection.find_one({"_id": objInstance}):
        raise HTTPException(status_code=404, detail="Museum not found")

    rating_dict = rating.dict()
    rating_dict["museum_id"] = museum_id

    rating_collection.insert_one(rating_dict)
    return {"message": "Rating added successfully"}


@router.get("/search")
async def search_museums(name: Optional[str] = None, location: Optional[str] = None, min_rating: Optional[float] = None):
    query = {}
    if name:
        query["name"] = {"$regex": f".*{name}.*", "$options": "i"}
    if location:
        query["location"] = {"$regex": f".*{location}.*", "$options": "i"}

    museums = list(museum_collection.find(query))

    if min_rating:
       
        museums = [museum for museum in museums if get_average_rating(museum["_id"]) >= min_rating]

    return museums

def get_average_rating(museum_id):
    ratings = rating_collection.aggregate([
        {"$match": {"museum_id": ObjectId(museum_id)}},
        {"$group": {
            "_id": "$museum_id",
            "average_rating": {"$avg": "$score"}
        }}
    ])
    average_rating = list(ratings)
    if average_rating:
        return average_rating[0]["average_rating"]
    else:
        return 0  


@router.post("/purchase_ticket")
async def purchase_ticket(museum_id: str, ticket: Ticket):
    objInstance = ObjectId(museum_id)
    if not museum_collection.find_one({"_id": objInstance}):
        raise HTTPException(status_code=404, detail="Museum not found")
    ticket.museum_id = museum_id
    ticket_collection.insert_one(ticket.dict())
    return {"message": "Ticket purchased successfully"}


@router.delete("/Deletecomment")
async def delete_comment(comment_id: str, user_id: str = Query(...)): 
    objInstance = ObjectId(comment_id)
    comment = comment_collection.find_one({"_id": objInstance})
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
   
    comment_collection.delete_one({"_id": objInstance})
    return {"message": "Comment deleted successfully"}

