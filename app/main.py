from builtins import Exception
from fastapi import FastAPI
from fastapi.response import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.database import Database
from app.dependencies import get_settings
from app.routers import event_routes, ui_routes, user_routes
from app.utils.api_description import getDescription
app = FastAPI(
    title="User Management",
    description=getDescription(),
    version="0.0.1",
    contact={
        "name": "API Support",
        "url": "http://www.example.com/support",
        "email": "support@example.com",
    },
    license_info={"name": "MIT", "url": "https://opensource.org/licenses/MIT"},
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Update this to match your Next.js app's URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    settings = get_settings()
    Database.initialize(settings.database_url, settings.debug)

@app.exception_handler(Exception)
async def exception_handler(request, exc):
    return JSONResponse(status_code=500, content={"message": "An unexpected error occurred."})

app.include_router(user_routes.router)
app.include_router(event_routes.router)
app.include_router(ui_routes.router)


