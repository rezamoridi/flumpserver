from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi.staticfiles import StaticFiles

# Create a router for your frontend routes
router = APIRouter()

# Define the templates directories
home_templates = Jinja2Templates(directory="templates/home")
auth_templates = Jinja2Templates(directory="templates/auth")

# Serve static files from the 'static' directory
router.mount("/static", StaticFiles(directory="./static"), name="static")

@router.get("/home", response_class=HTMLResponse)
async def home_template(request: Request):
    return home_templates.TemplateResponse("index.html", {"request": request})

@router.get("/auth/authentication")
async def auth_template(request: Request):
    return auth_templates.TemplateResponse("index.html", {"request": request})