from db import db
from sqlalchemy import select
# from application.orm.brand import Brand
# from application.orm.category import Category
# from application.orm.member import Supplier
from application.models.brand import Brand
from application.models.category import Category
from application.models.member import Supplier
import datetime


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
    def getProductById(product_id):
        product_record = Product.query.filter_by(product_id=product_id).first()
        return Product.getProduct_FullInfo(product_record)

    #取得單個產品完整資訊
    def getProduct_FullInfo(self):
        P_full_record = db.session.query(Product,Brand.brand_name,Category.category_name,Supplier.supplier_name
                    ).filter_by(product_id=self.product_id).join(Brand,Product.brand_id==Brand.brand_id
                    ).join(Category,Product.category_id==Category.category_id
                    ).join(Supplier,Product.supplier_id == Supplier.supplier_id).first()
        product_full_json = {
            'product_id': P_full_record[0].product_id,
            'product_name': P_full_record[0].product_name,
            'product_model': P_full_record[0].product_model,
            'brand_id': P_full_record[0].brand_id,
            'brand_name': P_full_record[1],
            'category_id': P_full_record[0].category_id,
            'category_name': P_full_record[2],
            'supplier_id': P_full_record[0].supplier_id,
            'supplier_name': P_full_record[3],
            'create_time': P_full_record[0].create_time.strftime("%m/%d/%Y, %H:%M:%S"),
            'details': P_full_record[0].details
        }

        return product_full_json

    #取得所有產品記錄
    def getProductList():
        products = db.session.query(Product).all()
        product_list_json = {
            'Products': [record.getProduct_FullInfo() for record in products]
        } 
        return product_list_json

    # 取得該類最新產品記錄
    def getThisCategory_LastP(catergory_id):
        lastP=db.session.query(Product).filter_by(category_id=catergory_id).order_by(Product.product_id.desc()).first()
        return lastP

    # 取得該類產品新id 
    def getThisCategory_NewP_id(catergory_id):
        lastP_id=Product.getThisCategory_LastP(catergory_id)
        lastest_id_cater = lastP_id.product_id[0:2]
        lastest_id = lastP_id.product_id[2:8]
        return lastest_id_cater+str(int(lastest_id) +1).zfill(6)
    
    #新增產品
    def createProduct(new_Pname,new_Pmodel,new_Pbrand,new_Pcate,new_Psupp,new_Pdetails):
        curr_datetime = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        print(curr_datetime)
        new_Pid = Product.getThisCategory_NewP_id(new_Pcate)
        add_product = Product(new_Pid,new_Pname,new_Pmodel,new_Pbrand,new_Pcate,new_Psupp,curr_datetime,new_Pdetails)
        db.session.add(add_product)
        db.session.commit()
        return add_product

    #新增產品所需資料
    def createP_selectList():
        brand_list = db.session.query(Brand).all()
        supplier_list = db.session.query(Supplier).all()
        category_list = db.session.query(Category).all()
        pAdd_list_json = {
            'data': {
                'brand_list':{'brand_id':[record.brand_id for record in brand_list],
                            'brand_name':[record.brand_name for record in brand_list]
                }, 
                "supplier_list":{'supplier_id':[record.supplier_id for record in supplier_list],
                                 'supplier_name':[record.supplier_name for record in supplier_list]
                },
                "category_list":{'category_id':[record.category_id for record in category_list],
                                 'category_name':[record.category_name for record in category_list]
                },
                "title": "product_create"
            }
        }
        return pAdd_list_json

    #新增產品所需資料
    def UpdateProductInfo(product_id,update_data):
        product = Product.query.filter_by(product_id=product_id).first()
        for data in update_data:
                print( data[0],data[1])
                product.locals()[data[0]] = data[1]
        # product.product_name = update_data['product_name']
        # product.product_model = update_data['product_model']
        # product.brand_id = update_data['brand_id']
        # product.category_id = update_data['category_id']
        # product.supplier_id = update_data['supplier_id']
        # product.details = update_data['details']
        # db.session.commit()
        return {'message':"hi"}
