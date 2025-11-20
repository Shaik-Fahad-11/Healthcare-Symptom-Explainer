CREATE TABLE IF NOT EXISTS chat_logs (
    id SERIAL PRIMARY KEY,
    user_input TEXT NOT NULL,
    ai_response TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE chat_logs ADD COLUMN IF NOT EXISTS session_id TEXT;
ALTER TABLE chat_logs ADD COLUMN IF NOT EXISTS has_image BOOLEAN DEFAULT FALSE;
ALTER TABLE chat_logs ADD COLUMN IF NOT EXISTS image_data BYTEA;



-- 1. Create Users Table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE
);

-- 2. Add user_id to chat_logs (Linking chats to users)
ALTER TABLE chat_logs ADD COLUMN IF NOT EXISTS user_id INTEGER REFERENCES users(id);


UPDATE users 
SET is_admin = TRUE 
WHERE username = 'your_username';