# -*- coding: utf-8 -*-
from itertools import product
import re
from select import select
from urllib import response
from flask_restful import Resource, reqparse
from db_pyodbc import cnxn
from db import db
from ..models.product import Product
from ..models.brand import Brand
from ..models.category import Category
from ..models.member import Supplier

class ProductController(Resource):

    LIST_URL= '/product/<product_id>'
    CREATE_URL= '/product/'
    parser = reqparse.RequestParser()
    parser.add_argument('product_name', required=True, help='Product Name is required',location=['form'])
    parser.add_argument('product_model', required=True, help='Product Model is required',location=['form'])
    
    # def get(self, brand_id):
    #     products = Product.query.filter_by(brand_id=brand_id).order_by(Product.product_id.desc()).all()
    #     json = {
    #         'Products': [record.to_json() for record in products]
    #     } 
    #     return json
    
    #用產品id做查詢
    def get(self, product_id):
        try:
            product_info_json = Product.getProductById(product_id)
            return product_info_json
        except Exception as e:
                print (e)
                return {"error message":"無法查詢該筆資料,請檢查是否輸入錯誤"}

    def post(self):
         # 新增資料
        try:
            arg =self.parser.parse_args()
            Product()
            product_add = Product('SP000011',f'{arg["product_name"]}',f'{arg["product_model"]}','B0002',1,4,'2022/01/01 20:37:21','蘋果14')
            db.session.add(product_add)
            db.session.commit()
            return {'message':f'insert {product_add}success'},200
        except Exception as e:
            print (e)
            return {"error message":f'{e}'}

    def put(self):
        # Update data
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('product_id', required=True, help='Product id is required',location=['form'])
            parser.add_argument('product_name', required=True, help='Product Name is required',location=['form'])
            parser.add_argument('product_model', required=True, help='Product Model is required',location=['form'])
            parser.add_argument('brand_id', help='Product Model is required',location=['form'])
            parser.add_argument('category_id',help='Product Model is required',location=['form'])
            parser.add_argument('supplier_id', help='Product Model is required',location=['form'])
            parser.add_argument('details', required=False, help='details is required',location=['form'])
            req_data =parser.parse_args()
            # product = Product.query.filter_by(product_id=req_data['product_id']).first()
            # print (product)
        except Exception as e:
            return {"error message":f'{e}'}
        else:
            update_list = []
            for data in req_data.items():
                if data[1] != None :
                    update_list.append(data)
                    # print(req_data.values())
            print(update_list)
            Product.UpdateProductInfo(req_data['product_id'],update_list)
            # product.product_name = req_data['product_name']
            # product.product_model = req_data['product_model']
            # product.brand_id = req_data['brand_id']
            # product.category_id = req_data['category_id']
            # product.supplier_id = req_data['supplier_id']
            # product.details = req_data['details']
            # db.session.commit()
            return {"message":"update success"}

    def delete(self,product_id):
        # 刪除資料by product_id
        try:
            selected_product = Product.query.filter_by(product_id=product_id).first()
            db.session.delete(selected_product)
            db.session.commit()
            return {'message': f'delete product {product_id} success'}
        except Exception as e:
            print (e)
            return {'message': f'delete product {product_id} failed'}



class ProductsListController(Resource):
    LIST_URL='/products/'
    parser = reqparse.RequestParser()
    parser.add_argument('product_name', required=True, help='Product Name is required',location=['form'])
    parser.add_argument('product_model', required=True, help='Product Model is required',location=['form'])
    
    def get(self):
        # 取得所有產品記錄
        product_list_json = Product.getProductList()
        return product_list_json

    def post(self):
         # 新增資料
        try:
            arg =self.parser.parse_args()
            product_add = Product('SP000011',f'{arg["product_name"]}',f'{arg["product_model"]}','B0002',1,4,'2022/01/01 20:37:21','蘋果14')
            db.session.add(product_add)
            db.session.commit()
            return {'message':f'insert {product_add}success'},200
        except Exception as e:
            print (e)
            return {"error message":f'{e}'}


class AddProductController(Resource):

    LIST_URL= '/addproduct/'
    parser = reqparse.RequestParser()
    parser.add_argument('product_name', required=True, help='Product Name is required',location=['form'])
    parser.add_argument('product_model', required=True, help='Product Model is required',location=['form'])
    parser.add_argument('brand_id', required=True, help='brand_id is required',location=['form'])
    parser.add_argument('category_id', required=True, help='category_id is required',location=['form'])
    parser.add_argument('supplier_id', required=True, help='supplier_id is required',location=['form'])
    parser.add_argument('details', required=True, help='details is required',location=['form'])
    
    def get(self):
        #取得新增產品所需資料
        try:
            select_list = Product.createP_selectList()
            return select_list
        except Exception as e:
            print (e)
            return {"error message":f'{e}'}


    def post(self):
         # 新增一筆產品資料
        try:
            arg =self.parser.parse_args()
            message = (Product.createProduct(arg["product_name"],{arg["product_model"]},arg["brand_id"],arg["category_id"],arg["supplier_id"],arg["details"]))
            return {'message':f'insert {message} success'},200
        except Exception as e:
            print (e)
            return {"error message":f'{e}'}

    def put(self):
        # Update data
        product = Product.query.filter_by(product_name='iPhone 14').first()
        product.product_name = 'iPhone 14 Pro'
        db.session.commit()
        return 