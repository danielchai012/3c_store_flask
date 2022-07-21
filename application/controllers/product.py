# -*- coding: utf-8 -*-
from flask_restful import Resource, reqparse
from ..models.product import Product
from flask import abort
import traceback,sys
def abort_msg(e):

    error_class = e.__class__.__name__ # 引發錯誤的 class
    detail = e.args[0] # 得到詳細的訊息
    cl, exc, tb = sys.exc_info() # 得到錯誤的完整資訊 Call Stack
    lastCallStack = traceback.extract_tb(tb)[-1] # 取得最後一行的錯誤訊息
    fileName = lastCallStack[0] # 錯誤的檔案位置名稱
    lineNum = lastCallStack[1] # 錯誤行數 
    funcName = lastCallStack[2] # function 名稱
    # generate the error message
    errMsg = "Exception raise in file: {}, line {}, in {}: [{}] {}. Please contact the member who is the person in charge of project!".format(fileName, lineNum, funcName, error_class, detail)
    # return 500 code
    abort(500, errMsg)
class ProductController(Resource):

    LIST_URL= '/product/<product_id>'
    CREATE_URL= '/product/'

    
    #用產品id做查詢
    def get(self, product_id):
        try:
            product_info_json = Product.getProductById(product_id)
            return product_info_json
        except Exception as e:
                abort_msg(e)
                return {"error message":"無法查詢該筆資料,請檢查是否輸入錯誤"}
    # 新增資料
    def post(self):
        return {"message":'請至/addproduct 新增產品'}

    # 更新產品資料
    def put(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('product_id', required=True, help='Product id is required')
            parser.add_argument('product_name', help='Product Name is required')
            parser.add_argument('product_model',help='Product Model is required')
            parser.add_argument('brand_id', help='brand_id is required')
            parser.add_argument('category_id',help='category_id is required')
            parser.add_argument('supplier_id', help='supplier_id is required')
            parser.add_argument('details', required=False, help='details is required')
            req_data =parser.parse_args()
        except Exception as e:
            return {"error message":f'{e}可能參數不齊全'}
        else:
            updateMessage = Product.UpdateProductInfo(req_data['product_id'],req_data)
            return {"message":f"{updateMessage}"}

    # 刪除資料by product_id
    def delete(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('product_id', required=True, help='Product id is required')
            req_data =parser.parse_args()
            returnMessage = Product.DeleteProduct(req_data['product_id'])
            return returnMessage
        except Exception as e:
            print (e)
            return {'message': f'delete product failed'}



class ProductsListController(Resource):
    LIST_URL='/products/'
    parser = reqparse.RequestParser()
    parser.add_argument('product_name', required=True, help='Product Name is required')
    parser.add_argument('product_model', required=True, help='Product Model is required')
    
    # 取得所有產品記錄
    def get(self):
        product_list_json = Product.getProductList()
        return product_list_json

class AddProductController(Resource):

    LIST_URL= '/addproduct/'
    parser = reqparse.RequestParser()
    parser.add_argument('product_name', required=True, help='Product Name is required')
    parser.add_argument('product_model', required=True, help='Product Model is required')
    parser.add_argument('brand_id', required=True, help='brand_id is required')
    parser.add_argument('category_id', required=True, help='category_id is required')
    parser.add_argument('supplier_id', required=True, help='supplier_id is required')
    parser.add_argument('details', required=True, help='details is required')
    
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