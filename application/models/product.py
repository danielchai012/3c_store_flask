from db import db
from sqlalchemy import select

class Product(db.Model):
    __tablename__ = 'product'
    # __table_args__ = {'mysql_charset': 'utf8mb4_unicode_ci'}

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

    def to_json(self):
        json = {
            'product_id': self.product_id,
            'product_name': self.product_name,
            'product_model': self.product_model,
            'brand_id': self.brand_id,
            'category_id': self.category_id,
            'supplier_id': self.supplier_id,
            'create_time': self.create_time.strftime("%m/%d/%Y, %H:%M:%S"),
            'details': self.details
        }
        return json
    
    # 取得該類最新產品 
    def getThisCategory_LastP(self,catergory_id):
        lastP=db.session.query(self).filter_by(category_id=catergory_id).order_by(Product.product_id.desc()).first()
        return lastP

    # 取得該類產品新id 
    def getThisCategory_NewP_id(self,catergory_id):
        lastP_id=self.getThisCategory_LastP(self,catergory_id)
        lastest_id_cater = lastP_id.product_id[0:2]
        lastest_id = lastP_id.product_id[2:8]
        return lastest_id_cater+str(int(lastest_id) +1).zfill(6)