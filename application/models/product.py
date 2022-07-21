from db import db
# from application.orm.brand import Brand
# from application.orm.category import Category
# from application.orm.member import Supplier
from application.models.brand import Brand
from application.models.category import Category
from application.models.member import Supplier
from application.orm.product import ProductORM
import datetime

class Product(db.Model):

    
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

    #取得產品by id
    def getProductById(product_id):
        product_record = ProductORM.query.filter_by(product_id=product_id).first()
        return Product.getProduct_FullInfo(product_record)

    #取得單個產品完整資訊
    def getProduct_FullInfo(self):
        try:
            P_full_record = db.session.query(ProductORM,Brand.brand_name,Category.category_name,Supplier.supplier_name
                        ).filter_by(product_id=self.product_id).join(Brand,Product.brand_id==Brand.brand_id
                        ).join(Category,ProductORM.category_id==Category.category_id
                        ).join(Supplier,ProductORM.supplier_id == Supplier.supplier_id).first()
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
        except Exception as e:
            error_json={"message":"該產品資訊不完整"}
            error_json.update(Product.to_json(self))
            return error_json

    #取得所有產品記錄
    def getProductList():
        try:
            products = db.session.query(Product).all()
            product_list_json = {
                'Products': [record.getProduct_FullInfo() for record in products]
            } 
            return product_list_json
        except Exception as e:
            pass

    # 取得該類最新產品記錄
    def getThisCategory_LastP(category_id):
        try:
            lastP=db.session.query(ProductORM).filter_by(category_id=category_id).order_by(ProductORM.product_id.desc()).first()      
            return lastP
        except Exception as e:
            pass

    # 取得該類產品新id 
    def getThisCategory_NewP_id(category_id):
        try:
            lastP_id=Product.getThisCategory_LastP(category_id)
            lastest_id_cater = lastP_id.product_id[0:2]
            lastest_id = lastP_id.product_id[2:8]
            return lastest_id_cater+str(int(lastest_id) +1).zfill(6)
        except Exception as e:
            try:
                cate_code=db.session.query(Category.category_code).filter_by(category_id=category_id).first()
                return cate_code.category_code+''.zfill(6)
            except Exception as e:
                return None
    
    #新增產品
    def createProduct(new_Pname,new_Pmodel,new_Pbrand,new_Pcate,new_Psupp,new_Pdetails):
        curr_datetime = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        new_Pid = Product.getThisCategory_NewP_id(new_Pcate)
        if (new_Pid == None):
            return "failed,pls check category"
        else:
            add_product = ProductORM(new_Pid,new_Pname,new_Pmodel,new_Pbrand,new_Pcate,new_Psupp,curr_datetime,new_Pdetails)
            db.session.add(add_product)
            db.session.commit()
            return new_Pid+" success"

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

    #更新產品
    def UpdateProductInfo(product_id,update_data):
        try:
            product = ProductORM.query.filter_by(product_id=product_id).first()
            update_message= []
            for data in update_data:
                print( data[0],data[1])
                if data[0]== "product_name":
                    product.product_name = data[1]
                    update_message.append(f"{data[0],data[1]} is updated")
                elif data[0]== "product_model":
                    product.product_model = data[1]
                    update_message.append(f"{data[0],data[1]} is updated")
                elif data[0]== "brand_id":
                    product.brand_id = data[1]
                    update_message.append(f"{data[0],data[1]} is updated")
                elif data[0]== "category_id":
                    product.category_id = data[1]
                    update_message.append(f"{data[0],data[1]} is updated")
                elif data[0]== "supplier_id":
                    product.supplier_id = data[1]
                    update_message.append(f"{data[0],data[1]} is updated")
                elif data[0]== "details":
                    product.details = data[1]
                    update_message.append(f"{data[0],data[1]} is updated")
                else: 
                    update_message.append(f"{data[0]} not a proper key")
            db.session.commit()
            update_message = ' '.join(update_message)
            return update_message
        except Exception as e:
            return {'message':"update error"}
    
    #刪除產品byid
    def DeleteProduct(product_id):
        try:
            selected_product = Product.query.filter_by(product_id=product_id).first()
            db.session.delete(selected_product)
            db.session.commit()
            return {'message': f'delete product {product_id} success'}  
        except Exception as e:
            return {'message': f'delete product {product_id} failed,請檢查產品是否存在'}