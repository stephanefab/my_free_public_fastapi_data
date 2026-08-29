from fastapi import FastAPI, Query, Path, Header

## initialisation de l'app
app = FastAPI()

@app.get("/")
def home():
    return {"message": "Bienvenue dans mon API"}

@app.get("/about")
def about():
    return {"name": "Fabien", "age": 27, "job": "Developer"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/path/{path_id}")
def path_test(path_id):
    return {
        "value": path_id,
        "type": type(path_id).__name__
    }

@app.get("/users/{user_id}")
def get_user(user_id: int = Path(ge=1)):
    return {
        "user_id": user_id,
        "message": "Utilisateur trouvé"
    }

@app.get("/products/{product_id}")
def get_product(product_id: int = Path(ge=1)):
    return {
        "product_id": product_id
    }

@app.get("/users")
def get_users(page: int = Query(default=1, ge=1), limit: int = Query(default=10, ge=1, le=50)):
    return {
        "limit": limit,
        "page": page
    }
    
@app.get("/products")
def get_products(page: int = Query(default=1, ge=1), limit: int = Query(default=10, ge=1, le=50)):
    return {
        "limit": limit,
        "page": page
    }

@app.get("/headers")
def get_headers(x_client_name: str = Header(default="")):
    return {
        "client": x_client_name
    }