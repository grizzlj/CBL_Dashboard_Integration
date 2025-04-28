from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.lti_launch import LTIMessageLaunch
import os

app = FastAPI()

# Set up templates folder
templates = Jinja2Templates(directory="app/templates")

# Root route (optional)
@app.get("/", response_class=HTMLResponse)
async def read_root():
    return "<h1>LTI Dashboard App Running</h1>"

# LTI launch route
@app.post("/lti/launch", response_class=HTMLResponse)
async def lti_launch(request: Request):
    try:
        # Validate launch request
        launch = await LTIMessageLaunch.from_request(request)

        user_id = launch.get_user_id()
        course_id = launch.get_course_id()

        # Render the dashboard template
        return templates.TemplateResponse("dashboard.html", {
            "request": request,
            "user_id": user_id,
            "course_id": course_id
        })

    except Exception as e:
        return HTMLResponse(content=f"Launch failed: {str(e)}", status_code=400)
