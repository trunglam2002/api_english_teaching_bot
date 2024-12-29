import sqlite3

# Hàm kết nối đến cơ sở dữ liệu
def connect_to_db(db_name='english_learning.db'):
    """Kết nối đến cơ sở dữ liệu SQLite."""
    return sqlite3.connect(db_name)

# Hàm liệt kê tất cả các bảng
def list_tables(conn):
    """Liệt kê tất cả các bảng trong cơ sở dữ liệu."""
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("Danh sách các bảng:")
    for table in tables:
        print(table[0])

# Hàm kiểm tra cấu trúc của một bảng
def show_table_structure(conn, table_name):
    """Hiển thị cấu trúc của một bảng."""
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name});")
    structure = cursor.fetchall()
    print(f"Cấu trúc bảng {table_name}:")
    for column in structure:
        print(f"- Cột: {column[1]}, Kiểu dữ liệu: {column[2]}, Có NULL: {column[3]}, Khóa chính: {column[5]}")

# Hàm hiển thị dữ liệu từ một bảng
def view_table_data(conn, table_name, limit=10):
    """Hiển thị dữ liệu từ một bảng."""
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name} LIMIT {limit};")
    rows = cursor.fetchall()
    print(f"Dữ liệu từ bảng {table_name} (tối đa {limit} dòng):")
    for row in rows:
        print(row)

# Hàm thêm dữ liệu vào một bảng
def insert_data(conn, table_name, data):
    """Thêm dữ liệu vào bảng cụ thể."""
    cursor = conn.cursor()
    placeholders = ', '.join(['?'] * len(data[0]))
    query = f"INSERT INTO {table_name} VALUES ({placeholders});"
    try:
        cursor.executemany(query, data)
        conn.commit()
        print(f"Đã thêm dữ liệu vào bảng {table_name} thành công.")
    except sqlite3.Error as e:
        print(f"Lỗi khi thêm dữ liệu vào bảng {table_name}: {e}")

# Hàm cập nhật dữ liệu trong một bảng
def update_data(conn, table_name, column, value, condition):
    """Cập nhật dữ liệu trong bảng."""
    cursor = conn.cursor()
    query = f"UPDATE {table_name} SET {column} = ? WHERE {condition};"
    try:
        cursor.execute(query, (value,))
        conn.commit()
        print(f"Đã cập nhật dữ liệu trong bảng {table_name} thành công.")
    except sqlite3.Error as e:
        print(f"Lỗi khi cập nhật dữ liệu trong bảng {table_name}: {e}")

# Hàm xóa dữ liệu từ một bảng
def delete_data(conn, table_name, condition):
    """Xóa dữ liệu khỏi bảng cụ thể."""
    cursor = conn.cursor()
    query = f"DELETE FROM {table_name} WHERE {condition};"
    try:
        cursor.execute(query)
        conn.commit()
        print(f"Đã xóa dữ liệu từ bảng {table_name} thành công.")
    except sqlite3.Error as e:
        print(f"Lỗi khi xóa dữ liệu từ bảng {table_name}: {e}")

# Hàm đóng kết nối
def close_connection(conn):
    """Đóng kết nối đến cơ sở dữ liệu."""
    conn.close()
    print("Kết nối đến cơ sở dữ liệu đã đóng.")

# Hàm lấy danh sách lỗi mẫu theo user_id
def get_errors(conn, user_id):
    """
    Lấy danh sách các lỗi mẫu từ bảng sample_error theo user_id.

    Parameters:
        user_id (int): ID của người dùng.

    Returns:
        list: Danh sách các lỗi mẫu (example, fix, correct, incorrect).
    """
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT example, fix, correct, incorrect FROM sample_error WHERE user_id = ?", (user_id,))
        results = cursor.fetchall()
        return [{"example": row[0], "fix": row[1], "correct": row[2], "incorrect": row[3]} for row in results]
    except sqlite3.Error as e:
        print(f"Lỗi khi truy vấn bảng sample_error: {e}")
        return []

# Sử dụng các hàm
if __name__ == "__main__":
    conn = connect_to_db()

    # Liệt kê các bảng
    list_tables(conn)

    # Hiển thị cấu trúc bảng 'error'
    show_table_structure(conn, 'users')

    # Hiển thị dữ liệu từ bảng 'grammar'
    view_table_data(conn, 'grammar', limit=20)

    # Lấy danh sách lỗi theo user_id
    user_id = 1  # Thay đổi theo ID người dùng
    errors = get_errors(conn, user_id)
    print("Danh sách lỗi mẫu:", errors)

    # Đóng kết nối
    close_connection(conn)