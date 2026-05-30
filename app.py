

from flask import Flask, render_template, request, redirect, url_for, session
from products import products
import os
from try_on import virtual_tryon

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Ensure the uploads directory exists
if not os.path.exists('uploads'):
    os.makedirs('uploads')

uploads_dir = os.path.join('static', 'uploads')
if not os.path.exists(uploads_dir):
    os.makedirs(uploads_dir)

# Home Page
@app.route('/')
def home():
    return render_template('home.html')

# Shop Page
@app.route('/shop/<gender>')
def shop(gender):
    selected_products = [p for p in products if p['gender'] == gender]
    return render_template('shop.html', products=selected_products, gender=gender)

# Cart Page
@app.route('/cart')
def cart():
    cart_items = session.get('cart', [])
    return render_template('cart.html', cart_items=cart_items)

# Add to Cart
@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    product = next(p for p in products if p['id'] == product_id)
    cart = session.get('cart', [])
    cart.append(product)
    session['cart'] = cart
    return redirect(url_for('cart'))

@app.route('/try_on/<int:product_id>', methods=['GET', 'POST'])
def try_on(product_id):
    product = next((item for item in products if item['id'] == product_id), None)
    
    if product:
        gender = product['gender']
        product_image = product['image']
    else:
        return "Product not found", 404

    person_image_path = None

    if request.method == 'POST':
        person_image = request.files['personImage']
        cloth_image_path = os.path.join('static/images', product_image)

        # Save the person image to a temporary location
        person_image_path = os.path.join('static/uploads', person_image.filename)
        person_image.save(person_image_path)

        # Log person image size
        from PIL import Image
        person_img = Image.open(person_image_path)
        print(f"Person image size: {person_img.size}")

        # Perform the virtual try-on
        output_image_path = 'static/results/output_try_on.png'
        virtual_tryon(person_image_path, cloth_image_path, output_image_path)

        if os.path.exists(output_image_path):
            print(f"Output image exists at: {output_image_path}")
        else:
            print("Output image not found.")

        return render_template('try_on.html', result_image='results/output_try_on.png', 
                               product_image=product_image, person_image_path=person_image.filename, gender=gender)

    return render_template('try_on.html', product_image=product_image, gender=gender)

# About Us Page
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/remove_from_cart/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    cart = session.get('cart', [])
    cart = [item for item in cart if item['id'] != product_id]
    session['cart'] = cart
    return redirect(url_for('cart'))

@app.route('/clear_cart', methods=['POST'])
def clear_cart():
    session['cart'] = []
    return redirect(url_for('cart'))

# Route to serve the payment page
@app.route('/payment_gateway')
def payment_gateway():
    return render_template('payment-gateway-integration/index.html')

@app.route('/payment')
def payment():
    return render_template('Payment-Gateway-Integration/paymentPage.html')

@app.route('/success')
def success():
    return render_template('Payment-Gateway-Integration/successPage.html')

@app.route('/payment_success')
def payment_success():
    return "Thank you for your purchase! Your payment was successful."

if __name__ == '__main__':
    app.run(debug=True)
