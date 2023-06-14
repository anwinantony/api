from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBasicCredentials
from pydantic import BaseModel
from pymongo import MongoClient
from bson import ObjectId

app = FastAPI()

# Set up CORS
origins = [
   "*"
    # Add other allowed origins here
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set up database connection
client = MongoClient("mongodb+srv://eldhopaulose0485:xyzel_025@cluster0.4sjqm.mongodb.net/Trash?retryWrites=true&w=majority")
db = client["Trash"]
collection = db["users"]


class User(BaseModel):
    username: str
    points: int = 0


@app.post("/login")
async def login(user: User):
    try:
        user = collection.find_one({"username": user.username})
        if user:
            # Convert ObjectId to string
            user["_id"] = str(user["_id"])
            return user
        else:
            raise HTTPException(status_code=401, detail="Invalid username")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.post("/add-points")
async def add_points(user: User):
    try:
        updated_user = collection.find_one_and_update(
            {"username": user.username}, {"$inc": {"points": user.points}}, return_document=True
        )
        if updated_user:
            # Convert ObjectId to string
            updated_user["_id"] = str(updated_user["_id"])
            return updated_user
        else:
            raise HTTPException(status_code=400, detail="Failed to update points")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")