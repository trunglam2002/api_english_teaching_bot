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

def update_one_param(isTrue, table_name, column, identifier):
    """
    Cập nhật bảng với một tham số (như grammar) dựa trên isTrue.
    
    Parameters:
        isTrue (bool): Xác định cập nhật cột 'correct' (nếu True) hoặc 'incorrect' (nếu False).
        table_name (str): Tên bảng cần cập nhật.
        identifier (any): Giá trị để đối chiếu trong điều kiện WHERE.
        column (str): Tên cột dùng trong điều kiện WHERE.
    """

    if isTrue not in [True, False]:
        print("Giá trị isTrue phải là True hoặc False.")
        return

    # Kết nối cơ sở dữ liệu
    conn, cursor = connect()
    column_to_update = 'correct' if isTrue else 'incorrect'

    try:
        # Kiểm tra nếu identifier tồn tại trong cột
        check_query = f"SELECT 1 FROM {table_name} WHERE {column} = ?"
        cursor.execute(check_query, (identifier,))
        if cursor.fetchone() is None:
            print(f"Giá trị '{identifier}' không tồn tại trong cột '{column}'. Bỏ qua cập nhật.")
            return

        # Truy vấn SQL với cột WHERE động
        query = f'''
        UPDATE {table_name}
        SET {column_to_update} = {column_to_update} + 1
        WHERE {column} = ?
        '''
        cursor.execute(query, (identifier,))
        conn.commit()
        print(f"Cập nhật {column_to_update} cho {column} = '{identifier}' thành công.")
    except Exception as e:
        print(f"Lỗi khi cập nhật bảng: {e}")
    finally:
        disconnect(conn)


def update_two_params(isTrue, table_name, category, subtype):
    """
    Cập nhật bảng với hai tham số (như error) dựa trên isTrue.
    """
    if isTrue != True and isTrue != False:
        return
        
    conn, cursor = connect()
    cursor.execute(f'''
    SELECT * FROM {table_name} 
    WHERE category = ? AND subtype = ?
    ''', (category, subtype))
    result = cursor.fetchone()

    if not result:
        print(f"Lỗi: Không tìm thấy '{category} - {subtype}' trong bảng '{table_name}'.")
    else:
        column_to_update = 'correct' if isTrue else 'incorrect'
        cursor.execute(f'''
        UPDATE {table_name}
        SET {column_to_update} = {column_to_update} + 1
        WHERE category = ? AND subtype = ?
        ''', (category, subtype))
        conn.commit()
        print(f"Cập nhật {column_to_update} cho lỗi '{category} - {subtype}' thành công.")
    disconnect(conn)

def update_vocab(isTrue, table_name, topic, vocab):
    """
    Cập nhật bảng vocab với topic và vocab cụ thể.
    """
    if isTrue != True and isTrue != False:
        return
        
    conn, cursor = connect()
    cursor.execute(f'''
    SELECT * FROM {table_name} 
    WHERE topic = ? AND vocab = ?
    ''', (topic, vocab))
    result = cursor.fetchone()

    if not result:
        print(f"Lỗi: Không tìm thấy '{topic} - {vocab}' trong bảng '{table_name}'.")
    else:
        column_to_update = 'correct' if isTrue else 'incorrect'
        cursor.execute(f'''
        UPDATE {table_name}
        SET {column_to_update} = {column_to_update} + 1
        WHERE topic = ? AND vocab = ?
        ''', (topic, vocab))
        conn.commit()
        print(f"Cập nhật {column_to_update} cho từ vựng '{topic} - {vocab}' thành công.")
    disconnect(conn)

def insert_sample_error(table_name, example, fix):
    """
    Thêm dữ liệu vào bảng sample_error.
    """
    if example == None or fix == None:
        return
        
    conn, cursor = connect()
    try:
        cursor.execute(f'''
            INSERT INTO {table_name} (example, fix)
            VALUES (?, ?)
        ''', (example, fix))
        conn.commit()
        print(f"Dữ liệu đã được thêm thành công vào bảng {table_name}.")
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

def get_vocab_topics():
    """Lấy danh sách chủ đề từ bảng vocab"""
    conn, cursor = connect()
    cursor.execute("SELECT DISTINCT topic FROM vocab")
    topics = [row[0] for row in cursor.fetchall()]
    disconnect(conn)
    return topics

def get_grammar_topics():
    """Lấy danh sách chủ đề từ bảng grammar"""
    conn, cursor = connect()
    cursor.execute("SELECT DISTINCT grammar FROM grammar")
    topics = [row[0] for row in cursor.fetchall()]
    disconnect(conn)
    return topics

def get_vocab_by_topic(topic):
    """Lấy tất cả từ vựng theo chủ đề"""
    conn, cursor = connect()
    try:
        cursor.execute("SELECT vocab FROM vocab WHERE topic = ?", (topic,))
        vocab_list = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Đã xảy ra lỗi khi truy vấn cơ sở dữ liệu: {e}")
        return []
    finally:
        disconnect(conn)
    return [v[0] for v in vocab_list]

def get_vocab_mastery(db_path='english_learning.db'):
    """
    Lấy mastery của các vocab từ cơ sở dữ liệu.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''SELECT topic, correct, incorrect FROM vocab''')
    data = cursor.fetchall()

    topic_data = {}
    for row in data:
        topic, correct, incorrect = row
        if topic not in topic_data:
            topic_data[topic] = {'correct': 0, 'incorrect': 0}
        topic_data[topic]['correct'] += correct
        topic_data[topic]['incorrect'] += incorrect

    result = []
    for topic, counts in topic_data.items():
        correct = counts['correct']
        incorrect = counts['incorrect']
        total = correct + incorrect
        if total == 0:
            mastery = 'new'
        else:
            accuracy = correct / total
            if accuracy > 0.9:
                mastery = 'mastered'
            elif accuracy >= 0.5:
                mastery = 'renewed'
            else:
                mastery = 'new'
        result.append((topic, mastery))

    conn.close()
    return result

def get_grammar_mastery(db_path='english_learning.db'):
    """
    Lấy mastery của các grammar từ cơ sở dữ liệu.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''SELECT grammar, correct, incorrect FROM grammar''')
    data = cursor.fetchall()

    result = []
    for row in data:
        grammar, correct, incorrect = row
        total = correct + incorrect
        if total == 0:
            mastery = 'new'
        else:
            accuracy = correct / total
            if accuracy > 0.9:
                mastery = 'mastered'
            elif accuracy >= 0.5:
                mastery = 'renewed'
            else:
                mastery = 'new'
        result.append((grammar, mastery))

    conn.close()
    return result

def get_errors():
    """Lấy danh sách các lỗi mẫu từ cơ sở dữ liệu"""
    conn = sqlite3.connect("english_learning.db")
    cursor = conn.cursor()

    cursor.execute("SELECT example, fix, correct, incorrect FROM sample_error")
    results = cursor.fetchall()

    conn.close()

    return [{"sentence": row[0], "error": row[1]} for row in results]
# Ví dụ sử dụng hàm
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
# print(get_errors())