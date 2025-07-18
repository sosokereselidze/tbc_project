from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length
from werkzeug.security import generate_password_hash, check_password_hash
import os
from models import db, User, Product
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your_secret_key'

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'users.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=4, max=150)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=6)])
    submit = SubmitField("Register")

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    submit = SubmitField("Login")
    
# @app.route("/")
# def home():
#     if current_user.is_authenticated:
#         if current_user.username == "sosokeres5":
#             return redirect(url_for("admin_panel"))
#         else:
#             return redirect(url_for("index"))
#     return redirect(url_for("login"))

@app.route("/")
def home():
    if current_user.is_authenticated:
        if current_user.username == "sosokeres5":
            return render_template("admin.html", name=current_user.username)
        else:
            return render_template("index.html", name=current_user.username)
    return redirect(url_for("login"))


@app.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash("Username already taken.")
            return redirect(url_for("sign_up"))

        hashed_pw = generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)  # ✅ Log in immediately after registration

        # ✅ Redirect based on user type
        if new_user.username == "sosokeres5":
            return redirect(url_for("admin_panel"))
        else:
            return redirect(url_for("index"))

    return render_template("sign-up.html", form=form)
@app.route("/index")
@login_required
def index():
    products = Product.query.all()
    return render_template("index.html", name=current_user.username, products=products)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user and check_password_hash(user.password, form.password.data):
            login_user(user)

            if user.username == "sosokeres" and form.password.data == "sosokereselidze2009":
                return redirect(url_for("admin_panel"))
            else:
                return redirect(url_for("index"))

        flash("Invalid username or password.")
    return render_template("login.html", form=form)

# @app.route("/dashboard")
# @login_required
# def dashboard():
#     return render_template("dashboard.html", name=current_user.username)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

UPLOAD_FOLDER = os.path.join(basedir, 'static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


products = []

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


@app.route("/admin", methods=["GET", "POST"])
@login_required
def admin_panel():
    if current_user.username != "sosokeres":
        flash("Unauthorized")
        return redirect(url_for("index"))

    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        image = request.files.get('image')

        if name and price and image:
            filename = secure_filename(image.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(image_path)
            image_url = url_for('static', filename=f'uploads/{filename}')

            product = Product(name=name, price=float(price), image_url=image_url)
            db.session.add(product)
            db.session.commit()
            flash("Product added successfully!")
            return redirect(url_for('admin_panel'))

    products = Product.query.all()
    return render_template("admin.html", products=products)


@app.route('/delete/<int:product_id>', methods=['POST'])
@login_required
def delete_product(product_id):
    if current_user.username != "sosokeres":
        flash("Unauthorized")
        return redirect(url_for("admin_panel"))

    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted successfully!')
    return redirect(url_for('admin_panel'))


@app.route('/edit/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if not product:
        flash("Product not found.")
        return redirect(url_for('admin_panel'))

    if request.method == 'POST':
        product['name'] = request.form['name']
        product['price'] = float(request.form['price'])

        image = request.files.get('image')
        if image and image.filename != "":
            filename = secure_filename(image.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(image_path)
            product['image_url'] = url_for('static', filename=f'uploads/{filename}')

        flash('Product updated successfully!')
        return redirect(url_for('admin_panel'))

    return render_template('edit.html', product=product)

@app.route("/wishlist")
@login_required
def wishlist_page():
    return render_template("wishlist.html", wishlist=current_user.wishlist)


@app.route("/buy/<int:product_id>", methods=["POST"])
@login_required
def buy_product(product_id):
    flash("Purchase successful (not implemented yet).")
    return redirect(url_for("index"))


@app.route("/wishlist/add/<int:product_id>", methods=["POST"])
@login_required
def add_to_wishlist(product_id):
    product = Product.query.get_or_404(product_id)
    if product not in current_user.wishlist:
        current_user.wishlist.append(product)
        db.session.commit()
        flash("Added to wishlist.")
    else:
        flash("Product already in wishlist.")
    return redirect(url_for("wishlist_page"))

@app.route("/products")
def products_page():
    products = Product.query.all()
    return render_template("products.html", products=products)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

        # Create admin user if it doesn't exist
        admin = User.query.filter_by(username="sosokeres").first()
        if not admin:
            hashed_pw = generate_password_hash("sosokereselidze2009")
            admin = User(username="sosokeres", password=hashed_pw)
            db.session.add(admin)
            db.session.commit()

    app.run(debug=True)
