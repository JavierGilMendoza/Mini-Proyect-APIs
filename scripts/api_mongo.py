from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, StringConstraints
from typing import Optional, List, Annotated
from pymongo import MongoClient
from bson import ObjectId
import datetime

app = FastAPI()

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["football_db"]
collection = db["matches"]

# Custom encoder for ObjectId
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

# Pydantic models
class Match(BaseModel):
    date: datetime.date
    hometeam: str
    awayteam: str
    ftr: Annotated[str, StringConstraints(pattern="^(1|X|2)$")]

class UpdateMatch(BaseModel):
    date: Optional[datetime.date]
    hometeam: Optional[str]
    awayteam: Optional[str]
    ftr: Optional[Annotated[str, StringConstraints(pattern="^(1|X|2)$")]]

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Football Match API with MongoDB and FastAPI"}

# Get matches with filters
@app.get("/matches", response_model=List[Match])
def get_matches(
    date: Optional[datetime.date] = None,
    season: Optional[str] = None,
    team: Optional[str] = None,
    home: Optional[bool] = None,
):
    query = {}

    if date:
        # Define range from start of the day to end of the day
        start_datetime = datetime.datetime.combine(date, datetime.time.min)
        end_datetime = datetime.datetime.combine(date, datetime.time.max)
        query["date"] = {"$gte": start_datetime, "$lte": end_datetime}

    # Team filtering
    if team:
        if home is True:
            query["hometeam"] = team
        elif home is False:
            query["awayteam"] = team
        else:
            query["$or"] = [{"hometeam": team}, {"awayteam": team}]

    # Season filtering
    if season:
        try:
            start_year, end_year = map(int, season.split("/"))
            start_date = datetime.datetime(start_year, 8, 1)
            end_date = datetime.datetime(end_year, 7, 31, 23, 59, 59)
            query["date"] = {"$gte": start_date, "$lte": end_date}
        except:
            raise HTTPException(status_code=400, detail="Season must be in format YYYY/YYYY")

    results = list(collection.find(query, {"_id": 0}))
    return results

# Insert a new match
@app.post("/matches")
def add_match(match: Match):
    # Convert date to datetime before inserting
    match_dict = match.model_dump()
    match_dict["date"] = datetime.datetime.combine(match.date, datetime.time.min)
    collection.insert_one(match_dict)
    return {"message": "Match inserted successfully"}

# Update a match by date and teams
@app.put("/matches")
def update_match(
    date: datetime.date,
    hometeam: str,
    awayteam: str,
    updated: UpdateMatch
):
    # Convert date to datetime for matching
    datetime_date = datetime.datetime.combine(date, datetime.time.min)

    update_data = updated.model_dump(exclude_unset=True)
    if "date" in update_data:
        update_data["date"] = datetime.datetime.combine(update_data["date"], datetime.time.min)

    result = collection.update_one(
        {"date": datetime_date, "hometeam": hometeam, "awayteam": awayteam},
        {"$set": update_data}
    )

    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Match not found or no changes made")

    return {"message": "Match updated successfully"}

# Delete a match by date and teams
@app.delete("/matches")
def delete_match(date: datetime.date, hometeam: str, awayteam: str):
    datetime_date = datetime.datetime.combine(date, datetime.time.min)

    result = collection.delete_one(
        {"date": datetime_date, "hometeam": hometeam, "awayteam": awayteam}
    )

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Match not found")

    return {"message": "Match deleted successfully"}