import sqlite3

# Kết nối đến cơ sở dữ liệu (sẽ tạo file nếu chưa có)
conn = sqlite3.connect('english_learning.db')
cursor = conn.cursor()

# Tạo bảng `users`
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    age INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
''')

# Tạo bảng `error`
cursor.execute('''
CREATE TABLE IF NOT EXISTS error (
    id1 INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    category TEXT NOT NULL,
    subtype TEXT NOT NULL,
    correct INTEGER DEFAULT 0,
    incorrect INTEGER DEFAULT 0,
    mastery TEXT DEFAULT 'new',
    FOREIGN KEY (user_id) REFERENCES users(id)
);
''')

# Tạo bảng `sample_error`
cursor.execute('''
CREATE TABLE IF NOT EXISTS sample_error (
    id2 INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    example TEXT NOT NULL,
    fix TEXT NOT NULL,
    correct INTEGER DEFAULT 0,
    incorrect INTEGER DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
''')

# Tạo bảng `vocab`
cursor.execute('''
CREATE TABLE IF NOT EXISTS vocab (
    id3 INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    topic TEXT NOT NULL,
    vocab TEXT NOT NULL,
    difficulty TEXT NOT NULL,
    correct INTEGER DEFAULT 0,
    incorrect INTEGER DEFAULT 0,
    mastery TEXT DEFAULT 'new',
    FOREIGN KEY (user_id) REFERENCES users(id)
);
''')

# Tạo bảng `grammar`
cursor.execute('''
CREATE TABLE IF NOT EXISTS grammar (
    id4 INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    grammar TEXT NOT NULL,
    correct INTEGER DEFAULT 0,
    incorrect INTEGER DEFAULT 0,
    mastery TEXT DEFAULT 'new',
    FOREIGN KEY (user_id) REFERENCES users(id)
);
''')

# Trigger cho bảng `error` để cập nhật cột mastery
cursor.execute('''
CREATE TRIGGER IF NOT EXISTS update_mastery_error
AFTER UPDATE ON error
FOR EACH ROW
BEGIN
    UPDATE error
    SET mastery = CASE
        WHEN (NEW.correct * 1.0 / (NEW.correct + NEW.incorrect)) > 0.9 THEN 'mastered'
        WHEN (NEW.correct * 1.0 / (NEW.correct + NEW.incorrect)) >= 0.5 THEN 'renewed'
        ELSE 'new'
    END
    WHERE id1 = NEW.id1;
END;
''')

# Trigger cho bảng `vocab` để cập nhật cột mastery
cursor.execute('''
CREATE TRIGGER IF NOT EXISTS update_mastery_vocab
AFTER UPDATE ON vocab
FOR EACH ROW
BEGIN
    UPDATE vocab
    SET mastery = CASE
        WHEN (NEW.correct * 1.0 / (NEW.correct + NEW.incorrect)) > 0.9 THEN 'mastered'
        WHEN (NEW.correct * 1.0 / (NEW.correct + NEW.incorrect)) >= 0.5 THEN 'renewed'
        ELSE 'new'
    END
    WHERE id3 = NEW.id3;
END;
''')

# Trigger cho bảng `grammar` để cập nhật cột mastery
cursor.execute('''
CREATE TRIGGER IF NOT EXISTS update_mastery_grammar
AFTER UPDATE ON grammar
FOR EACH ROW
BEGIN
    UPDATE grammar
    SET mastery = CASE
        WHEN (NEW.correct * 1.0 / (NEW.correct + NEW.incorrect)) > 0.9 THEN 'mastered'
        WHEN (NEW.correct * 1.0 / (NEW.correct + NEW.incorrect)) >= 0.5 THEN 'renewed'
        ELSE 'new'
    END
    WHERE id4 = NEW.id4;
END;
''')

# Commit và đóng kết nối
conn.commit()
conn.close()

print("Các bảng và trigger đã được tạo thành công.")
