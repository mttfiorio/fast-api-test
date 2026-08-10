from fastapi import FastAPI, HTTPException
from models import Product

app = FastAPI()

@app.get("/")
def greet():
    return "Hello, World!"

products = [Product(id=1, name="Product 1", description="Description 1", price=100, quantity=100)]

@app.get("/products")
def get_products():
    return products

@app.get("/product/{id}")
def get_products_by_id(id: int):
    # in js terms[product.id for product in products] is the same as products.map(product => product.id)
    if id not in [product.id for product in products]:
        raise HTTPException(status_code=404, detail="Product not found")
   
    # for product in products - iterates over products
    # if product.id == id - only considers items with this condition
    # product (at the start) - what to yield out of this function 
    # next() - returns the first item that satisfies the condition. It's lazy and doesn't compute all items.
    product = next(product for product in products if product.id == id)
    return product

@app.post("/product")
def create_product(product: Product):
    products.append(product)
    return product

@app.put("/product/{id}")
def update_product(id: int, product: Product):

    # The old way of doing this is:
    #   for i in range(len(products)):
    #     p = products[i]
    #   enumerate(products) - returns a tuple of (index, product), so it's preferred
    for i, p in enumerate(products):
        if p.id == id:
            products[i] = product
            return product
    raise HTTPException(status_code=404, detail="Product not found")

@app.delete("/product/{id}")
def delete_product(id: int):
    productToDelete = next((product for product in products if product.id == id), None)
    if productToDelete is None:
        raise HTTPException(status_code=404, detail="Product not found")

    products.remove(productToDelete)
    return {"message": "Product deleted successfully"}
