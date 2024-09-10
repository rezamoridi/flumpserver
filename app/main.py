import routers
from fastapi import FastAPI

import routers.auth
import routers.song

from db import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(routers.auth.router, tags=["Users"])
app.include_router(routers.song.router, tags=["Songs"])