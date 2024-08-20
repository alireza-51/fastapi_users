from fastapi import FastAPI
from app.routers import users, login
from app.database import engine, Base
from dotenv import load_dotenv
import os
import asyncio

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Include routers
app.include_router(users.router, prefix="/api", tags=["users"])
app.include_router(login.router, prefix="/api", tags=["auth"])

# Lifespan event handler
async def lifespan(app: FastAPI):
    # Startup event
    async with engine.begin() as conn:
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)
    
    # Shutdown event
    yield
    await engine.dispose()

# Set the lifespan handler for the FastAPI app
app.lifespan = lifespan

# Start the application with Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
