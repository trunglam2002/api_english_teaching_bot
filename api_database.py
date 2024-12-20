from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)

def fetch_all_data(table_name):
    conn = sqlite3.connect('english_learning.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    conn.close()
    return rows

@app.route('/api/<table_name>', methods=['GET'])
def get_table_data(table_name):
    valid_tables = ['error', 'sample_error', 'vocab', 'grammar']
    if table_name not in valid_tables:
        return jsonify({"error": "Invalid table name"}), 400

    data = fetch_all_data(table_name)
    print(type(data[0][0]))
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=6000)
