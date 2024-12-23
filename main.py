from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.car_router import router as car_router
from routers.garage_router import router as garage_router
from routers.maintenance_router import router as maintenance_router
app = FastAPI()

origins = [
    "http://localhost:3000",
]

#CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# routers
app.include_router(car_router)
app.include_router(garage_router)
app.include_router(maintenance_router)