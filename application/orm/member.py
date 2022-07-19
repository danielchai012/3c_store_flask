from db import db


class Customer(db.Model):
    __tablename__ = 'customer'
    __table_args__ = {'mysql_charset': 'utf8mb4'}

    customer_id = db.Column(db.String(7), primary_key=True)
    customer_name = db.Column(db.String(20), nullable=False)
    customer_gender = db.Column(db.String(1), nullable=False)
    customer_phone = db.Column(db.String(20), nullable=False)
    customer_address = db.Column(db.String(50), nullable=False)
    join_time = db.Column(db.DateTime(), nullable=False)
    update_time = db.Column(db.DateTime(), nullable=False)

    @classmethod 
    def create(cls, customer_id, customer_name, customer_gender, customer_phone, customer_address, join_time, update_time):
        customer = Customer()
        customer.customer_id = customer_id
        customer.customer_name = customer_name
        customer.customer_gender = customer_gender
        customer.customer_phone = customer_phone
        customer.customer_address = customer_address
        customer.join_time = join_time
        customer.update_time = update_time
        return customer

    def to_json(self):
        json = {
            'customer_id': self.customer_id,
            'customer_name': self.customer_name,
            'customer_gender': self.customer_gender,
            'customer_phone': self.customer_phonetrans_date,
            'customer_address': self.customer_address,
            'customer_join_time': self.join_time.strftime("%m/%d/%Y, %H:%M:%S"),
            'customer_update_time': self.update_time.strftime("%m/%d/%Y, %H:%M:%S")
        }
        return json

class Employee(db.Model):
    __tablename__ = 'employee'
    __table_args__ = {'mysql_charset': 'utf8mb4'}

    employee_id = db.Column(db.String(7), primary_key=True)
    employee_name = db.Column(db.String(20), nullable=False)
    employee_gender = db.Column(db.String(1), nullable=False)
    employee_phone = db.Column(db.String(20), nullable=False)
    employee_address = db.Column(db.String(50), nullable=False)
    join_time = db.Column(db.DateTime(), nullable=False)
    update_time = db.Column(db.DateTime(), nullable=False)


    @classmethod 
    def create(cls, employee_id, employee_name, employee_gender, employee_phone, employee_address, join_time, update_time):
        employee = Employee()
        employee.employee_id = employee_id
        employee.employee_name = employee_name
        employee.employee_gender = employee_gender
        employee.employee_phone = employee_phone
        employee.employee_address = employee_address
        employee.join_time = join_time
        employee.update_time = update_time
        return employee

    def to_json(self):
        json = {
            'employee_id': self.employee_id,
            'employee_name': self.employee_name,
            'employee_gender': self.employee_gender,
            'employee_phone': self.employee_phone,
            'employee_address': self.employee_address,
            'join_time': self.join_time.strftime("%m/%d/%Y, %H:%M:%S"),
            'update_time': self.update_time.strftime("%m/%d/%Y, %H:%M:%S")
        }
        return json

class Supplier(db.Model):
    __tablename__ = 'supplier'
    __table_args__ = {'mysql_charset': 'utf8mb4'}

    supplier_id = db.Column(db.Integer, primary_key=True)
    supplier_name = db.Column(db.String(40), nullable=False)
    contact_num = db.Column(db.String(10), nullable=False)
    create_time = db.Column(db.DateTime(), nullable=False)
    last_instock_time = db.Column(db.DateTime(), nullable=False)

# class ReStockDetail(db.Model):
#     __tablename__ = 'restock_detail'
#     __table_args__ = {'mysql_charset': 'utf8mb4'}

#     restock_id = db.Column(db.String(36), primary_key=True)
#     sku_id = db.Column(db.String(11), primary_key=True, nullable=False)
#     serial_id = db.Column(db.String(128), nullable=True)
#     sale_price = db.Column(db.Integer, nullable=False)
#     quantity = db.Column(db.Integer, nullable=False)
#     memo = db.Column(db.String(300), nullable=True)

#     @classmethod 
#     def create(cls, restock_id, sku_id, serial_id, sale_price, quantity, memo):
#         restock_detail = ReStockDetail()
#         restock_detail.restock_id = restock_id
#         restock_detail.sku_id = sku_id
#         restock_detail.serial_id = serial_id
#         restock_detail.sale_price = sale_price
#         restock_detail.quantity = quantity
#         restock_detail.memo = memo
#         return restock_detail

#     def to_json(self):
#         json = {
#             'restock_id': self.restock_id,
#             'sku_id': self.sku_id,
#             'serial_id': self.serial_id,
#             'sale_price': self.sale_price,
#             'quantity': self.sale_quantity,
#             'memo': self.memo
#         }
#         return json