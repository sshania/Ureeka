from fastapi import FastAPI
from auth import auth_router as auth_router
from course import course_router as course_router
from material import material_router as material_router
from answer import answer_router as answer_router

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello Guys. Welcome to the API"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "query": q}


# Routing > (buat jadiin satu pas beda file gitu) 
app.include_router(auth_router, prefix="/auth")
app.include_router(course_router, prefix="/course")
app.include_router(material_router, prefix="/material")
app.include_router(answer_router, prefix="/answer")


# Apply Middleware
# app.middleware("https")(log_requests)
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Adjust to your needs
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Health Check (test api jalan atau ga)
# @app.get("/api")
# @limiter.limit("50/minute")
# async def root(request: Request):
#     return {"message": "AI REST API is running"}