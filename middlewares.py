from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


class CustomHeaderMiddleware(BaseHTTPMiddleware):

    def __init__(self, app, header_value):
        super(CustomHeaderMiddleware, self).__init__(app)

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Process-Time"] = str(0.5)
        return response