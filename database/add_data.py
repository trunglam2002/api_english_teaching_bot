import sqlite3

def add_default_data_for_user(user_id, cursor):

    # Thêm dữ liệu mặc định vào bảng `error`
    cursor.executemany('''
    INSERT INTO error (user_id, category, subtype, correct, incorrect, mastery)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', [
        (user_id, 'ngữ pháp', 'chủ ngữ và động từ không hợp lệ', 0, 0, 'new'),
        (user_id, 'ngữ pháp', 'lỗi về thì của động từ', 0, 0, 'new'),
        (user_id, 'ngữ pháp', 'sử dụng sai giới từ', 0, 0, 'new'),
        (user_id, 'ngữ pháp', 'lỗi câu điều kiện', 0, 0, 'new'),
        (user_id, 'ngữ pháp', 'câu hỏi sai cấu trúc', 0, 0, 'new'),
        (user_id, 'ngữ pháp', 'câu bị động', 0, 0, 'new'),
        (user_id, 'ngữ pháp', 'câu phức không đúng cấu trúc', 0, 0, 'new'),
        (user_id, 'từ vựng', 'lỗi chính tả', 0, 0, 'new'),
        (user_id, 'từ vựng', 'lựa chọn từ sai nghĩa', 0, 0, 'new'),
        (user_id, 'từ vựng', 'dùng sai từ đồng âm', 0, 0, 'new'),
        (user_id, 'từ vựng', 'lỗi số ít và số nhiều', 0, 0, 'new'),
        (user_id, 'từ vựng', 'lỗi về thành ngữ', 0, 0, 'new'),
        (user_id, 'cấu trúc câu', 'cấu trúc câu không rõ ràng hoặc thiếu thành phần', 0, 0, 'new'),
        (user_id, 'cấu trúc câu', 'sử dụng từ ngữ dư thừa', 0, 0, 'new'),
        (user_id, 'cấu trúc câu', 'đoạn văn bị lặp', 0, 0, 'new')
    ])

    # Thêm dữ liệu mặc định vào bảng `vocab`
    cursor.executemany('''
    INSERT INTO vocab (user_id, topic, vocab, difficulty, correct, incorrect, mastery)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', [
        (user_id, 'môi trường', 'biodiversity', 'hard', 0, 0, 'new'),
        (user_id, 'môi trường', 'sustainability', 'medium', 0, 0, 'new'),
        (user_id, 'công nghệ', 'algorithm', 'hard', 0, 0, 'new'),
        (user_id, 'công nghệ', 'software', 'easy', 0, 0, 'new'),
        (user_id, 'kinh tế', 'inflation', 'medium', 0, 0, 'new'),
        (user_id, 'kinh tế', 'investment', 'medium', 0, 0, 'new'),
        (user_id, 'giáo dục', 'curriculum', 'hard', 0, 0, 'new'),
        (user_id, 'giáo dục', 'scholarship', 'easy', 0, 0, 'new'),
        (user_id, 'y tế', 'diagnosis', 'hard', 0, 0, 'new'),
        (user_id, 'y tế', 'treatment', 'medium', 0, 0, 'new')
    ])

    # Thêm dữ liệu mặc định vào bảng `grammar`
    cursor.executemany('''
    INSERT INTO grammar (user_id, grammar, correct, incorrect, mastery)
    VALUES (?, ?, ?, ?, ?)
    ''', [
        (user_id, 'hiện tại đơn', 0, 0, 'new'),
        (user_id, 'hiện tại tiếp diễn', 0, 0, 'new'),
        (user_id, 'quá khứ đơn', 0, 0, 'new'),
        (user_id, 'quá khứ tiếp diễn', 0, 0, 'new'),
        (user_id, 'tương lai đơn', 0, 0, 'new'),
        (user_id, 'hiện tại hoàn thành', 0, 0, 'new'),
        (user_id, 'quá khứ hoàn thành', 0, 0, 'new'),
        (user_id, 'câu điều kiện loại 0', 0, 0, 'new'),
        (user_id, 'câu điều kiện loại 1', 0, 0, 'new'),
        (user_id, 'câu điều kiện loại 2', 0, 0, 'new'),
        (user_id, 'câu điều kiện loại 3', 0, 0, 'new'),
        (user_id, 'câu bị động', 0, 0, 'new'),
        (user_id, 'câu so sánh hơn', 0, 0, 'new'),
        (user_id, 'câu so sánh nhất', 0, 0, 'new'),
        (user_id, 'động từ dạng danh từ', 0, 0, 'new'),
        (user_id, 'động từ nguyên thể', 0, 0, 'new'),
        (user_id, 'động từ khiếm khuyết', 0, 0, 'new')
    ])
