from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.car_router import router as car_router
from routers.garage_router import router as garage_router
from routers.maintenance_router import router as maintenance_router

app = FastAPI()

# List of allowed origins (frontend URL)
origins = [
    "http://localhost:3000",  # Frontend URL
]

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Include the car router from car_router
app.include_router(car_router)
app.include_router(garage_router)
app.include_router(maintenance_router)

# You can add more routers here as needed
