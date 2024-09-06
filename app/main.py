import models
import routers
import models.users
from fastapi import FastAPI
from db import engine
import routers.users

app = FastAPI()

app.include_router(routers.users.router, tags=["Users"])



