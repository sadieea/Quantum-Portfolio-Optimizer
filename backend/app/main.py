from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from contextlib import asynccontextmanager

from app.config import settings
from app.database import create_tables
from app.routes import auth, dataset, optimize, results, user
from app.utils.logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting Quantum Portfolio Optimizer API")
    create_tables()
    logger.info("Database tables created")
    yield
    # Shutdown
    logger.info("Shutting down Quantum Portfolio Optimizer API")


# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.DESCRIPTION,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Include routers
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["authentication"])
app.include_router(dataset.router, prefix=f"{settings.API_V1_STR}/datasets", tags=["datasets"])
app.include_router(optimize.router, prefix=f"{settings.API_V1_STR}/optimize", tags=["optimization"])
app.include_router(results.router, prefix=f"{settings.API_V1_STR}/results", tags=["results"])
app.include_router(user.router, prefix=f"{settings.API_V1_STR}/users", tags=["users"])


@app.get("/")
async def root():
    return {
        "message": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "status": "running",
        "docs_url": "/docs",
        "api_version": settings.API_V1_STR
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT,
        "debug": settings.DEBUG
    }


@app.get(f"{settings.API_V1_STR}/info")
async def api_info():
    return {
        "title": settings.PROJECT_NAME,
        "description": settings.DESCRIPTION,
        "version": settings.VERSION,
        "quantum_backend": settings.QISKIT_BACKEND,
        "classical_solver": settings.CLASSICAL_SOLVER,
        "qubo_sampler": settings.QUBO_SAMPLER
    }