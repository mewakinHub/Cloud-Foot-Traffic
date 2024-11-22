from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import download_routes, create_routes, delete_routes, read_routes, update_routes

app = FastAPI()

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(create_routes.router, prefix="/create", tags=["create"])
app.include_router(read_routes.router, prefix="/read", tags=["read"])
app.include_router(update_routes.router, prefix="/update", tags=["update"])
app.include_router(delete_routes.router, prefix="/delete", tags=["delete"])
app.include_router(download_routes.router, prefix="/download", tags=["download"])
