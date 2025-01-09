from flask import Flask, render_template, request, redirect, jsonify, send_from_directory
import mysql.connector
import os
from flask_cors import CORS
import re

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST", "db"),
            user=os.getenv("MYSQL_USER", "root"),
            password=os.getenv("MYSQL_PASSWORD", "root"),
            database=os.getenv("MYSQL_DB", "startdoing")
        )
        return conn
    except mysql.connector.Error as e:
        print(f"Error connecting to database: {e}")
        return None

def sanitize_table_name(name):
    return re.sub(r'[^a-zA-Z0-9_]', '_', name)

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
        conn = get_db_connection()
        if not conn:
            return jsonify({'message': 'Database connection failed.'}), 500

        cursor = conn.cursor()
        
        # First check if table exists
        cursor.execute(f"SHOW TABLES LIKE '{list_name}'")
        if cursor.fetchone():
            cursor.close()
            conn.close()
            return jsonify({'message': 'List already exists.'}), 400

        # Create the table with proper structure
        cursor.execute(f"""
            CREATE TABLE `{list_name}` (
                id INT AUTO_INCREMENT PRIMARY KEY,
                item VARCHAR(255) NOT NULL
            )
        """)
        
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': f'List {list_name} created successfully.'}), 201
        
    except Exception as e:
        print(f"Error creating list: {e}")
        return jsonify({'message': f'Error creating list: {str(e)}'}), 500

@app.route('/api/lists', methods=['GET'])
def api_lists():
    conn = get_db_connection()
    if not conn:
        return jsonify({'message': 'Database connection failed.'}), 500

    cursor = conn.cursor()
    cursor.execute("SHOW TABLES")
    tables = [table[0] for table in cursor.fetchall()]
    cursor.close()
    conn.close()
    return jsonify({'lists': tables}), 200

@app.route('/api/list/<list_name>', methods=['GET', 'POST'])
def api_list_items(list_name):
    try:
        list_name = sanitize_table_name(list_name)
        conn = get_db_connection()
        if not conn:
            return jsonify({'message': 'Database connection failed.'}), 500

        cursor = conn.cursor()
        
        if request.method == 'POST':
            item = request.json.get('item')
            cursor.execute(f"INSERT INTO `{list_name}` (item) VALUES (%s)", (item,))
            conn.commit()
        
        cursor.execute(f"SELECT * FROM `{list_name}`")
        items = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify({'items': items}), 200
    except Exception as e:
        print(f"Error accessing list: {e}")
        return jsonify({'message': f'Error accessing list: {str(e)}'}), 500

@app.route('/api/list/<list_name>/delete/<int:item_id>', methods=['DELETE'])
def api_delete_item(list_name, item_id):
    try:
        list_name = sanitize_table_name(list_name)
        conn = get_db_connection()
        if not conn:
            return jsonify({'message': 'Database connection failed.'}), 500

        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM `{list_name}` WHERE id = %s", (item_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Item done!'}), 200
    except Exception as e:
        print(f"Error deleting item: {e}")
        return jsonify({'message': f'Error deleting item: {str(e)}'}), 500

@app.route('/api/delete-list/<list_name>', methods=['DELETE'])
def api_delete_list(list_name):
    try:
        list_name = sanitize_table_name(list_name)
        conn = get_db_connection()
        if not conn:
            return jsonify({'message': 'Database connection failed.'}), 500

        cursor = conn.cursor()
        cursor.execute(f"DROP TABLE IF EXISTS `{list_name}`")
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': f'List {list_name} removed successfully.'}), 200
    except Exception as e:
        print(f"Error deleting list: {e}")
        return jsonify({'message': f'Error deleting list: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)