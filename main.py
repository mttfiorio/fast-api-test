from fastapi import FastAPI, HTTPException, Depends
from models.Product import ProductSchema, Product
from config import get_db
from sqlalchemy.orm import Session

app = FastAPI()

@app.get("/")
def greet():
    return "Hello, World!"


@app.get("/products")
# Depends(get_db) -  It's a dependency injection. FastAPI calls get_db automatically and passes the session to the function
def get_products(db: Session = Depends(get_db)):
    return db.query(Product).all()

@app.get("/product/{id}")
def get_products_by_id(id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

    """
    # in js terms[product.id for product in products] is the same as products.map(product => product.id)
    if id not in [product.id for product in products]:
        raise HTTPException(status_code=404, detail="Product not found")
   
    # for product in products - iterates over products
    # if product.id == id - only considers items with this condition
    # product (at the start) - what to yield out of this function 
    # next() - returns the first item that satisfies the condition. It's lazy and doesn't compute all items.
    product = next(product for product in products if product.id == id)
    return product
    """

@app.post("/product")
def create_product(product: ProductSchema, db: Session = Depends(get_db)):
    # exclude_none=True means: "don't include fields that are None". Used for the id
    # model_dump() - converts the Pydantic model to a dictionary
    db_product = Product(**product.model_dump(exclude_none=True))
    db.add(db_product)
    db.commit()
    return db_product

@app.put("/product/{id}")
def update_product(id: int, product: ProductSchema, db: Session = Depends(get_db)):
    db.query(Product).filter(Product.id == id).update(product.model_dump())
    db.commit()
    return product

    """
    # The old way of doing this is:
    #   for i in range(len(products)):
    #     p = products[i]
    #   enumerate(products) - returns a tuple of (index, product), so it's preferred
    for i, p in enumerate(products):
        if p.id == id:
            products[i] = product
            return product
    raise HTTPException(status_code=404, detail="Product not found")
    """

@app.delete("/product/{id}")
def delete_product(id: int, db: Session = Depends(get_db)):
    productToDelete = db.query(Product).filter(Product.id == id).first()
    if productToDelete is None:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(productToDelete)
    db.commit()
    return {"message": "Product deleted successfully"}

    """
    productToDelete = next((product for product in products if product.id == id), None)
    if productToDelete is None:
        raise HTTPException(status_code=404, detail="Product not found")

    products.remove(productToDelete)
    return {"message": "Product deleted successfully"}
    """
