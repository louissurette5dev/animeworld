from flask import Flask, render_template, request, jsonify

from dataclasses import dataclass

from flask_sqlalchemy import SQLAlchemy

import os
from dotenv import load_dotenv


"""
pip install Flask
pip install Flask-SQLAlchemy
pip install psycopg2-binary


"""
load_dotenv()

app = Flask( __name__ )
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# DataClass
@dataclass
class Product ( db.Model) :
    __tablename__ = 'Product'

    # Python datatypes
    id : int
    name : str
    description : str
    image : str
    price : float
    stockAvailable : int

    # SQL/Postgres datatypes
    id = db.Column( db.Integer(), primary_key=True )
    name = db.Column( db.String(200) )
    description = db.Column( db.String(2000) )
    image = db.Column( db.String(500) )
    price = db.Column( db.Float() )
    stockAvailable = db.Column( db.Integer() )

# DataClass
@dataclass
class Order ( db.Model) :
    __tablename__ = 'Order'

    # Python datatypes
    id : int
    shippingAddress : str
    city : str
    country : str
    region : str
    productOrdered : int
    totalCost : float

    # SQL/Postgres datatypes
    id = db.Column( db.Integer(), primary_key=True )
    shippingAddress = db.Column( db.String(2000) )
    city = db.Column( db.String(200) )
    country = db.Column( db.String(200) )
    region = db.Column( db.String(200) )
    productOrdered = db.Column( db.Integer() )
    totalCost = db.Column( db.Float() )

# DataClass
@dataclass
class Message ( db.Model) :
    __tablename__ = 'Message'

    # Python datatypes
    id : int
    name : str
    email : str
    phoneNumber : str
    message : str

    # SQL/Postgres datatypes
    id = db.Column( db.Integer(), primary_key=True )
    name = db.Column( db.String(200) )
    email = db.Column( db.String(200) )
    phoneNumber = db.Column( db.String(20) )
    message = db.Column( db.String(2000) )
    

@app.route( '/index' )
def index_route() :
    # retrieve product info here
    allProducts = Product.query.order_by(Product.id).all()
    
    product_id_list = []
    product_name_list = []
    product_image_list = []
    product_price_list = []
    product_stock_list = []
    
    for item in allProducts :
        #print( item.id, item.name )
        product_id_list.append( item.id )
        product_name_list.append( item.name )
        product_image_list.append( item.image )
        product_price_list.append( item.price )
        product_stock_list.append( item.stockAvailable )
        
    # DEBUG
    print( 'id list:', product_id_list )
    print( 'name list:', product_name_list )
    print( 'name list:', product_name_list )
    
    product_list_len = len( product_id_list )
    
    return render_template( 'index.html', productLength=product_list_len, productsByID=product_id_list, productsByName=product_name_list, productsByImage=product_image_list, productsByPrice=product_price_list , productsByAvailableStock=product_stock_list)

@app.route( '/' )
def default_route() :
    #return 'success'
    
    # retrieve product info here
    allProducts = Product.query.all()
    
    product_id_list = []
    product_name_list = []
    product_image_list = []
    product_price_list = []
    
    for item in allProducts :
        #print( item.id, item.name )
        product_id_list.append( item.id )
        product_name_list.append( item.name )
        product_image_list.append( item.image )
        product_price_list.append( item.price )
        
    # DEBUG
    print( 'id list:', product_id_list )
    print( 'name list:', product_name_list )
    print( 'name list:', product_name_list )
    
    product_list_len = len( product_id_list )
    
    # pass product info to orderform below
    return render_template('orderform.html', productLength=product_list_len, productsByID=product_id_list, productsByName=product_name_list, productsByImage=product_image_list, productByPrice=product_price_list )


# http://127.0.0.1:5055/product/list
@app.route('/product/list')
def list_products() :
    allProducts = Product.query.all()
    
    # DEBUG
    print( allProducts) 
    
    return allProducts


# http://127.0.0.1:5055/order/list
@app.route('/order/list')
def list_orders() :
    allOrders = Order.query.all()
    
    # DEBUG
    print( allOrders) 
    
    return allOrders

# http://127.0.0.1:5055/message/list
@app.route('/message/list')
def list_messages() :
    allMessage = Message.query.all()
    
    # DEBUG
    print( allMessage) 
    
    return allMessage


# http://127.0.0.1:5055/order/insert
@app.route( '/order/insert', methods=['POST'])
def insert_order() :
    shipping_address_val = request.form['shippingAddress']
    city_val = request.form['city']
    country_val = request.form['country']
    region_val = request.form['region']
    product_ordered_val = request.form['productOrdered']
    
    product_orderd_id = int( product_ordered_val )
    query = db.session.query(Product)
    query = query.filter(Product.id==product_orderd_id)
    
    product_found = query.first()
    
    print( product_found, product_found.price )
    total_price = 0
    region = int( region_val )
    if region == 1 :
        print( 'North America')
        total_price = product_found.price + 5
    elif region == 2 :
        print( 'Central America') 
        total_price = product_found.price + 7
    elif region == 3 :
        print( 'Asia' )
        total_price = product_found.price + 7
    elif region == 4 :
        print( 'EU' )
        total_price = product_found.price + 10
    else :
        # error
        print( 'ERROR - region does not exist' )
        total_price = 0

    newOrder = Order(shippingAddress=shipping_address_val, city=city_val, country=country_val, region=region_val, productOrdered=product_ordered_val, totalCost=total_price )

    db.session.add( newOrder )
    product_found.stockAvailable = product_found.stockAvailable - 1
    db.session.commit()
    db.session.flush()
    
    #return 'success'
    
    message = 'You have ordered ' + product_found.name + ' for a total cost of ' + str(total_price)
    print( message )
    return message


# http://127.0.0.1:5055/message/insert
@app.route( '/message/insert', methods=['POST'])
def insert_message():
    name_val = request.form['name']
    email_val = request.form['email']
    phone_val = request.form['phone']
    message_val = request.form['message']

    newmsg = Message(name=name_val, email=email_val, phoneNumber=phone_val, message=message_val)

    db.session.add( newmsg )
    db.session.commit()
    db.session.flush()
    
    messagea = 'Your message has been received. We will contact you soon. Thank you for reaching out to us.'
    print( messagea )
    return messagea


if __name__ == '__main__' :
    app.run( debug=True, port=5055 )

