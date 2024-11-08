from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from mangum import Mangum
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict

import bcrypt
import logging

# Set up logging with INFO level
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
log = logging.getLogger(__name__)  # Alias 'log' for logger

app = FastAPI()




# Define allowed origins
origins = [
    "chrome-extension://edncinoabpchkhcajhbdpdbflcgppelj",  # Replace with your Chrome extension ID
]

# Add CORS middleware to the app
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Use "*" to allow all origins, but this is less secure
    allow_credentials=True,
    allow_methods=["*"],  # Define specific methods if needed, e.g., ["GET", "POST"]
    allow_headers=["*"],  # Define specific headers if needed, e.g., ["Content-Type"]
)

# In-memory user "database"
fake_users_db: Dict[str, Dict[str, str]] = {}

# Models for incoming data
class UserSignup(BaseModel):
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

# Utility function to hash password
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# Utility function to verify password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

# Signup route
@app.post("/signup")
async def signup(user: UserSignup):
    log.info("Signup called with ",{user.email})
    if user.email in fake_users_db:
        raise HTTPException(status_code=400, detail="user with this email already exists.")
    
    hashed_password = hash_password(user.password)
    fake_users_db[user.email] = {"password": hashed_password}
    return {"message": "User created successfully!"}

# Login route
@app.post("/login")
async def login(user: UserLogin):
    log.info("Login called with data:",user.email)
    user_record = fake_users_db.get(user.email)
    if not user_record or not verify_password(user.password, user_record["password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password.")
    return {"message": "Login successful!"}

# Adapter to handle AWS Lambda
handler = Mangum(app)
