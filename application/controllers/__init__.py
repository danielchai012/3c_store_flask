from flask import Blueprint
from flask_restful import Api

from .transaction import *
from .member import *
from .product import *
from .sku import *

transaction_bp = Blueprint('transaction', __name__)
member_bp = Blueprint('member', __name__)
product_bp = Blueprint('product', __name__)
sku_bp = Blueprint('sku', __name__)

product_api = Api(product_bp)
transaction_api = Api(transaction_bp)
member_api = Api(member_bp)
sku_api = Api(sku_bp)

transaction_api.add_resource(
    RestockController,
    RestockController.LIST_URL,
    RestockController.CREATE_URL
)
transaction_api.add_resource(
    RestockDataController,
    RestockDataController.LIST_URL,
    RestockDataController.CREATE_URL
)
transaction_api.add_resource(
    TransactionController,
    TransactionController.LIST_URL,
    TransactionController.CREATE_URL
)

member_api.add_resource(
    CustomerController,
    CustomerController.LIST_URL,
    CustomerController.CREATE_URL
)
member_api.add_resource(
    EmployeeController,
    EmployeeController.LIST_URL,
    EmployeeController.CREATE_URL
)

product_api.add_resource(
    ProductController,
    ProductController.LIST_URL,
    ProductController.CREATE_URL
    
)

product_api.add_resource(
    AddProductController,
    AddProductController.LIST_URL
)

product_api.add_resource(
    ProductsListController,
    ProductsListController.LIST_URL
)

sku_api.add_resource(
    SkuController,
    SkuController.LIST_URL,
    SkuController.CREATE_URL
)

sku_api.add_resource(
    SkuDataController,
    SkuDataController.LIST_URL,
    SkuDataController.CREATE_URL
)