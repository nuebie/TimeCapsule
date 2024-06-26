from fastapi import FastAPI
from routes import user, authentication

app = FastAPI()

app.include_router(user.router)
app.include_router(authentication.router)
