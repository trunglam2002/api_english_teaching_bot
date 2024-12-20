import sqlite3

# Kết nối đến cơ sở dữ liệu
conn = sqlite3.connect('english_learning.db')
cursor = conn.cursor()

# Thêm dữ liệu vào bảng `error`
cursor.executemany('''
INSERT INTO error (category, subtype, correct, incorrect, mastery)
VALUES (?, ?, ?, ?, ?)
''', [
    ('ngữ pháp', 'chủ ngữ và động từ không hợp lệ', 9, 1, 'mastered'),
    ('ngữ pháp', 'lỗi về thì của động từ', 7, 3, 'renewed'),
    ('ngữ pháp', 'sử dụng sai giới từ', 4, 6, 'new'),
    ('ngữ pháp', 'lỗi câu điều kiện', 9, 1, 'mastered'),
    ('ngữ pháp', 'câu hỏi sai cấu trúc', 6, 4, 'renewed'),
    ('ngữ pháp', 'câu bị động', 8, 2, 'renewed'),
    ('ngữ pháp', 'câu phức không đúng cấu trúc', 9, 1, 'mastered'),
    ('từ vựng', 'lỗi chính tả', 9, 1, 'mastered'),
    ('từ vựng', 'lựa chọn từ sai nghĩa', 6, 4, 'renewed'),
    ('từ vựng', 'dùng sai từ đồng âm', 9, 1, 'mastered'),
    ('từ vựng', 'lỗi số ít và số nhiều', 5, 5, 'renewed'),
    ('từ vựng', 'lỗi về thành ngữ', 7, 3, 'renewed'),
    ('cấu trúc câu', 'cấu trúc câu không rõ ràng hoặc thiếu thành phần', 9, 1, 'mastered'),
    ('cấu trúc câu', 'sử dụng từ ngữ dư thừa', 6, 4, 'renewed'),
    ('cấu trúc câu', 'đoạn văn bị lặp', 5, 5, 'renewed')
])

# Thêm dữ liệu vào bảng `vocab`
cursor.executemany('''
INSERT INTO vocab (topic, vocab, difficulty, correct, incorrect, mastery)
VALUES (?, ?, ?, ?, ?, ?)
''', [
    ('môi trường', 'biodiversity', 'hard', 7, 3, 'renewed'),
    ('môi trường', 'sustainability', 'medium', 9, 1, 'mastered'),
    ('công nghệ', 'algorithm', 'hard', 5, 5, 'renewed'),
    ('công nghệ', 'software', 'easy', 10, 0, 'mastered'),
    ('kinh tế', 'inflation', 'medium', 6, 4, 'renewed'),
    ('kinh tế', 'investment', 'medium', 9, 1, 'mastered'),
    ('giáo dục', 'curriculum', 'hard', 9, 0, 'mastered'),
    ('giáo dục', 'scholarship', 'easy', 10, 0, 'mastered'),
    ('y tế', 'diagnosis', 'hard', 7, 3, 'renewed'),
    ('y tế', 'treatment', 'medium', 8, 2, 'renewed')
])

# Thêm dữ liệu vào bảng `grammar` với `correct` và `incorrect`
cursor.executemany('''
INSERT INTO grammar (grammar, correct, incorrect, mastery)
VALUES (?, ?, ?, ?)
''', [
    ('hiện tại đơn', 9, 1, 'mastered'),
    ('hiện tại tiếp diễn', 7, 3, 'renewed'),
    ('quá khứ đơn', 6, 4, 'renewed'),
    ('quá khứ tiếp diễn', 10, 0, 'mastered'),
    ('tương lai đơn', 6, 4, 'renewed'),
    ('hiện tại hoàn thành', 5, 5, 'renewed'),
    ('quá khứ hoàn thành', 7, 3, 'renewed'),
    ('câu điều kiện loại 0', 10, 0, 'mastered'),
    ('câu điều kiện loại 1', 6, 4, 'renewed'),
    ('câu điều kiện loại 2', 5, 5, 'renewed'),
    ('câu điều kiện loại 3', 4, 6, 'new'),
    ('câu bị động', 9, 1, 'mastered'),
    ('câu bị động', 6, 4, 'renewed'),
    ('câu so sánh hơn', 5, 5, 'renewed'),
    ('câu so sánh nhất', 8, 2, 'renewed'),
    ('động từ dạng danh từ', 10, 0, 'mastered'),
    ('động từ nguyên thể', 5, 5, 'renewed'),
    ('động từ khiếm khuyết', 6, 4, 'renewed')
])

# Commit và đóng kết nối
conn.commit()
conn.close()
