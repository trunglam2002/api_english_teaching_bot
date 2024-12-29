import sqlite3

# Hàm kết nối đến cơ sở dữ liệu
def connect_to_db(db_name):
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

# Hàm đóng kết nối
def close_connection(conn):
    """Đóng kết nối đến cơ sở dữ liệu."""
    conn.close()
    print("Kết nối đến cơ sở dữ liệu đã đóng.")

conn = connect_to_db('english_learning.db')
list_tables(conn)
show_table_structure(conn, 'error')
# view_table_data(conn, 'vocab', limit=20)
# view_table_data(conn, 'grammar', limit=20)
view_table_data(conn, 'grammar', limit=20)
# view_table_data(conn, 'sample_error', limit=20)
close_connection(conn)