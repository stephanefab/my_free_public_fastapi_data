from fastapi import FastAPI

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
def get_user(user_id: int):
    return {
        "user_id": user_id,
        "message": "Utilisateur trouvé"
    }

@app.get("/products/{product_id}")
def get_product(product_id: int):
    return {
        "product_id": product_id
    }
