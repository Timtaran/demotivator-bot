__all__ = ["all_routers"]

from .media import media_router
from .common import common_router

all_routers = [media_router, common_router]
