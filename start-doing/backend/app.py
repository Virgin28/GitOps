from flask import Flask, render_template, request, redirect, jsonify
import mysql.connector
import os
from flask_cors import CORS
import re

app = Flask(__name__)
CORS(app)

# Database connection
def get_db_connection():
    conn = mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "db"),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", "root"),
        database=os.getenv("MYSQL_DB", "startdoing")
    )
    return conn

# Sanitize table names
def sanitize_table_name(name):
    return re.sub(r'[^a-zA-Z0-9_]', '_', name)  # Replace invalid characters with underscores

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/lists', methods=['GET'])
def api_lists():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES")
    tables = [table[0] for table in cursor.fetchall()]
    cursor.close()
    conn.close()

    if not tables:
        return jsonify({'message': "No lists found."}), 404
    
    return jsonify({'lists': tables}), 200

@app.route('/api/create-list', methods=['POST'])
def api_create_list():
    list_name = request.json.get('list_name')
    if not list_name:
        return jsonify({'message': 'List name is required.'}), 400
    
    list_name = sanitize_table_name(list_name)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"CREATE TABLE IF NOT EXISTS `{list_name}` (id INT AUTO_INCREMENT PRIMARY KEY, item VARCHAR(255))")
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': f'List {list_name} created successfully.'}), 201

@app.route('/api/list/exists/<list_name>', methods=['GET'])
def api_list_exists(list_name):
    list_name = sanitize_table_name(list_name)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES LIKE %s", (list_name,))
    table = cursor.fetchone()
    cursor.close()
    conn.close()
    return jsonify({'exists': bool(table)}), 200

@app.route('/api/list/<list_name>', methods=['GET', 'POST'])
def api_list_items(list_name):
    list_name = sanitize_table_name(list_name)
    conn = get_db_connection()
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

@app.route('/api/list/<list_name>/delete/<int:item_id>', methods=['DELETE'])
def api_delete_item(list_name, item_id):
    list_name = sanitize_table_name(list_name)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM `{list_name}` WHERE id = %s", (item_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': f'Item {item_id} deleted successfully.'}), 200

@app.route('/api/delete-list/<list_name>', methods=['DELETE'])
def api_delete_list(list_name):
    list_name = sanitize_table_name(list_name)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"DROP TABLE IF EXISTS `{list_name}`")
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': f'List {list_name} deleted successfully.'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
