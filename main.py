from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "query": q}


# contoh: ( buat jadiin satu pas beda file gitu)
# app.include_router(auth_router, prefix="/auth")
# app.include_router(dashboard_router, prefix="/dashboard")
# app.include_router(product_router, prefix="/product")
# app.include_router(superadmin_router, prefix="/superadmin")

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