from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import museum, users

app = FastAPI()

app.include_router(users.router)
app.include_router(museum.router)

origins = ["http://localhost:5173"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
