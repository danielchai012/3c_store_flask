from db import db

class Category(db.Model):
    __tablename__ = 'category'
    __table_args__ = {'mysql_charset': 'utf8mb4'}

    category_id = db.Column(db.Integer, primary_key=True)
    category_code = db.Column(db.String(2), nullable=False)
    category_name = db.Column(db.String(100), nullable=False)
    category_level = db.Column(db.Integer, nullable=False)
    parent_id = db.Column(db.Integer, nullable=False)

    db_cater_product = db.relationship("Product", backref="category")

    def to_json(self):
        json = {
            'category_id': self.category_id,
            'category_code': self.category_code,
            'category_name': self.category_name,
            'category_level': self.category_level,
            'parent_id': self.parent_id
        }
        return json
