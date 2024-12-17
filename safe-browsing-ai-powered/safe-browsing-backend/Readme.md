#### STARTING THE SERVER LOCALY
1. run `uvicorn backend:app --reload`



### How to create the backEnd
1. Create python venv and activate it
2. install all requirements from requirements.txt or run `pip install fastapi mangum bcrypt`


## Details
1. When Signup called user provides email + password
    a. We register the user with its hashsed password in our database.
    b. Respond with email and success message only.
    c. Redirect user to login page, user provides the email and password.
        c.1. check users email and password.
        c.2. provide the jwt token.
    
    d. next call onwards in each call this token should be present.
