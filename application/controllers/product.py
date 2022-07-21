# -*- coding: utf-8 -*-
from flask_restful import Resource, reqparse
from db import db
from ..models.product import Product

class ProductController(Resource):

    LIST_URL= '/product/<product_id>'
    CREATE_URL= '/product/'
    parser = reqparse.RequestParser()
    parser.add_argument('product_name', required=True, help='Product Name is required',location=['form'])
    parser.add_argument('product_model', required=True, help='Product Model is required',location=['form'])
    
    #用產品id做查詢
    def get(self, product_id):
        try:
            product_info_json = Product.getProductById(product_id)
            return product_info_json
        except Exception as e:
                print (e)
                return {"error message":"無法查詢該筆資料,請檢查是否輸入錯誤"}

    # 新增資料
    def post(self):
        return {"message":'請至/addproduct 新增產品'}

    # 更新產品資料
    def put(self):
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
        except Exception as e:
            return {"error message":f'{e}'}
        else:
            update_list = []
            for data in req_data.items():
                if data[1] != None :
                    update_list.append(data)

            updateMessage = Product.UpdateProductInfo(req_data['product_id'],update_list)

            return {"message":f"{updateMessage}"}

    # 刪除資料by product_id
    def delete(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('product_id', required=True, help='Product id is required',location=['form'])
            req_data =parser.parse_args()
            returnMessage = Product.DeleteProduct(req_data['product_id'])
            return returnMessage
        except Exception as e:
            print (e)
            return {'message': f'delete product failed'}



class ProductsListController(Resource):
    LIST_URL='/products/'
    parser = reqparse.RequestParser()
    parser.add_argument('product_name', required=True, help='Product Name is required',location=['form'])
    parser.add_argument('product_model', required=True, help='Product Model is required',location=['form'])
    
    # 取得所有產品記錄
    def get(self):
        product_list_json = Product.getProductList()
        return product_list_json

class AddProductController(Resource):

    LIST_URL= '/addproduct/'
    parser = reqparse.RequestParser()
    parser.add_argument('product_name', required=True, help='Product Name is required',location=['form'])
    parser.add_argument('product_model', required=True, help='Product Model is required',location=['form'])
    parser.add_argument('brand_id', required=True, help='brand_id is required',location=['form'])
    parser.add_argument('category_id', required=True, help='category_id is required',location=['form'])
    parser.add_argument('supplier_id', required=True, help='supplier_id is required',location=['form'])
    parser.add_argument('details', required=True, help='details is required',location=['form'])
    
    #取得新增產品所需資料
    def get(self):
        try:
            select_list = Product.createP_selectList()
            return select_list
        except Exception as e:
            print (e)
            return {"error message":f'{e}'}

    # 新增一筆產品資料
    def post(self):
        try:
            arg =self.parser.parse_args()
            message = (Product.createProduct(arg["product_name"],{arg["product_model"]},arg["brand_id"],arg["category_id"],arg["supplier_id"],arg["details"]))
            return {'message':f'insert {message}'},200
        except Exception as e:
            print (e)
            return {"error message":'無法新增'}