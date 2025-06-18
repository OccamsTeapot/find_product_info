from pydantic import BaseModel


class Product(BaseModel):
    brand: str
    product_name: str
    product_page: bool
    product_url_page: str

class ProductList(BaseModel):
    products: list[Product]
