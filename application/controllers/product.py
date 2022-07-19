# -*- coding: utf-8 -*-
from itertools import product
import re
from urllib import response
from flask_restful import Resource, reqparse
from db_pyodbc import cnxn
from db import db
from ..models.product import Product
from ..models.brand import Brand
from ..models.category import Category
from ..models.member import Supplier

class ProductCTRL(Resource):

    LIST_URL= '/product/<brand_id>'
    parser = reqparse.RequestParser()
    parser.add_argument('product_name', required=True, help='Product Name is required',location=['form'])
    parser.add_argument('product_model', required=True, help='Product Model is required',location=['form'])
    
    def get(self, brand_id):
        products = Product.query.filter_by(brand_id=brand_id).order_by(Product.product_id.desc()).all()
        json = {
            'Products': [record.to_json() for record in products]
        } 
        return json

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
        product = Product.query.filter_by(product_name='iPhone 14').first()
        product.product_name = 'iPhone 14 Pro'
        db.session.commit()
        return 

    def delete(self):
        # 刪除資料
        query = Product.query.filter_by(product_name='iPhone 14').first()
        db.session.delete(query)
        db.session.commit()
        return 


class ProductsListCTRL(Resource):
    LIST_URL='/products/'
    parser = reqparse.RequestParser()
    parser.add_argument('product_name', required=True, help='Product Name is required',location=['form'])
    parser.add_argument('product_model', required=True, help='Product Model is required',location=['form'])
    
    def get(self):

        products = db.session.query(Product).all()
        json = {
            'Products': [record.to_json() for record in products]
        } 
        # query = Product.query.filter_by(brand_id='B0002').order_by(Product.product_id.desc()).all()
        # for record in query :
        #     print(record.product_id,record.product_name)
        return json

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


class AddProductCTRL(Resource):

    LIST_URL= '/addproduct/'
    parser = reqparse.RequestParser()
    parser.add_argument('product_name', required=True, help='Product Name is required',location=['form'])
    parser.add_argument('product_model', required=True, help='Product Model is required',location=['form'])
    parser.add_argument('brand_id', required=True, help='brand_id is required',location=['form'])
    parser.add_argument('category_id', required=True, help='category_id is required',location=['form'])
    parser.add_argument('supplier_id', required=True, help='supplier_id is required',location=['form'])
    parser.add_argument('details', required=True, help='details is required',location=['form'])
    
    def get(self):
        #新增產品所需資料
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


    def post(self):
         # 新增一筆產品資料
        try:
            arg =self.parser.parse_args()
            print(arg["product_name"],arg["product_model"],arg["brand_id"],arg["category_id"],arg["supplier_id"],arg["details"])
            # Product.query.filter_by(category_id=arg["category_id"]).order_by(Product.product_id.desc()).all()
            product_add = Product('SP000012',f'{arg["product_name"]}',f'{arg["product_model"]}','B0002',1,4,'2022/01/01 20:37:21',arg["details"])
            db.session.add(product_add)
            db.session.commit()
            # return {'message':f'insert {product_add}success'},200
            return {'message':f'insert {arg["product_name"],arg["product_model"],arg["brand_id"],arg["category_id"],arg["supplier_id"],arg["details"]} success'},200
        except Exception as e:
            print (e)
            return {"error message":f'{e}'}

    def put(self):
        # Update data
        product = Product.query.filter_by(product_name='iPhone 14').first()
        product.product_name = 'iPhone 14 Pro'
        db.session.commit()
        return 

    def delete(self):
        # 刪除資料
        query = Product.query.filter_by(product_id='SP000012').first()
        db.session.delete(query)
        db.session.commit()
        return 
            