
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from datetime import datetime, timedelta
from log.logger import logger
import dotenv
import jwt
import os

secret = os.getenv('secret')
algorithm = os.getenv('algorithm')

dotenv.load_dotenv()
log = logger

class RateLimitingMiddleware(BaseHTTPMiddleware):
    # Rate limiting configurations
    RATE_LIMIT_DURATION = timedelta(minutes=1)
    RATE_LIMIT_REQUESTS = 3

    def __init__(self, app):
        super().__init__(app)
        # Dictionary to store request counts for each IP
        self.request_counts = {}

    async def dispatch(self, request:Request, call_next):
        # Get the client's IP address
        client_ip = request.client.host
       
        # Check if IP is already present in request_counts
        request_count, last_request = self.request_counts.get(client_ip, (0, datetime.min))

        # Calculate the time elapsed since the last request
        elapsed_time = datetime.now() - last_request

        if elapsed_time > self.RATE_LIMIT_DURATION:
            # If the elapsed time is greater than the rate limit duration, reset the count
            request_count = 1
        else:
            if request_count >= self.RATE_LIMIT_REQUESTS:
                # If the request count exceeds the rate limit, return a JSON response with an error message
                return JSONResponse(
                    status_code=429,
                    content={"message": "Rate limit exceeded. Please try again later."}
                )
            request_count += 1

        # Update the request count and last request timestamp for the IP
        self.request_counts[client_ip] = (request_count, datetime.now())

        # Proceed with the request
        response = await call_next(request)
        return response

class LoggerMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        # Dictionary to store request counts for each IP
        self.request_counts = {}
    
    async def dispatch(self,request:Request,call_next):
        log.info(f'{request.method} :: {request.url.path} invoked with {await request.json()}')
        response = await call_next(request)
        return response



class AuthenticationMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        # dict to store email:token for an incoming request of a user
        self.auth_data = {}
    
    async def dispatch(self, request, call_next):
        header_data = request.headers
        log.info(f'header info : ${header_data}')
        jwt_payload = {
            "userId":r
        }
        # auth_response = verify_jwt_token()
        # if(auth_response.status_code==200):
        #     response = await call_next(request)
        #     return response
        # elif (auth_response.status_code==403):
        #     response = await logout(request)
        #     return response
        # elif (auth_response.status_code==401):
        #     return {"status_code":401,"message":"unauthorized"}
        # else :
        #     return {"status_code":400,"message":"Authtoken incorrect"}

    def getjwttoken(self,algorithm,payload,secretkey):
        encoded = jwt.encode(payload, secretkey, algorithm=algorithm)
        return encoded
    
        

