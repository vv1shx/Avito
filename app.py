from flask import Flask, request, jsonify
from database import db
from models import User, Advertisement, Cart, Chat, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/avito_clone.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Привязываем базу к приложению
db.init_app(app)

# Создаем таблицы при первом запуске
with app.app_context():
    db.create_all()

# --- CRUD ДЛЯ ОБЪЯВЛЕНИЙ ---

@app.route('/ads', methods=['POST'])
def create_ad():
    data = request.form
    new_ad = Advertisement(
        title=data['title'],
        body=data.get('body'),
        price=data.get('price'),
        user_id=data['user_id'],
        photo=data['photo']
    )
    db.session.add(new_ad)
    db.session.commit()
    return jsonify({"message": "Created", "id": new_ad.id}), 201

@app.route('/ads', methods=['GET'])
def get_ads():
    ads = Advertisement.query.all()
    return jsonify([{
        "id": a.id, 
        "title": a.title, 
        "price": a.price, 
        "author_id": a.user_id,
        "photo": a.photo
    } for a in ads])

@app.route('/ads/<int:id>', methods=['GET'])
def get_one_ad(id):
    ad = Advertisement.query.get_or_404(id)
    return jsonify({"id": ad.id, "title": ad.title, "body": ad.body})

@app.route('/ads/<int:id>', methods=['PUT'])
def update_ad(id):
    ad = Advertisement.query.get_or_404(id)
    data = request.form
    ad.title = data.get('title', ad.title)
    ad.price = data.get('price', ad.price)
    db.session.commit()
    return jsonify({"message": "Updated"})

@app.route('/ads/<int:id>', methods=['DELETE'])
def delete_ad(id):
    ad = Advertisement.query.get_or_404(id)
    db.session.delete(ad)
    db.session.commit()
    return jsonify({"message": "Deleted"})

# --- ВСПОМОГАТЕЛЬНЫЕ ОПЕРАЦИИ (Корзина и Юзеры) ---

@app.route('/users', methods=['POST'])
def create_user():
    data = request.form
    user = User(username=data['username'], role=data.get('role', 'member'))
    db.session.add(user)
    db.session.commit()
    return jsonify({"id": user.id})

@app.route('/cart/add', methods=['POST'])
def add_to_cart():
    data = request.form
    item = Cart(user_id=data['user_id'], advertisement_id=data['ad_id'])
    db.session.add(item)
    db.session.commit()
    return jsonify({"message": "Added to cart"})




if __name__ == '__main__':
    app.run(debug=True)