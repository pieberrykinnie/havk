from .auth import router as auth_router
from .resources import router as resources_router
from .solutions import router as solutions_router

__all__ = [
    "auth_router",
    "resources_router",
    "solutions_router",
]