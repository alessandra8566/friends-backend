from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from db import Base, engine
from minio_client import MinioClient
from router import user, image, profile
from starlette.middleware.base import BaseHTTPMiddleware

Base.metadata.create_all(bind=engine)

class LimitRequestSizeMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI, max_size: int):
        super().__init__(app)
        self.max_size = max_size

    async def dispatch(self, request: Request, call_next):
        if int(request.headers.get('content-length', 0)) > self.max_size:
            return JSONResponse(
                status_code=413,
                content={"message": "Request Entity Too Large"},
            )
        return await call_next(request)

app = FastAPI(debug=True)

app.add_middleware(LimitRequestSizeMiddleware, max_size=100 * 1024 * 1024) # 100 MB
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # List of allowed origins
    allow_credentials=True,  # Allow sending cookies or authorization headers
    allow_methods=["*"],     # Allow all HTTP methods (GET, POST, PUT, etc.)
    allow_headers=["*"],     # Allow all headers in the request
)

app.include_router(user.router, prefix="/api/users", tags=["users"])
app.include_router(profile.router, prefix="/api/profile", tags=["profile"])
app.include_router(image.router, prefix="/api/images", tags=["images"])

minio_client = MinioClient()