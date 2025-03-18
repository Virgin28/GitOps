from flask import Flask, render_template, request, redirect, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import os
from flask_cors import CORS
import re
import sqlalchemy.exc
from sqlalchemy import text

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

# Database configuration
DB_USER = os.getenv('MYSQL_USER')
DB_PASSWORD = os.getenv('MYSQL_PASSWORD')
DB_HOST = os.getenv('MYSQL_HOST')
DB_NAME = os.getenv('MYSQL_DB')

# Configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True  # This will log all database operations

db = SQLAlchemy(app)

# Ensure the database exists
def init_db():
    try:
        # Create database if it doesn't exist
        engine = sqlalchemy.create_engine(f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}")
        with engine.connect() as conn:
            conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}"))
        engine.dispose()
        
        # Initialize the app's database connection
        db.create_all()
        return True
    except Exception as e:
        print(f"Database initialization error: {e}")
        return False

def sanitize_table_name(name):
    return re.sub(r'[^a-zA-Z0-9_]', '_', name)

class DynamicList():
    @staticmethod
    def get_model(table_name):
        class List(db.Model):
            __tablename__ = table_name
            __table_args__ = {'extend_existing': True}
            id = db.Column(db.Integer, primary_key=True)
            item = db.Column(db.String(255), nullable=False)
        return List

@app.before_first_request
def initialize():
    init_db()

@app.route('/')
def index():
    return send_from_directory('templates', 'index.html')

@app.route('/lists')
def lists():
    return send_from_directory('templates', 'lists.html')

@app.route('/create_list')
def create_list():
    return send_from_directory('templates', 'create_list.html')

@app.route('/list/<list_name>')
def list_page(list_name):
    return send_from_directory('templates', 'list_page.html')

@app.route('/api/create-list', methods=['POST'])
def api_create_list():
    try:
        list_name = request.json.get('list_name')
        if not list_name:
            return jsonify({'message': 'List name is required.'}), 400
        
        list_name = sanitize_table_name(list_name)
        
        # Check if table exists
        inspector = sqlalchemy.inspect(db.engine)
        if list_name in inspector.get_table_names():
            return jsonify({'message': 'List already exists.'}), 400

        # Create new table
        ListModel = DynamicList.get_model(list_name)
        db.create_all()
        
        return jsonify({'message': f'List {list_name} created successfully.'}), 201
        
    except Exception as e:
        print(f"Error creating list: {str(e)}")
        return jsonify({'message': 'Failed to create list. Database error.'}), 500

@app.route('/api/lists', methods=['GET'])
def api_lists():
    try:
        inspector = sqlalchemy.inspect(db.engine)
        tables = inspector.get_table_names()
        return jsonify({'lists': tables}), 200
    except Exception as e:
        print(f"Error getting lists: {str(e)}")
        return jsonify({'message': 'Failed to retrieve lists. Database error.'}), 500

@app.route('/api/list/<list_name>', methods=['GET', 'POST'])
def api_list_items(list_name):
    try:
        list_name = sanitize_table_name(list_name)
        ListModel = DynamicList.get_model(list_name)
        
        if request.method == 'POST':
            item = request.json.get('item')
            if not item:
                return jsonify({'message': 'Item content is required.'}), 400
            
            new_item = ListModel(item=item)
            db.session.add(new_item)
            db.session.commit()
        
        items = [(item.id, item.item) for item in ListModel.query.all()]
        return jsonify({'items': items}), 200
    except Exception as e:
        print(f"Error accessing list: {str(e)}")
        return jsonify({'message': 'Failed to access list. Database error.'}), 500

@app.route('/api/list/<list_name>/delete/<int:item_id>', methods=['DELETE'])
def api_delete_item(list_name, item_id):
    try:
        list_name = sanitize_table_name(list_name)
        ListModel = DynamicList.get_model(list_name)
        item = ListModel.query.get(item_id)
        if item:
            db.session.delete(item)
            db.session.commit()
            return jsonify({'message': 'Item done!'}), 200
        return jsonify({'message': 'Item not found.'}), 404
    except Exception as e:
        print(f"Error deleting item: {str(e)}")
        return jsonify({'message': 'Failed to delete item. Database error.'}), 500

@app.route('/api/delete-list/<list_name>', methods=['DELETE'])
def api_delete_list(list_name):
    try:
        list_name = sanitize_table_name(list_name)
        db.engine.execute(text(f"DROP TABLE IF EXISTS `{list_name}`"))
        return jsonify({'message': f'List {list_name} removed successfully.'}), 200
    except Exception as e:
        print(f"Error deleting list: {str(e)}")
        return jsonify({'message': 'Failed to delete list. Database error.'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)