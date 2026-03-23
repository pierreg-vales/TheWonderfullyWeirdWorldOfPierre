from flask import Flask, jsonify, request, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask (__name__) 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.dirname(__file__), 'instance', 'archive.db')
db = SQLAlchemy(app)

class ArchiveItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)
    item = db.Column(db.String(200), nullable=False)

@app.route("/")
def home():
    return send_from_directory("static", "index.html")

@app.route("/me")
def me():
    items = ArchiveItem.query.all()
    result = {}
    for item in items:
        if item.category not in result:
            result[item.category] = []
        result[item.category].append({"id": item.id, "item": item.item})
    return jsonify(result)

@app.route("/category/<string:name>")
def category(name):
    items = ArchiveItem.query.filter_by(category=name).all()
    if not items:
        return jsonify({"message": "Category not found"}), 404
    else:
        item_list = [{"id": item.id, "item": item.item} for item in items]
        return jsonify({name: item_list})
    
@app.route("/category", methods=["POST"])
def add_category():
    data = request.get_json()

    if not data or "category" not in data or "item" not in data:
        return jsonify({"message": "Invalid request, 'category' and 'item' are required."}, 400)
    
    category = data["category"].strip()
    item = data["item"].strip()

    new_item = ArchiveItem(category=category, item=item)
    db.session.add(new_item)
    db.session.commit()

    return jsonify({"message": f'Item added succesfully- Category: {category}, Item: {item}'}, 201)

@app.route("/item/<int:item_id>", methods=["PUT"])
def update_item(item_id):
    data = request.get_json()
    item = ArchiveItem.query.get(item_id)

    if not item:
        return jsonify({"message": "Item not found"}), 404
    
    if "item" in data:
        item.item = data["item"]
    if "category" in data:
        item.category = data["category"]

    db.session.commit()

    return jsonify({"message": "Item updated successfully", "item": {"id": item.id, "category": item.category, "item": item.item}})
    
@app.route("/item/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    item = ArchiveItem.query.get(item_id)

    if not item:
        return jsonify({"message": "Item not found"}), 404
    
    db.session.delete(item)
    db.session.commit()

    return jsonify({"message": "Item deleted successfully"})

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=False)