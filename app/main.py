import routers
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware


import routers.auth
import routers.song
import routers.video
import routers.book
import frontRouters.front

from db import Base, engine


app = FastAPI()

app.mount("/static", StaticFiles(directory="./static"), name="static")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can specify the origins you want to allow
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(routers.auth.router, tags=["Users"])
app.include_router(routers.song.router, tags=["Songs"])
app.include_router(routers.video.router, tags=["Video"])
app.include_router(routers.book.router, tags=["Books"])


app.include_router(frontRouters.front.router, tags=["Front"])