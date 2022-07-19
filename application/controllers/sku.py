import datetime
from html import parser
from lib2to3.pgen2.parse import Parser
from urllib import response
from flask_restful import Resource, reqparse
from db import db
from application.models.sku import Sku
#from application.models.product import Product
#from application.models.transaction import Transaction, ReStock, ReStockDetail

class SkuAPI(Resource):
    LIST_URL = '/sku/<date>'

    def get(self, date):
        parser = reqparse.RequestParser()
        parser.add_argument('sku_id', type=str,required=True)
        parser.add_argument('chkstaff_id',type=str,required=True)

        sku = db.session.query(Sku).all()

        if not sku:
            return{'message':'No stock record could be found'}

        sku_json = {
            'sku': [record.to_json() for record in sku]
        } 
      
        return sku_json
    
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('sku_id', type=str,required=True)
        parser.add_argument('chkstaff_id',type=str,required=True)
        parser.add_argument('chk_date', type=datetime, required=True)
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
        parser.add_argument('chk_amount', type=int, required=True)
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

        db.session.add(sku)
        db.session.commit()    
        return 