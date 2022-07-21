from datetime import datetime
from html import parser
from lib2to3.pgen2.parse import Parser
from urllib import response
from flask_restful import Resource, reqparse
from db import db
from application.models.sku import Sku
from application.models.product import Product

class SkuController(Resource):
    LIST_URL = '/sku/<sku_id>'
    CREATE_URL = '/sku'

    def get(self, sku_id):
        parser = reqparse.RequestParser()
        parser.add_argument('sku_id', type=str,required=True, location=['form'])
        parser.add_argument('chkstaff_id',type=str,required=True, location=['form'])

        sku = db.session.query(Sku).filter(
            Sku.sku_id == (sku_id if(sku_id!='all') else Sku.sku_id)
        ).all()

        if not sku:
            return{'message':'No stock record could be found'}

        sku_json = {
            'sku': [record.to_sku_json() for record in sku]
        } 
      
        return sku_json
    
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('sku_id', type=str,required=True, location=['form'])
        parser.add_argument('chkstaff_id',type=str,required=True, location=['form'])
        parser.add_argument('chk_date', type=datetime, required=True, location=['form'])
        req_data = parser.parse_args()
        print(req_data)
        sku = Sku.create(
            sku_id = req_data['sku_id'],
            chkstaff_id = req_data['chkstaff_id'],
            chk_date = req_data['chk_date'],
            chk_amount = 10
        )
        return {'sku_id': sku.sku_id}

    def put(self, sku_id):
        parser = reqparse.RequestParser()
        parser.add_argument('chk_amount', type=int, required=True, location=['form'])
        req_data = parser.parse_args()

        sku = db.session.query(Sku).filter(
            Sku.sku_id == sku_id
        ).first()
        if not sku:
            return{'message:'f'{sku_id}此sku_id不存在'}

        sku.chk_amount = req_data['chk_amount']
        db.session.add(sku)
        db.session.commit()
        return 

    def delete(self, sku_id):
        sku = db.session.query(Sku).filter(
            Sku.sku_id == sku_id
        ).first()

        if not sku:
            return{'message:'f'{sku_id}此sku_id不存在'}

        db.session.delete(sku)
        db.session.commit()    
        return 

class SkuDataController(Resource):
     LIST_URL = '/sku_data/<sku_id>'
     CREATE_URL = '/sku_data'

     def get(self, sku_id):
            sku = db.session.query(
                                Sku.sku_id,
                                Product.product_id,
                                Sku.sku_code,
                                Sku.sell_price,
                                Sku.recom_price,
                                Sku.cost,
                                Sku.stock_quantity
                            ).join(
                                Product,
                                Sku.product_id == Product.product_id,
                                isouter = True
                            ).all()
            sku_json = {
            'data': [{   
                        'sku_id': record[0],
                        'product_id': record[1],
                        'sku_code': record[2],
                        'sell_price': record[3],
                        'recom_price': record[4],
                        'cost': record[5],
                        'stock_quantity': record[6],
                    } for record in sku],
            'title': 'sku_data'
            } 
            return  sku_json                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
        

