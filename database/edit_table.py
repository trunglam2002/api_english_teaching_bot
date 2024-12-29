import sqlite3

def connect(db_path='english_learning.db'):
    """
    Kết nối tới cơ sở dữ liệu SQLite.
    :param db_path: Đường dẫn tới file cơ sở dữ liệu SQLite.
    :return: Kết nối và con trỏ (cursor) tới cơ sở dữ liệu.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    return conn, cursor

def disconnect(conn):
    """
    Ngắt kết nối cơ sở dữ liệu.
    :param conn: Đối tượng kết nối.
    """
    if conn:
        conn.close()

def update_one_param(isTrue, table_name, column, identifier, user_id):
    """
    Cập nhật bảng với một tham số (như grammar) dựa trên isTrue và user_id.
    
    Parameters:
        isTrue (bool): Xác định cập nhật cột 'correct' (nếu True) hoặc 'incorrect' (nếu False).
        table_name (str): Tên bảng cần cập nhật.
        identifier (any): Giá trị để đối chiếu trong điều kiện WHERE.
        column (str): Tên cột dùng trong điều kiện WHERE.
        user_id (int): ID của người dùng.
    """

    if isTrue not in [True, False]:
        print("Giá trị isTrue phải là True hoặc False.")
        return

    # Kết nối cơ sở dữ liệu
    conn, cursor = connect()
    column_to_update = 'correct' if isTrue else 'incorrect'

    try:
        # Kiểm tra nếu identifier tồn tại trong cột với user_id
        check_query = f"SELECT 1 FROM {table_name} WHERE {column} = ? AND user_id = ?"
        cursor.execute(check_query, (identifier, user_id))
        if cursor.fetchone() is None:
            print(f"Giá trị '{identifier}' không tồn tại trong cột '{column}' của user_id = {user_id}. Bỏ qua cập nhật.")
            return

        # Truy vấn SQL với cột WHERE động
        query = f'''
        UPDATE {table_name}
        SET {column_to_update} = {column_to_update} + 1
        WHERE {column} = ? AND user_id = ?
        '''
        cursor.execute(query, (identifier, user_id))
        conn.commit()
        print(f"Cập nhật {column_to_update} cho {column} = '{identifier}' và user_id = {user_id} thành công.")
    except Exception as e:
        print(f"Lỗi khi cập nhật bảng: {e}")
    finally:
        disconnect(conn)

def update_two_params(isTrue, table_name, category, subtype, user_id):
    """
    Cập nhật bảng với hai tham số (như error) dựa trên isTrue và user_id.
    """
    if isTrue not in [True, False]:
        print("Giá trị isTrue phải là True hoặc False.")
        return
        
    conn, cursor = connect()
    try:
        cursor.execute(f'''
        SELECT * FROM {table_name} 
        WHERE category = ? AND subtype = ? AND user_id = ?
        ''', (category, subtype, user_id))
        result = cursor.fetchone()

        if not result:
            print(f"Lỗi: Không tìm thấy '{category} - {subtype}' trong bảng '{table_name}' cho user_id = {user_id}.")
        else:
            column_to_update = 'correct' if isTrue else 'incorrect'
            cursor.execute(f'''
            UPDATE {table_name}
            SET {column_to_update} = {column_to_update} + 1
            WHERE category = ? AND subtype = ? AND user_id = ?
            ''', (category, subtype, user_id))
            conn.commit()
            print(f"Cập nhật {column_to_update} cho lỗi '{category} - {subtype}' và user_id = {user_id} thành công.")
    except Exception as e:
        print(f"Lỗi khi cập nhật bảng: {e}")
    finally:
        disconnect(conn)

def update_vocab(isTrue, table_name, topic, vocab, user_id):
    """
    Cập nhật bảng vocab với topic và vocab cụ thể, kèm theo user_id.
    """
    if isTrue not in [True, False]:
        print("Giá trị isTrue phải là True hoặc False.")
        return
        
    conn, cursor = connect()
    try:
        cursor.execute(f'''
        SELECT * FROM {table_name} 
        WHERE topic = ? AND vocab = ? AND user_id = ?
        ''', (topic, vocab, user_id))
        result = cursor.fetchone()

        if not result:
            print(f"Lỗi: Không tìm thấy '{topic} - {vocab}' trong bảng '{table_name}' cho user_id = {user_id}.")
        else:
            column_to_update = 'correct' if isTrue else 'incorrect'
            cursor.execute(f'''
            UPDATE {table_name}
            SET {column_to_update} = {column_to_update} + 1
            WHERE topic = ? AND vocab = ? AND user_id = ?
            ''', (topic, vocab, user_id))
            conn.commit()
            print(f"Cập nhật {column_to_update} cho từ vựng '{topic} - {vocab}' và user_id = {user_id} thành công.")
    except Exception as e:
        print(f"Lỗi khi cập nhật bảng: {e}")
    finally:
        disconnect(conn)

def insert_sample_error(table_name, example, fix, user_id):
    """
    Thêm dữ liệu vào bảng sample_error với user_id.
    """
    if example is None or fix is None:
        print("Example và fix không được để trống.")
        return
        
    conn, cursor = connect()
    try:
        cursor.execute(f'''
            INSERT INTO {table_name} (user_id, example, fix)
            VALUES (?, ?, ?)
        ''', (user_id, example, fix))
        conn.commit()
        print(f"Dữ liệu đã được thêm thành công vào bảng {table_name} cho user_id = {user_id}.")
    except sqlite3.Error as e:
        print(f"Lỗi khi thêm dữ liệu vào bảng {table_name}: {e}")
    finally:
        disconnect(conn)

def delete_table(table_name):
    """
    Xóa bảng trong cơ sở dữ liệu.
    """
    conn, cursor = connect()
    try:
        cursor.execute(f"DROP TABLE IF EXISTS {table_name};")
        conn.commit()
        print(f"Bảng '{table_name}' đã được xóa thành công.")
    except sqlite3.Error as e:
        print(f"Lỗi khi xóa bảng: {e}")
    finally:
        disconnect(conn)

def get_vocab_topics(user_id):
    """Lấy danh sách chủ đề từ bảng vocab cho user_id"""
    conn, cursor = connect()
    cursor.execute("SELECT DISTINCT topic FROM vocab WHERE user_id = ?", (user_id,))
    topics = [row[0] for row in cursor.fetchall()]
    disconnect(conn)
    return topics

def get_grammar_topics(user_id):
    """Lấy danh sách chủ đề từ bảng grammar cho user_id"""
    conn, cursor = connect()
    cursor.execute("SELECT DISTINCT grammar FROM grammar WHERE user_id = ?", (user_id,))
    topics = [row[0] for row in cursor.fetchall()]
    disconnect(conn)
    return topics

def get_vocab_by_topic(topic, user_id):
    """Lấy tất cả từ vựng theo chủ đề và user_id"""
    conn, cursor = connect()
    try:
        cursor.execute("SELECT vocab FROM vocab WHERE topic = ? AND user_id = ?", (topic, user_id))
        vocab_list = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Đã xảy ra lỗi khi truy vấn cơ sở dữ liệu: {e}")
        return []
    finally:
        disconnect(conn)
    return [v[0] for v in vocab_list]

def get_vocab_mastery_by_topic(topic, user_id, db_path='english_learning.db'):
    """
    Lấy danh sách mastery của các từ trong một topic từ cơ sở dữ liệu theo user_id.

    Parameters:
        topic (str): Tên topic cần lấy danh sách mastery.
        user_id (int): ID của người dùng.
        db_path (str): Đường dẫn đến cơ sở dữ liệu SQLite.

    Returns:
        list: Danh sách (vocab, mastery) của các từ trong topic.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Lấy dữ liệu mastery cho topic được truyền vào
    cursor.execute('''SELECT vocab, mastery FROM vocab WHERE topic = ? AND user_id = ?''', (topic, user_id))
    data = cursor.fetchall()

    if not data:
        conn.close()
        return f"Topic '{topic}' không tồn tại trong cơ sở dữ liệu hoặc không có từ vựng nào cho user_id = {user_id}."

    # Trả về danh sách (vocab, mastery)
    result = [(vocab, mastery) for vocab, mastery in data]

    conn.close()
    return result

def get_grammar_mastery(user_id, db_path='english_learning.db'):
    """
    Lấy mastery của các grammar từ cơ sở dữ liệu theo user_id.

    Parameters:
        user_id (int): ID của người dùng.
        db_path (str): Đường dẫn đến cơ sở dữ liệu SQLite.

    Returns:
        list: Danh sách các grammar và mastery của chúng.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Lấy thẳng cột grammar và mastery từ cơ sở dữ liệu
    cursor.execute('''SELECT grammar, mastery FROM grammar WHERE user_id = ?''', (user_id,))
    data = cursor.fetchall()

    # Đưa dữ liệu vào danh sách kết quả
    result = [(grammar, mastery) for grammar, mastery in data]

    conn.close()
    return result

def get_errors(user_id):
    """
    Lấy danh sách các lỗi mẫu từ bảng sample_error theo user_id.

    Parameters:
        user_id (int): ID của người dùng.

    Returns:
        list: Danh sách các lỗi mẫu (example, fix, correct, incorrect).
    """
    conn, cursor = connect()
    try:
        cursor.execute("SELECT example, fix, correct, incorrect FROM sample_error WHERE user_id = ?", (user_id,))
        results = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Lỗi khi truy vấn bảng sample_error: {e}")
        results = []
    finally:
        disconnect(conn)

    return [{"sentence": row[0], "error": row[1]} for row in results]

# Ví dụ sử dụng hàm
# delete_table('users')
# delete_table('error')
# delete_table('grammar')
# delete_table('sample_error')
# delete_table('vocab')
# update(False, 'error', 'Cấu trúc câu', 'Sử dụng từ ngữ dư thừa')
# update_vocab(True, "vocab",'môi trường', 'biodiversity')
# Sử dụng hàm
# vocab_result = get_vocab_mastery()
# grammar_result = get_grammar_mastery()
# # In kết quả
# print("Vocab Mastery:")
# for item in vocab_result:
#     print(item)

# print("\nGrammar Mastery:")
# for item in grammar_result:
#     print(item)
# print(get_grammar_mastery())