from app.routers.user_routes import router as user_routes
from app.routers.auth_routes import router as auth_routes
from app.routers.health_routes import router as health_routes
from app.routers.qrcode_routes import router as qrcode_routes
from app.routers.admin_routes import router as admin_routes

__all__ = [
    "user_routes",
    "auth_routes",
    "health_routes",
    "qrcode_routes",
    "admin_routes",
]
