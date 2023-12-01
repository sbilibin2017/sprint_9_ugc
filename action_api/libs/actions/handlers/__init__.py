from .bookmarks import router as bookmark_router
from .likes import router as likes_router
from .reviews import router as review_router

__all__ = [
    "likes_router",
    "review_router",
    "bookmark_router",
]
