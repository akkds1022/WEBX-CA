from flask import Flask, render_template, request, redirect, url_for, flash, session
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os
from datetime import datetime
from bson import ObjectId
import bcrypt

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)

# MongoDB connection with error handling
try:
    # Create a new client and connect to the server
    client = MongoClient(
        os.getenv('MONGODB_URI'),
        server_api=ServerApi('1'),
        connectTimeoutMS=30000,  # 30 seconds
        socketTimeoutMS=45000,   # 45 seconds
        maxPoolSize=50
    )
    
    # Send a ping to confirm a successful connection
    client.admin.command('ping')
    print("Successfully connected to MongoDB!")
    
    db = client['clothing_rental']
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    raise

# Collections
users = db.users
products = db.products
rentals = db.rentals

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed)

@app.route('/')
def home():
    try:
        featured_products = list(products.find().limit(8))
        return render_template('index.html', products=featured_products)
    except Exception as e:
        flash('Error loading products', 'error')
        return render_template('index.html', products=[])

@app.route('/products')
def all_products():
    try:
        category = request.args.get('category')
        if category:
            items = list(products.find({'category': category}))
        else:
            items = list(products.find())
        return render_template('products.html', products=items)
    except Exception as e:
        flash('Error loading products', 'error')
        return render_template('products.html', products=[])

@app.route('/product/<product_id>')
def product_detail(product_id):
    try:
        product = products.find_one({'_id': ObjectId(product_id)})
        if not product:
            flash('Product not found', 'error')
            return redirect(url_for('all_products'))
        return render_template('product_detail.html', product=product)
    except Exception as e:
        flash('Error loading product details', 'error')
        return redirect(url_for('all_products'))

@app.route('/rent/<product_id>', methods=['POST'])
def rent_product(product_id):
    if 'user_id' not in session:
        flash('Please login to rent items', 'error')
        return redirect(url_for('login'))
    
    try:
        # Convert string ID to ObjectId
        product_id = ObjectId(product_id)
        product = products.find_one({'_id': product_id})
        
        if not product:
            flash('Product not found', 'error')
            return redirect(url_for('all_products'))
            
        if product['stock'] <= 0:
            flash('Item is out of stock', 'error')
            return redirect(url_for('product_detail', product_id=str(product_id)))
            
        # Create rental record
        rental = {
            'user_id': session['user_id'],
            'product_id': str(product_id),
            'rental_date': datetime.now(),
            'return_date': None,
            'status': 'active'
        }
        
        # Start a MongoDB session for transaction
        with client.start_session() as mongo_session:
            with mongo_session.start_transaction():
                # Insert rental record
                rentals.insert_one(rental, session=mongo_session)
                # Update product stock
                products.update_one(
                    {'_id': product_id},
                    {'$inc': {'stock': -1}},
                    session=mongo_session
                )
        
        flash('Item rented successfully!', 'success')
        return redirect(url_for('product_detail', product_id=str(product_id)))
        
    except Exception as e:
        print(f"Error in rent_product: {str(e)}")
        flash('An error occurred while processing your rental. Please try again.', 'error')
        return redirect(url_for('product_detail', product_id=product_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            email = request.form['email']
            password = request.form['password']
            user = users.find_one({'email': email})
            if user and check_password(password, user['password']):
                session['user_id'] = str(user['_id'])
                flash('Login successful!', 'success')
                return redirect(url_for('home'))
            else:
                flash('Invalid credentials', 'error')
        except Exception as e:
            flash('Error during login', 'error')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            user_data = {
                'name': request.form['name'],
                'email': request.form['email'],
                'password': hash_password(request.form['password']),
                'created_at': datetime.now()
            }
            # Check if email already exists
            if users.find_one({'email': user_data['email']}):
                flash('Email already registered', 'error')
                return render_template('register.html')
            
            users.insert_one(user_data)
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash('Error during registration', 'error')
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Logged out successfully', 'success')
    return redirect(url_for('home'))

@app.route('/my-rentals')
def my_rentals():
    if 'user_id' not in session:
        flash('Please login to view your rentals', 'error')
        return redirect(url_for('login'))
    
    try:
        # Get all rentals for the current user
        user_rentals = list(rentals.find({'user_id': session['user_id']}))
        
        # Get product details for each rental
        rental_items = []
        for rental in user_rentals:
            try:
                product = products.find_one({'_id': ObjectId(rental['product_id'])})
                if product:
                    rental_items.append({
                        'rental': rental,
                        'product': product
                    })
            except Exception as e:
                print(f"Error processing rental {rental['_id']}: {str(e)}")
                continue
        
        return render_template('my_rentals.html', rental_items=rental_items)
    except Exception as e:
        print(f"Error in my_rentals: {str(e)}")
        flash('Error loading your rentals', 'error')
        return redirect(url_for('home'))

@app.route('/return/<rental_id>', methods=['POST'])
def return_product(rental_id):
    if 'user_id' not in session:
        flash('Please login to return items', 'error')
        return redirect(url_for('login'))
    
    try:
        # Convert string ID to ObjectId
        rental_id = ObjectId(rental_id)
        rental = rentals.find_one({'_id': rental_id, 'user_id': session['user_id']})
        
        if not rental:
            flash('Rental not found', 'error')
            return redirect(url_for('my_rentals'))
            
        if rental['status'] != 'active':
            flash('This item has already been returned', 'error')
            return redirect(url_for('my_rentals'))
            
        # Start a MongoDB session for transaction
        with client.start_session() as mongo_session:
            with mongo_session.start_transaction():
                # Update rental status
                rentals.update_one(
                    {'_id': rental_id},
                    {
                        '$set': {
                            'status': 'returned',
                            'return_date': datetime.now()
                        }
                    },
                    session=mongo_session
                )
                # Increment product stock
                products.update_one(
                    {'_id': ObjectId(rental['product_id'])},
                    {'$inc': {'stock': 1}},
                    session=mongo_session
                )
        
        flash('Item returned successfully!', 'success')
        return redirect(url_for('my_rentals'))
        
    except Exception as e:
        print(f"Error in return_product: {str(e)}")
        flash('An error occurred while processing your return. Please try again.', 'error')
        return redirect(url_for('my_rentals'))

if __name__ == '__main__':
    app.run(debug=True) 