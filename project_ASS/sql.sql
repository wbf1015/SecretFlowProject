-- 如果 users 表存在，则删除该表
DROP TABLE IF EXISTS users;

-- 创建一个新的 users 表
CREATE TABLE users (
    username VARCHAR(255),
    password VARCHAR(255)
);

-- 插入五个用户记录
INSERT INTO users (username, password) VALUES
    ('alice', '123456'),
    ('bob', 'qwer1234'),
    ('carol', 'rs90123'),
    ('david', '5678!dbn'),
    ('eva', 'serectflow');
