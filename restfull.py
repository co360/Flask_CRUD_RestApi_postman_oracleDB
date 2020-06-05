from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='oracle://system:oracle@127.0.0.1:1521/orcl'
db = SQLAlchemy(app)


###Models####
class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20))
    productDescription = db.Column(db.String(100))
    productBrand = db.Column(db.String(20))
    price = db.Column(db.Integer)

    def create(self):
      db.session.add(self)
      db.session.commit()
      return self
    def __init__(self,id,title,productDescription,productBrand,price):
        self.id = id
        self.title = title
        self.productDescription = productDescription
        self.productBrand = productBrand
        self.price = price
    def __repr__(self):
        return '' % self.id
db.create_all()

class ProductSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Product
        sqla_session = db.session
    id = fields.Number(dump_only=True)
    title = fields.String(required=True)
    productDescription = fields.String(required=True)
    productBrand = fields.String(required=True)
    price = fields.Number(required=True)


@app.route('/products', methods = ['GET'])
def index():
    get_products = Product.query.all()
    product_schema = ProductSchema(many=True)
    products = product_schema.dump(get_products)
    return make_response(jsonify({"product": products}))


@app.route('/products', methods=['POST'])
def create_product():
    newid = request.form['ID']
    newtitle = request.form['TITLE']
    newproductDescription = request.form['productDescription']
    newproductBrand = request.form['productBrand']
    newprice = request.form['PRICE']
    user = Product(newid, newtitle, newproductDescription, newproductBrand,newprice)
    db.session.add(user)
    db.session.commit()
    return "<p>Data is updated</p>"


@app.route('/products/<id>', methods = ['DELETE'])
def delete_product_by_id(id):
    get_product = Product.query.get(id)
    db.session.delete(get_product)
    db.session.commit()
    return "<p>Data is deleted</p>"


@app.route('/products/<id>', methods = ['PUT'])
def update_product_by_id(id):
    #data = request.get_json()
    get_product = Product.query.get(id)
    if request.form['PRICE']:
        get_product.price = request.form['PRICE']
    if request.form['productDescription']:
        get_product.productDescription = request.form['productDescription']
    if request.form['productBrand']:
        get_product.productBrand = request.form['productBrand']
    if request.form['TITLE']:
        get_product.title= request.form['TITLE']
    db.session.add(get_product)
    db.session.commit()
    product_schema = ProductSchema(only=['id', 'title', 'productDescription','productBrand','price'])
    product = product_schema.dump(get_product)
    return make_response(jsonify({"product": product}))


if __name__ == '__main__':
    app.run(debug=True)




