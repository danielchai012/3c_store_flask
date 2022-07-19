from datetime import datetime
from urllib import response
from flask_restful import Resource, reqparse
from application.models.member import Customer, Employee, Supplier
from application.models.transaction import Transaction, ReStock, ReStockDetail
from application.models.sku import Sku
from application.models.product import Product

from db import db
# from db_pyodbc import cnxn
import uuid
# import json 

class TransactionController(Resource):
    LIST_URL = '/transaction/<trans_id>'
    CREATE_URL = '/transaction'

    def get(self, trans_id):
        parser = reqparse.RequestParser()
        parser.add_argument('employee_id', type=str, required=True, location=['form'])
        parser.add_argument('customer_id', type=str, required=True, location=['form'])
        
        transaction = db.session.query(Transaction).filter(
            Transaction.trans_id == (trans_id if(trans_id!='all') else Transaction.trans_id)
        ).all()

        if not transaction:
            return {'message':'查無此交易紀錄'}

        transaction_json = {
            'data': [record.to_json() for record in transaction],
            'title': 'transaction'
        } 
        return transaction_json
    
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('employee_id', type=str, required=True, location=['form'])
        parser.add_argument('customer_id', type=str, required=True, location=['form'])
        parser.add_argument('trans_date', type=str, required=False, location=['form'])
        req_data = parser.parse_args()
        print(req_data)
        transaction = Transaction.create(
            trans_id = str(uuid.uuid4()),
            employee_id = req_data['employee_id'],
            customer_id = req_data['customer_id'],
            trans_date = req_data['trans_date'],
            total_price = 200000
        )
        db.session.add(transaction)
        db.session.commit()
        return {'trans_id': transaction.trans_id},

    def put(self, trans_id): 
        parser = reqparse.RequestParser()
        parser.add_argument('total_price', type=int, required=True)
        req_data = parser.parse_args()

        transaction = db.session.query(Transaction).filter(
            Transaction.trans_id == trans_id
        ).first()
        if not transaction:
            return {'message': f'不存在的trans_id:{trans_id}'}
        
        transaction.total_price = req_data['total_price']
        db.session.add(transaction)
        db.session.commit()
        return 

    def delete(self, trans_id):
        transaction = db.session.query(Transaction).filter(
            Transaction.trans_id == trans_id
        ).first()
        
        if not transaction:
            return {'message': f'不存在的trans_id:{trans_id}'}

        db.session.delete(transaction)
        db.session.commit()
        return 

class RestockDataController(Resource):
    LIST_URL = '/restock_data/<supplier_id>'
    CREATE_URL = '/restock_data'

    def get(self, supplier_id):
        sku = db.session.query(
                                Sku.sku_id,
                                Product.product_name,
                                Sku.sku_code,
                                Sku.cost
                            ).join(
                                Product,
                                Sku.product_id == Product.product_id,
                                isouter = True
                            ).filter(
                                Product.supplier_id == supplier_id
                            ).all()                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
        json = {
            'data': [{   
                        'product_id': record[0],
                        'sku_id': record[1],
                        'product_name': record[2],
                        'sku_code': record[3],
                        'cost': record[4]
                    } for record in sku],
            'title': 'sku_restock'
        } 
        return  json

class RestockController(Resource):
    LIST_URL = '/restock/<restock_id>'
    CREATE_URL = '/restock'

    def get(self, restock_id):
        parser = reqparse.RequestParser()
        parser.add_argument('employee_id', type=str, required=True, location=['form'])
        parser.add_argument('customer_id', type=str, required=True, location=['form'])
        
        restock = db.session.query(
                                ReStock, 
                                Employee.employee_name,
                                Supplier.supplier_name
                            ).join(
                                Employee, 
                                ReStock.employee_id == Employee.employee_id, 
                                isouter = True
                            ).join(
                                Supplier,
                                ReStock.supplier_id == Supplier.supplier_id, 
                                isouter = True
                            ).filter(
                                ReStock.restock_id == (restock_id if(restock_id!='all') else ReStock.restock_id)
                            ).all()

        print(restock)
        if not restock:
            return {'message':'查無此交易紀錄'}

        restock_json = {
            'data': [{
                            'restock_id': record[0].restock_id,
                            'employee_id': record[0].employee_id,
                            'employee_name': record[1],
                            'supplier_id': record[0].supplier_id,
                            'supplier_name': record[2],
                            'restock_date': record[0].restock_date.strftime("%m/%d/%Y, %H:%M:%S"),
                            'total_price': record[0].total_price
                        } for record in restock],
            'title': 'restock'
        } 
        return restock_json
        return 200
    
    def post(self):
        parser = reqparse.RequestParser()
        # trans_record Tb
        parser.add_argument('employee_id', type=str, required=True, location=['form'])
        parser.add_argument('supplier_id', type=str, required=True, location=['form'])
        # parser.add_argument('restock_date', type=str, required=True, location=['form'])

        # trans_detail Tb
        parser.add_argument('sku_id[]', type=str, required=True, location=['form'], action='append')
        parser.add_argument('sale_price[]', type=int, required=True, location=['form'], action='append')
        parser.add_argument('quantity[]', type=int, required=True, location=['form'], action='append')
        parser.add_argument('memo[]', type=str, required=False, location=['form'], action='append')
        
        req_data = parser.parse_args()
        restock = ReStock.create(
            restock_id = str(uuid.uuid4()),
            employee_id = req_data['employee_id'],
            supplier_id = req_data['supplier_id'],
            restock_date = datetime.now(),
            total_price = 200000
        )
        db.session.add(restock)

        for i in range(0, len(req_data['sku_id[]'])):
            reStockDetail = ReStockDetail.create(
                restock_id = restock.restock_id,
                sku_id = req_data['sku_id[]'][i],
                serial_id = 1,
                sale_price = req_data['sale_price[]'][i],
                quantity = req_data['quantity[]'][i],
                memo = req_data['memo[]'][i]
            )          
            print(reStockDetail.to_json())
            db.session.add(reStockDetail)

        db.session.commit()
        return {'restock_id': restock.restock_id},

    def put(self, trans_id): 
        parser = reqparse.RequestParser()
        parser.add_argument('total_price', type=int, required=True)
        req_data = parser.parse_args()

        Restock = db.session.query(Restock).filter(
            Restock.trans_id == trans_id
        ).first()
        if not Restock:
            return {'message': f'不存在的trans_id:{trans_id}'}
        
        Restock.total_price = req_data['total_price']
        db.session.add(Restock)
        db.session.commit()
        return 

    def delete(self, trans_id):
        Restock = db.session.query(Restock).filter(
            Restock.trans_id == trans_id
        ).first()
        
        if not Restock:
            return {'message': f'不存在的trans_id:{trans_id}'}

        db.session.delete(Restock)
        db.session.commit()
        return 
