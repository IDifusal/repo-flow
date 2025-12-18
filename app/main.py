import os
import logging
import time
from collections import defaultdict
from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response, JSONResponse
from contextlib import asynccontextmanager
from sqlalchemy import text
from slowapi import _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.db import Base, engine, get_session
from app.api.rest.recipes import router as recipe_router 
from app.api.graphql.schema import graphql_router
from app.middleware.rate_limit import limiter

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Simple rate limiter for GraphQL (100 requests per minute per IP)
_graphql_rate_limits = defaultdict(list)

def check_graphql_rate_limit(ip: str, limit: int = 100, window: int = 60) -> bool:
    """Check if IP has exceeded rate limit for GraphQL"""
    now = time.time()
    # Clean old entries
    _graphql_rate_limits[ip] = [t for t in _graphql_rate_limits[ip] if now - t < window]
    
    # Check if limit exceeded
    if len(_graphql_rate_limits[ip]) >= limit:
        return False
    
    # Add current request
    _graphql_rate_limits[ip].append(now)
    return True

@asynccontextmanager
async def lifespan(app: FastAPI):
    from app.models.recipe import Recipe
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Repo Flow Recipes API", 
    version="0.1.0", 
    lifespan=lifespan,
    max_request_size=int(os.getenv("MAX_REQUEST_SIZE", 1048576))  # 1MB default
)

# Add rate limiter to app state
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Configure CORS
cors_origins = os.getenv("CORS_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins if "*" not in cors_origins else ["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Security headers middleware
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response: Response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    
    # Add HSTS if HTTPS is detected
    if request.url.scheme == "https":
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    
    return response

# Rate limiting middleware for GraphQL
@app.middleware("http")
async def rate_limit_graphql(request: Request, call_next):
    if request.url.path.startswith("/graphql"):
        # Apply rate limiting to GraphQL endpoint (100 requests per minute)
        ip = get_remote_address(request)
        if not check_graphql_rate_limit(ip, limit=100, window=60):
            logger.warning(f"GraphQL rate limit exceeded for {ip}")
            return JSONResponse(
                status_code=429,
                content={"error": "Rate limit exceeded. Maximum 100 requests per minute."}
            )
    return await call_next(request)

# Logging middleware for security events
@app.middleware("http")
async def log_security_events(request: Request, call_next):
    response = await call_next(request)
    
    # Log rate limit blocks
    if response.status_code == 429:
        logger.warning(f"Rate limit exceeded for {get_remote_address(request)} - {request.url.path}")
    
    # Log validation errors
    if response.status_code == 422:
        logger.info(f"Validation error for {request.url.path} from {get_remote_address(request)}")
    
    # Log delete operations
    if request.method == "DELETE" and response.status_code in [204, 200]:
        logger.info(f"Delete operation on {request.url.path} from {get_remote_address(request)}")
    
    return response

app.include_router(graphql_router, prefix="/graphql")
app.include_router(recipe_router)

@app.get("/health")
def health_check() -> dict:
    return {"status": "ok"}

@app.get("/health/db")
def db_health_check(session=Depends(get_session)):
    session.execute(text("SELECT 1"))
    return {"database": "ok"}
