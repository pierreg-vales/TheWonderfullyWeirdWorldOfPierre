from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy


app = Flask (__name__) 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///archive.db'
db = SQLAlchemy(app)

class ArchiveItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)
    item = db.Column(db.String(200), nullable=False)

@app.route("/")
def home():
    return "The Revival Has Begun"

@app.route("/me")
def me():
    items = ArchiveItem.query.all()
    result = {}
    for item in items:
        if item.category not in result:
            result[item.category] = []
        result[item.category].append(item.item)
    return jsonify(result)

@app.route("/category/<string:name>")
def category(name):
    items = ArchiveItem.query.filter_by(category=name).all()
    if not items:
        return jsonify({"message": "Category not found"}), 404
    else:
        return jsonify({name: [item.item for item in items]})
    
@app.route("/category", methods=["POST"])
def add_category():
    data = request.get_json()

    if not data or "category" not in data or "item" not in data:
        return jsonify({"message": "Invalid request, 'category' and 'item' are required."}, 400)
    
    category = data["category"]
    item = data["item"]

    new_item = ArchiveItem(category=category, item=item)
    db.session.add(new_item)
    db.session.commit()

    return jsonify({"message": f'Item added succesfully- Category: {category}, Item: {item}'}, 201)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)