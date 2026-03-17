from rest_framework.exceptions import NotFound, APIException
from .repositories import ProductRepository

class ProductService:
    def __init__(self):
        self.repo = ProductRepository()

    def _format_product(self, product):
        if product:
            product['id'] = str(product.pop('_id'))
        return product

    def get_all_products(self):
        try:
            products = self.repo.get_all()
            return [self._format_product(p) for p in products]
        except Exception:
            raise APIException("Error conectando a MongoDB")

    def get_product_by_id(self, product_id: str):
        product = self.repo.get_by_id(product_id)
        if not product:
            raise NotFound("No se ha encontrado el producto")
        return self._format_product(product)

    def create_product(self, product_data: dict):
        product = self.repo.create(product_data)
        return self._format_product(product)

    def update_product(self, product_id: str, product_data: dict):
        product = self.repo.update(product_id, product_data)
        if not product:
            raise NotFound("No se ha actualizado el producto")
        return self._format_product(product)

    def delete_product(self, product_id: str):
        success = self.repo.delete(product_id)
        if not success:
            raise NotFound("No se ha eliminado el producto")