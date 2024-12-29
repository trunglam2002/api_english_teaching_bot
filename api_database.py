import bcrypt
from flask import Flask, jsonify, request
from database.add_data import add_default_data_for_user
import sqlite3

app = Flask(__name__)

# Hàm kết nối cơ sở dữ liệu
def connect_to_db():
    """
    Kết nối đến cơ sở dữ liệu với thời gian chờ (timeout) lâu hơn
    và cấu hình busy_timeout để giảm thiểu lỗi 'database is locked'.
    """
    conn = sqlite3.connect('english_learning.db', timeout=30)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA busy_timeout = 30000;")  # 30 giây
    return conn

# Hàm lấy toàn bộ dữ liệu từ bảng
def fetch_all_data(table_name, user_id):
    """
    Lấy toàn bộ dữ liệu từ bảng theo user_id, bỏ qua cột user_id trong kết quả.
    """
    conn = connect_to_db()
    try:
        cursor = conn.cursor()
        
        # Fetch chỉ các cột cần thiết, bỏ qua user_id
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = [row[1] for row in cursor.fetchall() if row[1] != 'user_id']
        column_list = ", ".join(columns)

        # Lấy dữ liệu từ bảng, bỏ qua cột user_id
        query = f"SELECT {column_list} FROM {table_name} WHERE user_id = ?"
        cursor.execute(query, (user_id,))
        rows = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Lỗi khi lấy dữ liệu từ bảng {table_name}: {e}")
        rows = []
    finally:
        conn.close()
    return rows

@app.route('/api/<table_name>', methods=['GET'])
def get_table_data(table_name):
    """
    API lấy dữ liệu từ bảng theo user_id.
    """
    valid_tables = ['error', 'sample_error', 'vocab', 'grammar']
    if table_name not in valid_tables:
        return jsonify({"error": "Invalid table name"}), 400

    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"error": "Missing user_id parameter."}), 400

    try:
        user_id = int(user_id)
        data = fetch_all_data(table_name, user_id)
        return jsonify(data)
    except ValueError:
        return jsonify({"error": "Invalid user_id parameter."}), 400

@app.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')
        age = data.get('age')

        if not username or not password or not age:
            return jsonify({"error": "Username, password, and age are required."}), 400

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # 1) Mở kết nối 1 lần
        conn = connect_to_db()
        cursor = conn.cursor()

        # 2) Insert user
        cursor.execute('''
            INSERT INTO users (username, password, age)
            VALUES (?, ?, ?)
        ''', (username, hashed_password, age))
        user_id = cursor.lastrowid

        # 3) Thêm dữ liệu mặc định, dùng cùng 'conn' hoặc 'cursor'
        add_default_data_for_user(user_id, cursor)

        conn.commit()
        conn.close()

        return jsonify({"message": "User registered successfully.", "user_id": user_id}), 201

    except sqlite3.IntegrityError:
        return jsonify({"error": "Username already exists."}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/login', methods=['POST'])
def login():
    """
    API xử lý đăng nhập và trả về user_id nếu thông tin đăng nhập hợp lệ.
    """
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({"error": "Username and password are required."}), 400

        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, password FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()

        if not user:
            return jsonify({"error": "Invalid username or password."}), 400

        user_id, hashed_password = user

        if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
            return jsonify({"user_id": user_id}), 200
        else:
            return jsonify({"error": "Invalid username or password."}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=6000)
