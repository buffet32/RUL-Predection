from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.config import settings
from app.routes import health, machines, sensor_readings, predictions, maintenance, reports, audit

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Predictive Maintenance API for RUL prediction and maintenance decision support"
)

# Add CORS middleware
# For development: allow frontend origin
# For production: replace with actual production domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite dev server
        "http://localhost:5174",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix=settings.API_PREFIX, tags=["health"])
app.include_router(machines.router, prefix=settings.API_PREFIX)
app.include_router(sensor_readings.router, prefix=settings.API_PREFIX)
app.include_router(predictions.router, prefix=settings.API_PREFIX)
app.include_router(maintenance.router, prefix=settings.API_PREFIX)
app.include_router(reports.router, prefix=settings.API_PREFIX, tags=["reports"])
app.include_router(audit.router, prefix=settings.API_PREFIX, tags=["audit"])


@app.on_event("startup")
async def startup_event():
    """Startup event to initialize services"""
    print(f"{settings.APP_NAME} v{settings.APP_VERSION} starting up...")


@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event to cleanup resources"""
    print(f"{settings.APP_NAME} v{settings.APP_VERSION} shutting down...")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
