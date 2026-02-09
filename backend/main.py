from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

# DB setup
from db.database import engine
from db import models

models.Base.metadata.create_all(bind=engine)

# Routers
from routers import plan, health

app = FastAPI(title="AI Startup Simulator")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(plan.router)
app.include_router(health.router)