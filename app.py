from flask import Flask, render_template , request , redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///course.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.app_context().push()

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    text = db.Column(db.Text, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    isActive = db.Column(db.Boolean, default=True)

@app.route('/')
def index():
    products = Product.query.order_by(Product.price).all()
    return render_template('index.html', products=products)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/<int:id>')
def course(id):
    article = Product.query.get_or_404(id)
    try:
        db.session.delete(article)
        db.session.commit()
        return redirect("/")
    except:
        return "Ошибка удаления"

@app.route('/contacts')
def contacts():
    return render_template('contacts.html')

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        price = request.form['price']
        text = request.form['text']

        product = Product(title=title, price=price, text=text)

        try:
            db.session.add(product)
            db.session.commit()
            return redirect('/')
        except:
            return "Error"
    else:
        return render_template('create.html')


if __name__ == '__main__':
    app.run()
