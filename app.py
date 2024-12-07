from flask import Flask, request, jsonify, session
from werkzeug.utils import secure_filename
import requests

import os
import hashlib

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with a real secret key
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Mock databases
users = {
    'farmer': {},
    'consumer': {}
}
products = []
orders = {
    '1': 'Delivered',
    '2': 'In Transit',
    '3': 'Pending',
}
cart = []

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    user_type = data.get('user_type')

    if user_type not in ['farmer', 'consumer']:
        return jsonify({'error': 'Invalid user type'})

    if username in users[user_type]:
        return jsonify({'error': 'User already exists'})

    users[user_type][username] = hash_password(password)
    return jsonify({'message': 'Registration successful'})

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    user_type = data.get('user_type')

    if user_type not in ['farmer', 'consumer']:
        return jsonify({'error': 'Invalid user type'}), 400

    if username not in users[user_type]:
        return jsonify({'error': 'User not found'}), 404

    if users[user_type][username] != hash_password(password):
        return jsonify({'error': 'Invalid password'}), 401

    session['user'] = {'username': username, 'user_type': user_type}
    return jsonify({'message': 'Login successful'})


@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user', None)
    return jsonify({'message': 'Logged out successfully'})

@app.route('/upload_product', methods=['POST'])
def upload_product():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    name = request.form.get('name')
    description = request.form.get('description')
    price = float(request.form.get('price', 0))
    products.append({'name': name, 'description': description, 'price': price, 'image': filename})
    return jsonify({'message': 'Product uploaded successfully'})

@app.route('/track_order', methods=['GET'])
def track_order():
    order_id = request.args.get('order_id')
    status = orders.get(order_id, 'Order ID not found')
    return jsonify({'status': status})

@app.route('/products', methods=['GET'])
def get_products():
    return jsonify(products)

@app.route('/checkout', methods=['POST'])
def place_order():
    data = request.json
    cart_items = data.get('cart_items')
    payment_method = data.get('payment_method')

    if not cart_items or len(cart_items) == 0:
        return jsonify({'error': 'Cart is empty'}), 400

    # Mock response for successful checkout
    print(f"Cart Items: {cart_items}")
    print(f"Payment Method: {payment_method}")
    
    # You can process the payment and order here.
    # For now, just return a success message.
    return jsonify({'message': 'Checkout successful'})


@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    data = request.json
    product = data.get('product')
    cart.append(product)
    return jsonify({'message': 'Product added to cart'})

@app.route('/get_cart', methods=['GET'])
def get_cart():
    return jsonify(cart)

if __name__ == '__main__':
    app.run(debug=True)
