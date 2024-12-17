
from fastapi import FastAPI, HTTPException, Depends,status
from fastapi.responses import JSONResponse
from h11 import Response
from pydantic import BaseModel
from mangum import Mangum
from fastapi.middleware.cors import CORSMiddleware
from middleware.middleware import RateLimitingMiddleware,LoggerMiddleware,AuthenticationMiddleware

from auth.authentication import Authentication
from log.logger import logger
from typing import Dict


log = logger
app = FastAPI()

# Initialize the Authentication class globally
authenticator = Authentication()

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
# app.add_middleware(RateLimitingMiddleware, dispatch=dispatch)

app.add_middleware(AuthenticationMiddleware)
# app.add_middleware(RateLimitingMiddleware)
app.add_middleware(LoggerMiddleware)


# In-memory user "database"
fake_users_db: Dict[str, Dict[str, str]] = {}
users_banned_websites_db: Dict[str, list[str]] = {}



# Models for incoming data
class UserSignup(BaseModel):
    email: str
    username: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class BannedWebsiteRequest(BaseModel):
    email: str
    banned_website: str


log.info("Starting safe-browsing-backend server....")

# Add banned Website to for a user
@app.post("/bannedWebsite")
def add_banned_website(request: BannedWebsiteRequest):
    try:
        user_email = request.email
        banned_website = request.banned_website
        
        log.info(f'adding banned website: ${banned_website} for ${user_email}')
        # Check if the user exists in the database
        if user_email not in users_banned_websites_db:
            users_banned_websites_db[user_email] = []  # Initialize empty list for this user
        
        # Check if the website is already banned
        if banned_website not in users_banned_websites_db[user_email]:
            users_banned_websites_db[user_email].append(banned_website)
            log.info(f"Website '{banned_website}' has been added to the banned list for {user_email}.")
        else:
            log.info(f"Website '{banned_website}' is already banned for {user_email}.")
        
        return users_banned_websites_db[user_email]
    except HTTPException as exc:
        # Handle specific HTTPException
        log.error(f"HTTPException caught in signup: {exc.detail}")
        raise exc
    except Exception as exc:
        # Handle unexpected errors
        log.error(f"Unexpected error in signup: {str(exc)}")
        raise HTTPException(status_code=500, detail="Internal server error occurred during signup.")
    

# Remove banned Website to for a user
@app.delete("/bannedWebsite")
def remove_banned_website(request: BannedWebsiteRequest):
    try:
        user_email = request.email
        banned_website = request.banned_website
        # Check if the user exists in the database
        if user_email not in users_banned_websites_db:
            log.info(f"No banned websites for {user_email}.")
            return
        
        # Check if the website is in the user's banned list
        if banned_website in users_banned_websites_db[user_email]:
            users_banned_websites_db[user_email].remove(banned_website)
            log.info(f"Website '{banned_website}' has been removed from the banned list for {user_email}.")
        else:
            log.info(f"Website '{banned_website}' is not banned for {user_email}.")

        return users_banned_websites_db[user_email]
    except HTTPException as e:
        raise e
        return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content=e.detail
            )

# Get banned Website to for a user
@app.get("/bannedWebsite")
def get_banned_websites(user_email: str):
    try:
        # Check if the user exists in the database
        if user_email not in users_banned_websites_db:
            print(f"No banned websites for {user_email}.")
            return []
        
        # Return the list of banned websites for the user
        return users_banned_websites_db[user_email]
    except HTTPException as e:
        return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content=e.detail
            )

# Signup route
@app.post("/signup")
async def signup(user: UserSignup):
    
    log.info(f"Signup called for :{user.email}")
    if user.email in fake_users_db:
        raise HTTPException(status_code=400, detail="user with this email already exists.")
    
    # STORING PASSWORD ALSO FOR CASES WHERE USER WANTS TO LOGIN AGAIN VIA EMAIL:PASSWORD
    hashed_password = authenticator.hash_password(user.password)
    fake_users_db[user.email] = {"password": hashed_password}

    return_payload ={
        "message":"User created successfully! Redirecting you to login page...",
        "status":200,
        "email":user.email
    }
    return return_payload



# Login route
@app.post("/login")
async def login(user: UserLogin):
    log.info(f'Login called with data: ${user.email}')
    user_record = fake_users_db.get(user.email)

    if not user_record or not authenticator.verify_password(user.password, user_record["password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password.")
    jwt_token = authenticator.getjwttoken(user.email,8764000)
    fake_users_db[user.email] = {"jwt_tokne":jwt_token}

    return {
            "message": "Login successful!",
            "email":user.email,
            "status":200,
            "jwt_token":jwt_token,
            "expiry":8763500
        }


# Adapter to handle AWS Lambda
handler = Mangum(app)
