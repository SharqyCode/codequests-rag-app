from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import ingest, ai, docs

app = FastAPI(title="AI Knowledge Assistant")

origins = [
    '*'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # Allows specific origins
    allow_credentials=True,           # Allows cookies and authentication headers
    allow_methods=["*"],              # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],              # Allows all request headers
)

# Register routers
app.include_router(ingest.router)
app.include_router(ai.router)
app.include_router(docs.router)


@app.get("/")
def root():
    return {"message": "API is running"}

for route in app.routes:
    print(route.path)