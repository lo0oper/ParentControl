
from fastapi import FastAPI, HTTPException, Request,status
from fastapi.responses import StreamingResponse, JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from datetime import datetime, timedelta
from log.logger import logger
import dotenv
import jwt
import os

from auth.authentication import Authentication

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
        client_ip = request.client.host if request.client else "Unknown_host"
       
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
        self.authenticator = Authentication()
        super().__init__(app)
        # dict to store email:token for an incoming request of a user
        self.auth_data = {}
    
    async def dispatch(self, request, call_next):
        header_data = request.headers
        body = await request.json()
        log.debug(f'header info : {header_data}')
        log.debug(f'request body  : {body}')
        jwt_token=''
        
         # Check if the request is for the signup or login route
        if request.url.path in ["/signup", "/login"]:
            return await call_next(request)  # Skip middleware for these routes
        
        try:
            ## Optimise here once jwt token created we don't need to reauthenticate again
            if self.authenticator.authenticate(body['email'],header_data.get('authorization',jwt_token)):
                response = await call_next(request)
                return response
            else:
                log.error("Authentication failed in middleware")

        except HTTPException as exc:
            # Re-raise the HTTPException caught in middleware
            log.error(f"HTTPException caught in middleware: {exc.detail}")
            raise exc
        except Exception as exc:
            # Catch any other exceptions and return a generic 500 error
            log.error(f"Unexpected error in middleware: {str(exc)}")
            raise HTTPException(
                status_code=500,
                detail="Internal server error occurred in middleware."
            )
            

            
        

