from .user_routers import router as user_router
from .auth_routers import router as auth_router
from .task_routers import router as tasks_router
from .tags_routers import router as tags_router


def include_routers(app):
    app.include_router(user_router)
    app.include_router(auth_router)
    app.include_router(tasks_router)
    app.include_router(tags_router)