# from flask import Blueprint, render_template, redirect, url_for, flash
# from flask_login import login_user, login_required, logout_user, current_user
# from app import db
# from app.models import User, Product
# from app.forms import RegistrationForm, LoginForm

# # Main Blueprint
# main = Blueprint('main', __name__)

# @main.route('/')
# def home():
#     return render_template('index.html')

# # Auth Blueprint
# auth = Blueprint('auth', __name__)

# @auth.route('/sign-up', methods=['GET', 'POST'])
# def sign_up():
#     form = RegistrationForm()
#     if form.validate_on_submit():
#         # ... registration logic ...
#         return render_template('sign-up.html', form=form)

# @auth.route('/login', methods=['GET', 'POST'])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         # ... login logic ...
#         return render_template('login.html', form=form)

# @auth.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     return redirect(url_for('auth.login'))

# # Admin Blueprint
# admin = Blueprint('admin', __name__)

# @admin.route('/admin-login', methods=['GET', 'POST'])
# def admin_login():
#     # ... admin login logic ...
#     return render_template('admin-login.html')

# @admin.route('/admin', methods=['GET', 'POST'])
# def admin_panel():
#     # ... admin panel logic ...
#     return render_template('admin-panel.html', products=products)

# @admin.route('/delete-product/<int:product_id>', methods=['POST'])
# def delete_product(product_id):
#     # ... delete product logic ...
#     return redirect(url_for('admin.admin_panel'))

# # Products Blueprint
# products = Blueprint('products', __name__)

# @products.route('/products')
# def show_products():
#     all_products = Product.query.all()
#     return render_template('products.html', products=all_products)

# @products.route('/dashboard')
# @login_required
# def dashboard():
#     user_data = {
#         'username': current_user.username,
#         # Add other user properties if available
#         # 'email': current_user.email,
#         # 'join_date': current_user.date_created
#     }
#     return render_template('dashboard.html', name=current_user.username)