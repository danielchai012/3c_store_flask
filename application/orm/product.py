from db import db
from sqlalchemy import select

class ProductORM(db.Model):
    __tablename__ = 'product'

    product_id = db.Column(db.String(8), primary_key=True)
    product_name = db.Column(db.String(100), nullable=True)
    product_model = db.Column(db.String(30), nullable=True)
    brand_id = db.Column(db.String(5), db.ForeignKey('brand.brand_id'), nullable=True)
    category_id = db.Column(db.Integer,db.ForeignKey('category.category_id'), nullable=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.supplier_id'),nullable=True)
    create_time = db.Column(db.DateTime(), nullable=True)
    details = db.Column(db.String(500), nullable=True)


    def __init__(self, product_id ,product_name,product_model,brand_id,category_id,supplier_id,create_time,details):
        self.product_id=product_id
        self.product_name=product_name
        self.product_model =product_model
        self.brand_id =brand_id
        self.category_id=category_id
        self.supplier_id=supplier_id
        self.create_time = create_time
        self.details=details