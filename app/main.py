from builtins import Exception
from fastapi import FastAPI, Request
from starlette.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
from app.database import Database
from app.dependencies import get_settings
from app.routers.user_routes import router as user_router
from app.routers.auth_routes import router as auth_router
from app.routers.health_routes import router as health_router
from app.routers.qrcode_routes import router as qrcode_router
from app.routers.admin_routes import router as admin_router
from app.utils.api_description import getDescription

# Initialize the FastAPI app
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

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (restrict in production).
    allow_credentials=True,  # Allow cookies and authorization headers.
    allow_methods=["*"],  # Allow all HTTP methods.
    allow_headers=["*"],  # Allow all HTTP headers.
)

# Startup event to initialize resources
@app.on_event("startup")
async def startup_event():
    """Startup event to initialize settings and database."""
    settings = get_settings()  # Load application settings.
    Database.initialize(settings.database_url, settings.debug)  # Initialize database connection.

# Shutdown event to clean up resources
@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event to clean up resources."""
    await Database.dispose_engine()  # Dispose the database engine gracefully.

# Global exception handler
@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    """Global exception handler for unhandled errors."""
    return JSONResponse(
        status_code=500,
        content={"message": "An unexpected error occurred.", "details": str(exc)},
    )

# Include routers for various modules
app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(health_router, prefix="/health", tags=["Health"])
app.include_router(qrcode_router, prefix="/qrcodes", tags=["QR Codes"])
app.include_router(admin_router, prefix="/admin", tags=["Admin"])
